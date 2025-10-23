1. Tạo môi trường ảo

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

2. Cài đặt thư viện

pip install -r requirements.txt

3. Tạo file .env

SECRET_KEY=your-secret-key-here
DATABASE_URL=mssql+pyodbc://user:password@host:port/dbname?driver=ODBC+Driver+17+for+SQL+Server

4. Chạy ứng dụng

uvicorn app.main:app --reload

