# APP-1: API Làm Sạch Dữ Liệu Đầu Vào

Ứng dụng API sử dụng FastAPI, tự động làm sạch dữ liệu đầu vào thông qua middleware.

## Tính năng
- Tự động loại bỏ HTML/script tags, khoảng trắng thừa khỏi dữ liệu đầu vào.
- Bảo vệ API khỏi các tấn công XSS và dữ liệu không hợp lệ.

## Hướng dẫn sử dụng
1. Cài đặt dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Chạy ứng dụng:
   ```
   uvicorn app.main:app --reload
   ```
3. Gửi request tới các endpoint, dữ liệu đầu vào sẽ được làm sạch tự động.

## Kiểm thử
```
pytest tests/
```