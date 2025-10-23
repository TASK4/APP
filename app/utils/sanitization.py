# app/utils/sanitization.py
import re
import bleach
import html
from typing import Any, Optional


def sanitize_input(data: Any) -> Any:
    """
    Clean input:
    - remove HTML tags (bleach.clean with strip=True)
    - html.unescape
    - remove quotes/parentheses/angle-brackets (no space left)
    - remove other non-alnum characters (do not insert spaces)
    - collapse 3+ consecutive whitespace -> single space (preserve double-space)
    - strip leading/trailing spaces
    Works recursively for dict/list/tuple/set.
    """
    if isinstance(data, str):
        cleaned = bleach.clean(data, tags=[], attributes={}, strip=True)
        cleaned = html.unescape(cleaned)

        # 1) remove quotes, parentheses, angle brackets (no spaces left)
        cleaned = re.sub(r"[\'\"()<>]", "", cleaned)

        # 2) remove other non-alphanumeric characters (do NOT replace with space)
        cleaned = re.sub(r"[^A-Za-z0-9\s]", "", cleaned)

        # 3) collapse 3 or more whitespace into one space (preserve 2-space cases)
        cleaned = re.sub(r"\s{3,}", " ", cleaned)

        # 4) strip edges
        cleaned = cleaned.strip()

        return cleaned

    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}

    elif isinstance(data, (list, tuple, set)):
        container_type = type(data)
        return container_type(sanitize_input(item) for item in data)

    else:
        return data


def sanitize_string(value: Optional[str]) -> Optional[str]:
    """Làm sạch chuỗi, loại bỏ XSS và ký tự thừa"""
    if not value:
        return value
    cleaned = bleach.clean(value, tags=[], strip=True)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def sanitize_email(email: Optional[str]) -> Optional[str]:
    """Chuẩn hóa và kiểm tra định dạng email"""
    if not email:
        return email
    email = email.lower().strip()
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return None
    return email


def sanitize_phone(phone: Optional[str]) -> Optional[str]:
    """Chuẩn hóa và kiểm tra định dạng số điện thoại"""
    if not phone:
        return phone
    phone = re.sub(r'[^0-9+]', '', phone)
    if not re.match(r'^\+?\d{10,11}$', phone):
        return None
    return phone
