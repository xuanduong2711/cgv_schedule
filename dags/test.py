from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

SRC_DIR = '/opt/airflow/src'
DATA_DIR = '/opt/airflow/data'
OUTPUT_DIR = f'{DATA_DIR}/output'
CRAWL_SCRIPT = f'{SRC_DIR}/crawl_data.py'
TRANSFORM_SCRIPT = f'{SRC_DIR}/transform.py'
INSERT_SCRIPT = f'{SRC_DIR}/insert_data.py'
RAW_JSON = f'{DATA_DIR}/cgv_movies.json'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 7),
    'retries': 0,
}

with DAG(
    dag_id="crawl_and_transform",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=['selenium', 'spark', 'mssql', 'insert'],
) as dag:

    # Task 1: Crawl data với Selenium
    run_crawl_data = BashOperator(
        task_id='run_crawl_data',
        bash_command=f'python3 {CRAWL_SCRIPT}'
    )

    # Task 2: Chạy Spark transformation
    run_transform = BashOperator(
        task_id='run_transform',
        bash_command=(
            f'spark-submit --master local[*] '
            f'--conf spark.executor.memory=4g '
            f'{TRANSFORM_SCRIPT} '
            f'{RAW_JSON} '
            f'{OUTPUT_DIR}'
        )
    )

    # Task 3: Insert vào SQL Server
    run_insert_script = BashOperator(
        task_id='run_insert_script',
        bash_command=(
            f'CSV_FILE=$(ls {OUTPUT_DIR}/part-00000*.csv | head -n 1) && '
            f'python3 {INSERT_SCRIPT} $CSV_FILE'
        )
    )

    run_crawl_data >> run_transform >> run_insert_script
