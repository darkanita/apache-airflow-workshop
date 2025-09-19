from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

DATA_DIR = "/opt/airflow/dags/data"

with DAG(
    dag_id="lab03_etl_chain_bash",
    start_date=datetime(2025, 1, 1),
    schedule=None,  # ejecución manual
    catchup=False,
    tags=["lab03", "etl", "bash"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=f'mkdir -p {DATA_DIR} && echo "id,name\n1,Ana\n2,Juan" > {DATA_DIR}/raw.csv'
    )

    transform = BashOperator(
        task_id="transform",
        bash_command=f"awk -F',' 'NR==1{{print $0",name_upper"}} NR>1{{print $0"," toupper($2)}}' {DATA_DIR}/raw.csv > {DATA_DIR}/clean.csv"
    )

    load = BashOperator(
        task_id="load",
        bash_command=f"cp {DATA_DIR}/clean.csv {DATA_DIR}/warehouse_customers.csv && echo 'Loaded to warehouse_customers.csv'"
    )

    extract >> transform >> load
