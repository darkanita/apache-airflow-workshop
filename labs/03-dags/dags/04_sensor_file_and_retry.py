import random
from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator

DATA_DIR = "/opt/airflow/dags/data"
TARGET_FILE = f"{DATA_DIR}/input_ready.txt"

def process_file():
    # Simula trabajo y falla a veces para demostrar retries
    if random.random() < 0.5:
        raise RuntimeError("Fallo aleatorio, intenta de nuevo")
    print("Procesado OK")

with DAG(
    dag_id="lab03_sensor_file_and_retry",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["lab03", "sensor", "retries"],
) as dag:

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath=TARGET_FILE,
        poke_interval=10,
        timeout=60*10,  # 10 minutos
        mode="poke",
    )

    work = PythonOperator(
        task_id="process_file",
        python_callable=process_file,
        retries=3,
        retry_delay=timedelta(seconds=15),
    )

    wait_for_file >> work
