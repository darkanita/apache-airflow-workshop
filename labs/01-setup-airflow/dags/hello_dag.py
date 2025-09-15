from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definición del DAG
with DAG(
    dag_id="hello_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["example", "intro"],
) as dag:

    hello = BashOperator(
        task_id="hello_task",
        bash_command="echo 'Hello, Airflow!'"
    )

