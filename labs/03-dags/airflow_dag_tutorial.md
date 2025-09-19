# Apache Airflow DAGs Tutorial

## What is Apache Airflow?

Apache Airflow is an open-source platform for developing, scheduling, and monitoring workflows. It allows you to programmatically author, schedule, and monitor data pipelines using Python.

## What are DAGs?

**DAG** stands for **Directed Acyclic Graph**. In Airflow:
- **Directed**: Tasks have dependencies and flow in one direction
- **Acyclic**: No circular dependencies (no loops)
- **Graph**: A collection of tasks with dependencies between them

Think of a DAG as a blueprint for your workflow that defines:
- What tasks to run
- When to run them
- In what order
- How they depend on each other

## Core Concepts

### 1. Task
A single unit of work (e.g., run a Python function, execute SQL, send email)

### 2. Operator
Defines what a task does. Common operators:
- `PythonOperator`: Execute Python functions
- `BashOperator`: Execute bash commands
- `SQLOperator`: Execute SQL queries
- `EmailOperator`: Send emails

### 3. Task Instance
A specific run of a task for a particular execution date

### 4. DAG Run
A single execution of the entire DAG for a specific date/time

## Basic DAG Structure

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments for all tasks
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'my_first_dag',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['tutorial'],
)
```

## Example 1: Simple Python Tasks

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def extract_data():
    print("Extracting data from source...")
    return "data_extracted"

def transform_data(**context):
    # Access the return value from previous task
    extracted_data = context['task_instance'].xcom_pull(task_ids='extract')
    print(f"Transforming {extracted_data}...")
    return "data_transformed"

def load_data(**context):
    transformed_data = context['task_instance'].xcom_pull(task_ids='transform')
    print(f"Loading {transformed_data} to destination...")
    return "data_loaded"

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Simple ETL pipeline',
    schedule_interval='@daily',
    catchup=False,
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task
```

## Example 2: Mixed Operators with Branching

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

def check_data_quality(**context):
    # Simulate data quality check
    import random
    data_quality_score = random.uniform(0, 1)
    
    if data_quality_score > 0.8:
        return 'high_quality_process'
    else:
        return 'low_quality_process'

def process_high_quality_data():
    print("Processing high quality data with advanced algorithms")

def process_low_quality_data():
    print("Processing low quality data with basic cleaning")

default_args = {
    'owner': 'data_team',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'branching_pipeline',
    default_args=default_args,
    description='Pipeline with conditional branching',
    schedule_interval='@daily',
    catchup=False,
)

start = DummyOperator(task_id='start', dag=dag)

data_ingestion = BashOperator(
    task_id='data_ingestion',
    bash_command='echo "Ingesting data from various sources"',
    dag=dag,
)

quality_check = BranchPythonOperator(
    task_id='quality_check',
    python_callable=check_data_quality,
    dag=dag,
)

high_quality_process = PythonOperator(
    task_id='high_quality_process',
    python_callable=process_high_quality_data,
    dag=dag,
)

low_quality_process = PythonOperator(
    task_id='low_quality_process',
    python_callable=process_low_quality_data,
    dag=dag,
)

end = DummyOperator(
    task_id='end',
    trigger_rule='none_failed_or_skipped',  # Run even if upstream tasks are skipped
    dag=dag,
)

# Set dependencies
start >> data_ingestion >> quality_check
quality_check >> [high_quality_process, low_quality_process]
[high_quality_process, low_quality_process] >> end
```

## Schedule Intervals

Airflow supports various scheduling options:

```python
# Common schedule intervals
schedule_interval='@daily'          # Run daily at midnight
schedule_interval='@hourly'         # Run every hour
schedule_interval='@weekly'         # Run weekly on Sunday at midnight
schedule_interval='@monthly'        # Run monthly on first day at midnight
schedule_interval='0 2 * * *'       # Cron expression: daily at 2 AM
schedule_interval=timedelta(hours=4) # Every 4 hours
schedule_interval=None              # Manual trigger only
```

## Task Dependencies

Multiple ways to set dependencies:

```python
# Method 1: Bit shift operators
task1 >> task2 >> task3

# Method 2: Multiple dependencies
task1 >> [task2, task3] >> task4

# Method 3: Using set methods
task1.set_downstream(task2) #means task2 will run after task1 finishes.
task2.set_upstream(task1) #means task2 depends on task1 (so, again, task2 runs after task1).

# Method 4: Complex dependencies
task1 >> task2
task1 >> task3
[task2, task3] >> task4
```

## XCom (Cross-Communication)

Share data between tasks:

```python
def producer_task(**context):
    value = "Hello from producer"
    # Push value to XCom
    context['task_instance'].xcom_push(key='my_key', value=value)
    return value  # Also pushes to XCom with default key

def consumer_task(**context):
    # Pull value from XCom
    value = context['task_instance'].xcom_pull(task_ids='producer', key='my_key')
    # Or pull return value (default key)
    return_value = context['task_instance'].xcom_pull(task_ids='producer')
    print(f"Received: {value}")
```

## Error Handling and Retries

```python
from airflow.exceptions import AirflowException

def task_with_retry():
    import random
    if random.random() < 0.7:  # 70% chance of failure
        raise AirflowException("Simulated failure")
    print("Task succeeded!")

retry_task = PythonOperator(
    task_id='retry_task',
    python_callable=task_with_retry,
    retries=3,
    retry_delay=timedelta(seconds=30),
    dag=dag,
)
```

## Best Practices

### 1. DAG Design
- Keep DAGs simple and focused
- Use meaningful names for DAGs and tasks
- Add documentation and descriptions
- Use tags to organize DAGs

### 2. Task Design
- Make tasks idempotent (can run multiple times safely)
- Keep tasks atomic and focused on single responsibility
- Use appropriate operators for the task type
- Handle errors gracefully

### 3. Dependencies
- Minimize cross-DAG dependencies
- Use sensors for external dependencies
- Avoid deep nesting of tasks

### 4. Configuration
```python
# Use Airflow Variables and Connections
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook

# Get configuration values
api_key = Variable.get("api_key")
db_conn = BaseHook.get_connection("my_database")
```

### 5. Testing DAGs
```python
# Test that DAG can be parsed
import pytest
from airflow.models import DagBag

def test_dag_loads():
    dagbag = DagBag()
    dag = dagbag.get_dag('my_dag_id')
    assert dag is not None
    assert len(dag.tasks) == expected_task_count
```

## Common Patterns

### 1. Dynamic Task Generation
```python
def create_tasks():
    tasks = []
    for i in range(5):
        task = PythonOperator(
            task_id=f'dynamic_task_{i}',
            python_callable=lambda: print(f"Task {i} executed"),
            dag=dag,
        )
        tasks.append(task)
    return tasks

dynamic_tasks = create_tasks()
```

### 2. File Processing Pipeline
```python
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='check_file',
    filepath='/path/to/file.csv',
    fs_conn_id='fs_default',
    poke_interval=60,
    timeout=300,
    dag=dag,
)

process_file = PythonOperator(
    task_id='process_file',
    python_callable=process_csv_file,
    dag=dag,
)

file_sensor >> process_file
```

## Getting Started Steps

1. **Install Airflow**:
   ```bash
   pip install apache-airflow
   ```

2. **Initialize Database**:
   ```bash
   airflow db init
   ```

3. **Create User**:
   ```bash
   airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

4. **Start Services**:
   ```bash
   # Terminal 1: Start webserver
   airflow webserver --port 8080
   
   # Terminal 2: Start scheduler
   airflow scheduler
   ```

5. **Create DAG File**: Save your DAG Python file in the `dags/` folder

6. **Access Web UI**: Open http://localhost:8080

## Debugging Tips

- Use `airflow dags list` to see all DAGs
- Use `airflow tasks test dag_id task_id execution_date` to test individual tasks
- Check logs in the web UI for task execution details
- Use `print()` statements in Python functions for debugging
- Validate DAG syntax with `python your_dag_file.py`

This tutorial covers the fundamentals of Airflow DAGs. Start with simple examples and gradually add complexity as you become more comfortable with the concepts!