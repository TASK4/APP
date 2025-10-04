import re

def sanitize_string(value: str) -> str:
    # Loại bỏ script, HTML tags, và khoảng trắng thừa
    value = re.sub(r'<.*?>', '', value)
    value = re.sub(r'\s+', ' ', value).strip()
    return value

def sanitize_input(data):
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    else:
        return data