import re
import html

def sanitize_string(value: str) -> str:
    if not isinstance(value, str):
        return value
        
    # First decode any HTML entities
    value = html.unescape(value)
    
    # Remove script tags and their content
    value = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove other HTML tags but keep their content
    value = re.sub(r'<[^>]+>', '', value)
    
    # Normalize whitespace
    value = ' '.join(value.split())
    
    # Remove any remaining special characters except alphanumeric, spaces and basic punctuation
    value = re.sub(r'[^\w\s-]', '', value)
    
    return value.strip()

def sanitize_input(data):
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, str):
        return sanitize_string(data)
    return data