import os
from dotenv import load_dotenv
import pyodbc

# Tải các biến môi trường
load_dotenv()

# Lấy thông tin cấu hình
SQL_SERVER = os.getenv("SQL_SERVER", "sqlserver")
SQL_PORT = os.getenv("SQL_PORT", "1433")
SQL_DB = os.getenv("SQL_DB", "MovieDB")
SQL_USER = os.getenv("SQL_USER", "sa")
SQL_PASSWORD = os.getenv("SQL_PASSWORD", "") 
TABLE_NAME = os.getenv("TABLE_NAME", "Movie_cgv") # Đảm bảo tên bảng khớp .env

# Xây dựng chuỗi kết nối
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SQL_SERVER},{SQL_PORT};"
    f"DATABASE=master;"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
    f"TrustServerCertificate=yes;"
)

conn = None
try:
    # Kết nối và bật autocommit
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()
    print("✅ Kết nối tới SQL Server thành công.")

    # Tạo database nếu chưa có (logic này đã đúng)
    cursor.execute(f"""
    IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{SQL_DB}')
    BEGIN
        CREATE DATABASE [{SQL_DB}];
    END
    """)

    # Chuyển sang context của database mới
    cursor.execute(f"USE [{SQL_DB}]")

    # --- LOGIC ĐÚNG ĐỂ BẢO VỆ DỮ LIỆU ---
    # Chỉ tạo bảng nếu nó chưa tồn tại. KHÔNG XÓA.
    print(f"Kiểm tra sự tồn tại của bảng '{TABLE_NAME}'...")
    cursor.execute(f"""
    IF OBJECT_ID('dbo.{TABLE_NAME}', 'U') IS NULL
    BEGIN
        PRINT 'Bảng chưa tồn tại, đang tạo bảng mới...';
        CREATE TABLE dbo.{TABLE_NAME} (
            Id INT IDENTITY(1,1) PRIMARY KEY,
            theater NVARCHAR(255) NOT NULL,
            name_movie NVARCHAR(255) NOT NULL,
            [day] TINYINT NOT NULL,
            [month] TINYINT NOT NULL,
            [time] TIME NOT NULL
        );
    END
    """)

    print(f"✅ Cấu trúc database '{SQL_DB}' đã sẵn sàng.")

except pyodbc.Error as ex:
    print(f"❌ Đã xảy ra lỗi pyodbc: {ex}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Đã đóng kết nối.")