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
    'schedule_interval':'@daily',
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='empower_to_ggdrive',
    default_args=default_args,
    schedule='@daily' # Set your desired schedule interval
)

scrape = PythonOperator(
    task_id='scraping',
    python_callable=scraping,
    dag=dag,
)

clean = PythonOperator(
    task_id='cleaning',
    python_callable=cleaning,
    dag=dag,
)

upload = PythonOperator(
    task_id='upload',
    python_callable=upload_to_ggdrive,
    dag=dag,
)

upload2 = PythonOperator(
    task_id='upload2',
    python_callable=upload_to_ggdrive,
    dag=dag,
)

download = PythonOperator(
    task_id='download',
    python_callable=download_from_ggdrive,
    dag=dag,
)
scrape >> upload >> download >> clean >> upload2