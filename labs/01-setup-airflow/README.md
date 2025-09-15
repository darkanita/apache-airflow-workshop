# Lab 01 – Configuración del ambiente con Apache Airflow (Docker)

En este laboratorio aprenderás a levantar un entorno de **Apache Airflow** usando **Docker Compose**.

## 🚀 Objetivo
- Instalar y ejecutar Apache Airflow en contenedores Docker.
- Conocer la estructura de directorios (`dags/`, `logs/`, `plugins/`).
- Correr tu primer DAG de ejemplo.

## 📦 Requisitos previos
- Docker instalado → [Instrucciones](https://docs.docker.com/get-docker/)
- Docker Compose instalado → [Instrucciones](https://docs.docker.com/compose/install/)

Verifica instalación:
```bash
docker --version
docker compose version
```

## ⚙️ Preparación del ambiente
1. Ve a la carpeta del lab:
```bash
cd labs/01-setup-airflow
```

2. Inicializa la base de datos de Airflow:
```bash
docker compose up airflow-init
```

3. Levanta el entorno completo:
```bash
docker compose up
```

## 🌐 Acceso a la interfaz web
- URL: [http://localhost:8080](http://localhost:8080)
- Usuario: `airflow`
- Password: `airflow`

## 📂 Estructura del directorio
```
01-setup-airflow/
├── dags/              # DAGs de ejemplo
│   └── hello_dag.py
├── logs/              # Logs de ejecución (se llenan al correr Airflow)
├── plugins/           # Plugins personalizados (vacío por ahora)
├── docker-compose.yml # Configuración de servicios
└── README.md          # Este archivo
```

## 👨‍💻 Tu primer DAG
Ya tienes incluido el archivo `dags/hello_dag.py`.  
Para probarlo:
1. Abre la UI en `http://localhost:8080`  
2. Activa el DAG `hello_dag`  
3. Corre una ejecución manual y revisa los logs.

## 🛑 Detener el entorno
```bash
docker compose down
```

---
¡Listo! Has configurado tu primer ambiente de Apache Airflow con Docker 🎉
