from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

with DAG(
    dag_id="lab03_scheduling_catchup",
    start_date=datetime(2025, 9, 14, 0, 0, 0),  # pon 1-2 días atrás para demostrar catchup
    schedule="@hourly",
    catchup=True,
    max_active_runs=1,
    tags=["lab03", "scheduling", "catchup"],
) as dag:

    tick = EmptyOperator(task_id="tick")
