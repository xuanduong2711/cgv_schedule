# 🚀 mini_prj — Airflow + Spark Integration Project

## 📘 Giới thiệu
Dự án này triển khai **Apache Airflow** để điều phối luồng xử lý dữ liệu (data pipeline) và **Apache Spark** để xử lý dữ liệu phân tán.  
Toàn bộ hệ thống được container hóa bằng **Docker Compose**, giúp dễ dàng cài đặt, mở rộng và quản lý.

---

### 🧩 Mô tả pipeline
1. **Crawl dữ liệu**  
   Sử dụng **Selenium** để tự động thu thập lịch chiếu phim từ trang web **CGV** và lưu về dưới dạng file `.json`.

2. **Xử lý dữ liệu với Spark**  
   Spark đọc file JSON, thực hiện các bước **transform** (lọc, chuẩn hóa dữ liệu) và xuất kết quả ra file `.csv`.

3. **Nạp dữ liệu (Load)**  
   File CSV được nạp vào **database** để phục vụ cho phân tích hoặc hiển thị dashboard.

4. **Điều phối toàn bộ pipeline bằng Airflow (v3.1.0)**  
   Airflow quản lý các task crawl, transform và load, đảm bảo pipeline chạy tự động theo lịch định sẵn.

---

## 🏗️ Cấu trúc thư mục

```bash
├── config
│   └── airflow.cfg
├── dags
│   ├── __pycache__
│   │   └── test.cpython-312.pyc
│   └── test.py
├── data
│   ├── cgv_movies.json
│   ├── create_data.py
│   ├── date_data.csv
│   └── output
│       ├── part-00000-7b793965-3626-4efa-9679-73735a9c0e47-c000.csv
│       └── _SUCCESS
├── Docker
│   ├── airflow
│   │   ├── Dockerfile.airflow
│   │   └── requirements.txt
│   └── spark
│       ├── Dockerfile.spark
│       └── requirements.txt
├── docker-compose.yml
├── logs
├── plugins
├── README.md
└── src
    ├── b.py
    ├── crawl_data.py
    └── transform.py
---
# 🚀 mini_prj — Airflow + Spark Integration Project

## ⚙️ Cách khởi chạy dự án

### 🔧 Các bước thực hiện

1️⃣ **Chuẩn bị môi trường**
- Cài đặt Docker và Docker Compose  
  - 🐳 [Docker](https://docs.docker.com/get-docker/)  
  - ⚙️ [Docker Compose](https://docs.docker.com/compose/)  
- Kiểm tra phiên bản:
  ```bash
  docker --version
  docker compose version

# Build và khởi động toàn bộ container (Airflow + Spark)
docker compose up -d --build

# Sau khi container đã khởi chạy thành công, mở trình duyệt và truy cập:
http://localhost:8080

# Đăng nhập với tài khoản mặc định:
user: airflow
pass: airflow

# Dừng toàn bộ hệ thống khi cần

docker compose down