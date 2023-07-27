import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from tasks import *
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 1),
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='empower_to_ggdrive',
    default_args=default_args,
    schedule='@daily' # Set your desired schedule interval
)

scrape_task = PythonOperator(
    task_id='scraping',
    python_callable=scraping,
    dag=dag,
)

clean_task = PythonOperator(
    task_id='cleaning',
    python_callable=cleaning,
    dag=dag,
)

scrape_task >> clean_task
