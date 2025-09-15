# Apache Airflow con Docker – Quickstart

Este repo contiene un entorno mínimo para aprender y experimentar con **Apache Airflow** usando **Docker Compose**.

## 📖 ¿Qué es Apache Airflow?
Apache Airflow es una plataforma open-source para **orquestar flujos de datos (pipelines)** definidos como **DAGs (Directed Acyclic Graphs)** en Python.
Airflow no procesa datos directamente, sino que **coordina tareas** en distintos sistemas (bases de datos, APIs, big data, cloud).

> Fuente: *Data Pipelines with Apache Airflow* – Bas Harenslak & Julian de Ruiter

## 🚀 Requisitos
- [Docker](https://docs.docker.com/get-docker/)  
- [Docker Compose](https://docs.docker.com/compose/install/)  

Verifica que están instalados:
```bash
docker --version
docker compose version
```

## ⚙️ Instalación
1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/airflow-docker-quickstart.git
cd airflow-docker-quickstart
```

2. Crea las carpetas necesarias:
```bash
mkdir -p dags logs plugins
```

3. Inicializa la base de datos de Airflow:
```bash
docker compose up airflow-init
```

## ▶️ Levantar Airflow
Ejecuta:
```bash
docker compose up
```

Esto levantará los siguientes servicios:
- **Postgres** – base de datos de metadatos.  
- **Airflow Webserver** – interfaz web (http://localhost:8080).  
- **Airflow Scheduler** – planifica tareas.  
- **Airflow Worker** – ejecuta las tareas.  

La primera vez, las credenciales por defecto son:
```
usuario: airflow
password: airflow
```

## 📂 Estructura de directorios
```
├── dags/         # Aquí van tus DAGs en Python
├── logs/         # Logs de ejecución
├── plugins/      # Plugins personalizados
├── docker-compose.yml
└── README.md
```

## 👨‍💻 Tu primer DAG
Crea un archivo en `dags/hello_dag.py` con el siguiente contenido:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="hello_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    hello = BashOperator(
        task_id="hello_task",
        bash_command="echo 'Hello, Airflow!'"
    )
```

Reinicia Airflow y ve a la UI (`http://localhost:8080`) → deberías ver el DAG `hello_dag`.

## 📊 Ejemplos visuales
Puedes ver ejemplos de DAGs en el libro *Data Pipelines with Apache Airflow*:
- Figura 1.2: **Pipeline simple en DAG**  
- Figura 1.6: **Pipeline con ramas paralelas**  
- Figura 1.9: **Arquitectura de Airflow**  

Incluye capturas de pantalla en tus slides/repositorio para reforzar los conceptos.

## 🛑 Detener todo
```bash
docker compose down
```

## 📚 Recursos adicionales
- [Documentación oficial de Airflow](https://airflow.apache.org/docs/)  
- Libro *Data Pipelines with Apache Airflow* (Manning, 2021)  
- [Ejemplos del libro en GitHub](https://github.com/BasPH/data-pipelines-with-apache-airflow)  

