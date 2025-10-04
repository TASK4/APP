import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.sanitization import sanitize_input

def test_sanitize_string():
    dirty = "<script>alert('x')</script>   Hello   World  "
    clean = sanitize_input(dirty)
    assert clean == "alert('x') Hello World"

def test_sanitize_dict():
    dirty = {"name": "<b>John</b>", "bio": "   Developer   "}
    clean = sanitize_input(dirty)
    assert clean == {"name": "John", "bio": "Developer"}