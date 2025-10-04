import re
import html

def sanitize_input(data: str) -> str:
    if not isinstance(data, str):
        return data
    data = html.escape(data)                     # Ngăn XSS
    data = re.sub(r"(--|\b(OR|AND)\b|;)", "", data, flags=re.IGNORECASE)  # Ngăn SQLi
    return data.strip()
