# 🚀 Mini Project: ETL Pipeline với Airflow, Spark, MSSQL và Streamlit

## 📘 Giới thiệu  
Dự án này xây dựng một **ETL Pipeline hoàn chỉnh** sử dụng các công nghệ hiện đại trong lĩnh vực **Data Engineering**.  
Toàn bộ hệ thống được **container hóa bằng Docker Compose**, giúp triển khai và quản lý dễ dàng, đồng nhất trên mọi môi trường.

---

## ✨ Công nghệ sử dụng  

| Thành phần | Công nghệ | Mô tả |
|-------------|------------|-------|
| **Orchestration** | Apache Airflow | Điều phối luồng công việc ETL |
| **Processing** | Apache Spark | Xử lý, làm sạch và biến đổi dữ liệu |
| **Storage** | Microsoft SQL Server | Lưu trữ dữ liệu đã xử lý |
| **Visualization** | Streamlit | Hiển thị dữ liệu qua giao diện web |
| **Crawling** | Selenium | Thu thập dữ liệu từ website CGV |
| **Containerization** | Docker & Docker Compose | Đóng gói, triển khai hệ thống |

---

## 🧩 Quy trình hoạt động (Workflow)

### 1️⃣ Extract – Thu thập dữ liệu  
- Airflow kích hoạt script Python sử dụng **Selenium** để thu thập lịch chiếu phim từ website CGV.  
- Dữ liệu được lưu dưới dạng **JSON** trong thư mục `data/raw/`.

### 2️⃣ Transform – Xử lý dữ liệu  
- **Apache Spark** đọc file JSON và thực hiện các bước:  
  - Làm sạch dữ liệu  
  - Chuẩn hóa định dạng  
  - Biến đổi dữ liệu thành cấu trúc mong muốn  
- Dữ liệu đầu ra được lưu thành các file **CSV** trong thư mục `data/output/`.

### 3️⃣ Load – Nạp dữ liệu  
- Một script Python khác đọc các file CSV đã xử lý và **insert** dữ liệu vào **Microsoft SQL Server**.  
- Trước khi nạp, dữ liệu cũ được **xóa tự động** để đảm bảo luôn cập nhật.

### 4️⃣ Visualization – Hiển thị dữ liệu  
- Ứng dụng **Streamlit** truy vấn dữ liệu trực tiếp từ **SQL Server**.  
- Giao diện hiển thị bảng dữ liệu có thể lọc, tìm kiếm và trực quan hóa.

### 5️⃣ Orchestration – Điều phối toàn bộ  
- Toàn bộ pipeline được định nghĩa trong một **DAG** của **Apache Airflow**.  
- Airflow đảm bảo các tác vụ chạy theo thứ tự, tự động hóa toàn bộ quy trình theo lịch định sẵn (ví dụ: chạy hàng ngày).

---

## 🏗️ Cấu trúc thư mục  

```bash
mini_prj
├── config
│   └── airflow.cfg
├── dags
│   ├── full_task.py
│   └── __pycache__
│       └── full_task.cpython-312.pyc
├── data
│   ├── cgv_movies.json
│   └── output
│       ├── part-00000-bd064b10-56f9-495f-9b5f-5c9f054eed1c-c000.csv
│       └── _SUCCESS
├── Docker
│   ├── airflow
│   │   ├── Dockerfile.airflow
│   │   └── requirements.txt
│   ├── mssql
│   │   ├── Dockerfile.sqlserver
│   │   └── entrypoint.sh
│   ├── spark
│   │   ├── Dockerfile.spark
│   │   └── requirements.txt
│   └── streamlit
│       ├── Dockerfile.streamlit
│       └── requirements.txt
├── docker-compose.yml
├── logs
│   └── dag_processor
│       ├── 2025-10-08
│       │   └── dags-folder
│       │       └── full_task.py.log
│       └── latest -> 2025-10-08
├── plugins
├── README.md
├── sql
└── src
    ├── crawl_data.py
    ├── init_db.py
    ├── insert_data.py
    ├── streamlit_app_db.py
    └── transform.py


---
## ⚙️ Hướng dẫn khởi chạy

### 1️⃣ Chuẩn bị môi trường  

#### 🔧 Yêu cầu hệ thống
- Đã cài đặt **Docker** và **Docker Compose**  
- Kiểm tra bằng:
```bash
docker --version
docker compose version
```

### ⚙️ Tạo cấu hình `.env`
```bash
AIRFLOW_UID=1000
AIRFLOW_GID=0

SQL_SERVER=
SQL_PORT=1433
SQL_DB=
SQL_USER=
SQL_PASSWORD= { pass phải trên 8 kí tự và bao gồm chữ hoa, thường, số và kí tự đặc biệt}
STREAMLIT_PORT=8888
```

### 🚀 Khởi động toàn bộ hệ thống
```bash
docker compose up -d --build
```
> Lệnh này sẽ build toàn bộ image (Airflow, SQL Server, Streamlit, ...)  
> và khởi chạy tất cả container ở chế độ nền.

---

### 🌐 Truy cập các dịch vụ

| Thành phần | URL | Ghi chú |
|-------------|------|---------|
| **Airflow Web UI** | http://localhost:8080 | Đăng nhập để quản lý DAG |
| **Streamlit App** | http://localhost:8888 | Giao diện hiển thị dữ liệu |

#### 🔑 Thông tin đăng nhập Airflow
- **User:** `airflow`  
- **Password:** `airflow`

---

### ▶️ Chạy pipeline ETL
1. Mở **Airflow Web UI** tại [http://localhost:8080](http://localhost:8080)  
2. Đăng nhập bằng tài khoản trên  
3. **Kích hoạt và Run DAG** `full_task` để bắt đầu pipeline  
4. Sau khi DAG chạy xong, truy cập **Streamlit App** tại [http://localhost:8888](http://localhost:8888)  
   → Lọc theo **rạp chiếu** hoặc **tên phim** để xem kết quả.

---

### 🧹 Dừng toàn bộ hệ thống
```bash
docker compose down
```
