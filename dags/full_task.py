from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
# Sử dụng Operator từ provider để tránh cảnh báo "deprecated"
from airflow.providers.standard.operators.bash import BashOperator

# Định nghĩa các hằng số đường dẫn để dễ đọc và bảo trì
SRC_DIR = '/opt/airflow/src'
DATA_DIR = '/opt/airflow/data'
OUTPUT_DIR = f'{DATA_DIR}/output'

with DAG(
    dag_id="movie_data_pipeline",
    start_date=pendulum.datetime(2025, 10, 8, tz="Asia/Ho_Chi_Minh"),
    schedule='@daily',
    catchup=False,
    tags=['movie', 'pipeline', 'etl', 'spark'],
) as dag:
    # Task 1: Đảm bảo DB và bảng đã sẵn sàng. An toàn để chạy lại.
    initialize_database = BashOperator(
        task_id='initialize_database',
        bash_command=f'python {SRC_DIR}/init_db.py'
    )

    # Task 2: Crawl dữ liệu phim thô.
    crawl_data = BashOperator(
        task_id='crawl_movie_data',
        bash_command=f'python {SRC_DIR}/crawl_data.py'
    )

    # Task 3: Chạy job Spark để chuyển đổi dữ liệu thô.
    transform_data = BashOperator(
        task_id='transform_data',
        bash_command=(
            f'spark-submit --master local[*] '
            f'{SRC_DIR}/transform.py '
            f'{DATA_DIR}/cgv_movies.json '  # File đầu vào
            f'{OUTPUT_DIR}'                 # Thư mục đầu ra
        )
    )

    # Task 4: Chèn dữ liệu đã chuyển đổi vào MS SQL Server.
    # Script Python đủ thông minh để tự tìm tất cả các file part-*.csv bằng glob.
    # Chúng ta không cần truyền tên file cụ thể vào nữa.
    insert_data = BashOperator(
        task_id='insert_data_to_db',
        bash_command=f'python {SRC_DIR}/insert_data.py'
    )

    # Định nghĩa thứ tự thực thi của các task
    initialize_database >> crawl_data >> transform_data >> insert_data

