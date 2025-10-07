import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.sanitization import sanitize_input

def test_sanitize_string():
    test_cases = [
        ("<script>alert('xss')</script>", "alertxss"),
        ("   Hello   World  ", "Hello World"),
        ("<b>Bold</b> text", "Bold text"),
        ("Hello & World", "Hello  World"),
        ("<img src=x onerror=alert(1)>", ""),
        ("Normal text 123", "Normal text 123"),
    ]
    
    for dirty, expected in test_cases:
        clean = sanitize_input(dirty)
        assert clean == expected

def test_sanitize_dict():
    dirty = {
        "name": "<b>John</b>",
        "bio": "   Developer   ",
        "tags": ["<script>bad</script>", "good"],
        "nested": {"key": "<i>value</i>"}
    }
    
    expected = {
        "name": "John",
        "bio": "Developer",
        "tags": ["bad", "good"],
        "nested": {"key": "value"}
    }
    
    clean = sanitize_input(dirty)
    assert clean == expected

def test_sanitize_non_string():
    assert sanitize_input(123) == 123
    assert sanitize_input(None) is None
    assert sanitize_input(True) is True