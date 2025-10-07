# 🚀 mini_prj — Airflow + Spark Integration Project

## 📘 Giới thiệu
Dự án này triển khai **Apache Airflow** để điều phối luồng xử lý dữ liệu (data pipeline) và **Apache Spark** để xử lý dữ liệu phân tán.  
Toàn bộ hệ thống được container hóa bằng **Docker Compose**, giúp dễ dàng cài đặt, mở rộng và quản lý.

### 🧩 Mô tả pipeline
1. **Crawl dữ liệu**:  
   Sử dụng **Selenium** để tự động thu thập lịch chiếu phim từ trang web **CGV** và lưu về dưới dạng file `.json`.

2. **Xử lý dữ liệu với Spark**:  
   Spark đọc file JSON, thực hiện các bước **transform** (lọc, chuẩn hóa dữ liệu) và xuất kết quả ra file `.csv`.

3. **Nạp dữ liệu (Load)**:  
   File CSV được nạp vào **database** để phục vụ cho phân tích hoặc hiển thị dashboard.

4. **Điều phối toàn bộ pipeline bằng Airflow (v3.1.0)**:  
   Airflow quản lý các task crawl, transform và load, đảm bảo pipeline chạy tự động theo lịch định sẵn.

---

## 🏗️ Cấu trúc thư mục

mini_prj/
├── config/
│ └── airflow.cfg
├── dags/
│ ├── test.py
│ └── pycache/
├── data/
│ ├── cgv_movies.json
│ ├── create_data.py
│ ├── date_data.csv
│ └── output/
│ ├── part-00000-xxxx.csv
│ └── _SUCCESS
├── Docker/
│ ├── airflow/
│ │ ├── Dockerfile.airflow
│ │ └── requirements.txt
│ └── spark/
│ ├── Dockerfile.spark
│ └── requirements.txt
├── docker-compose.yml
├── logs/
├── plugins/
├── src/
│ ├── crawl_data.py
│ ├── transform.py
│ └── b.py
└── README.md


---

## ⚙️ Cách khởi chạy dự án

### 1️⃣ Chuẩn bị môi trường
Cài đặt các công cụ sau:
- [Docker]
- [Docker Compose]

### 2️⃣ Xây dựng và khởi động toàn bộ hệ thống
```bash
docker compose up -d --build

3️⃣ Truy cập giao diện Airflow

Mở trình duyệt và truy cập:
👉 http://localhost:8080
user: airflow
pass: airflow