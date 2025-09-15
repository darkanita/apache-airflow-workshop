from __future__ import annotations

import csv
import json
import os
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

DATA_DIR = "/opt/airflow/dags/data"
os.makedirs(DATA_DIR, exist_ok=True)


def extract_fn(execution_date: datetime, **context):
    """Genera un CSV de ventas ficticio para la fecha de ejecución."""
    run_date = (execution_date or datetime.utcnow()).strftime("%Y%m%d")
    csv_path = os.path.join(DATA_DIR, f"sales_{run_date}.csv")
    rows = [
        {"id": 1, "amount": 100.0},
        {"id": 2, "amount": 250.5},
        {"id": 3, "amount": 75.25},
        {"id": 4, "amount": 10.0},
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "amount"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[extract] wrote {csv_path} with {len(rows)} rows")


def transform_fn(execution_date: datetime, **context):
    """Lee el CSV y calcula métricas simples; escribe un JSON con el resultado."""
    run_date = (execution_date or datetime.utcnow()).strftime("%Y%m%d")
    csv_path = os.path.join(DATA_DIR, f"sales_{run_date}.csv")
    json_path = os.path.join(DATA_DIR, f"metrics_{run_date}.json")

    total = 0.0
    count = 0
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += float(row["amount"])
            count += 1
    avg = total / count if count else 0.0

    metrics = {"run_date": run_date, "total": total, "count": count, "avg": avg}
    with open(json_path, "w") as f:
        json.dump(metrics, f)
    print(f"[transform] read {csv_path}, wrote {json_path}: {metrics}")


def load_fn(execution_date: datetime, **context):
    """Simula la carga de métricas a un destino (solo log)."""
    run_date = (execution_date or datetime.utcnow()).strftime("%Y%m%d")
    json_path = os.path.join(DATA_DIR, f"metrics_{run_date}.json")
    with open(json_path) as f:
        metrics = json.load(f)
    # Aquí iría una inserción en DB o POST a una API.
    print(f"[load] loaded metrics for {run_date}: {metrics}")


with DAG(
    dag_id="etl_dag",
    description="ETL simple con dependencias: extract >> transform >> load",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["workshop", "lab02", "etl"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_fn,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_fn,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_fn,
    )

    # Dependencias: extract -> transform -> load
    extract >> transform >> load
