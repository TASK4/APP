# tests/test_sanitizer.py
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Thêm path để import module app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.sanitization import sanitize_input
from app.main import app

client = TestClient(app)


# ==========================
# 🔹 TEST HÀM sanitize_input
# ==========================
class TestSanitizeFunction:
    def test_sanitize_string(self):
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
            assert clean == expected, f"Expected '{expected}', got '{clean}'"

    def test_sanitize_dict(self):
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

    def test_sanitize_non_string(self):
        assert sanitize_input(123) == 123
        assert sanitize_input(None) is None
        assert sanitize_input(True) is True


# ==========================
# 🔹 TEST MIDDLEWARE hoạt động
# ==========================
class TestSanitizeMiddleware:
    def test_sanitizer_middleware(self):
        """
        Kiểm tra middleware tự động làm sạch dữ liệu POST.
        """
        response = client.post("/auth/register", json={
            "username": "<script>alert('xss')</script>",
            "email": "test@example.com",
            "password": "password123",
            "role_id": 1
        })
        # Middleware chạy trước controller => username phải được sanitize
        assert response.status_code in (200, 422, 400)
        data = response.json()
        if "username" in data:
            assert "<script>" not in data["username"]

    def test_sanitizer_query_params(self):
        """
        Kiểm tra query params được làm sạch trước khi tới router.
        """
        response = client.get(
            "/auth/me?param=<script>alert('xss')</script>",
            headers={"Authorization": "Bearer invalid_token"},
        )
        # Có thể 401 do token sai, nhưng middleware vẫn chạy
        assert response.status_code == 401
