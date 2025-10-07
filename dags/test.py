from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

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
    tags=['selenium', 'spark'],
) as dag:

    # Task 1: Crawl data với Selenium
    run_crawl_data = BashOperator(
        task_id='run_crawl_data',
        bash_command=(
            'python3 /opt/airflow/src/crawl_data.py'
        )
    )

    # Task 2: Chạy Spark transformation
    run_transform = BashOperator(
        task_id='run_transform',
        bash_command=(
            'spark-submit --master local[*] '
            '--conf spark.executor.memory=4g '
            '/opt/airflow/src/transform.py '
            '/opt/airflow/data/cgv_movies.json '
            '/opt/airflow/data/output'
        )
    )

    run_crawl_data >> run_transform

