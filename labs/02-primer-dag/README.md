# Lab 02 – Crear un DAG con dependencias (ETL simple)

En este laboratorio escribirás un **DAG con 3 tareas encadenadas** que simulan un flujo **ETL**:
1) `extract` → genera datos de ventas (CSV)
2) `transform` → calcula métricas (JSON)
3) `load` → 'carga' los datos (simulado) y registra el resultado

> Este lab se enfoca en **definir dependencias** entre tareas con Airflow 2.x.

## 🎯 Objetivos
- Definir múltiples tareas en un DAG.
- Encadenar tareas con `>>` (o `set_downstream`).
- Entender el patrón **ETL** dentro de Airflow.

## 📂 Estructura
```
labs/02-primer-dag/
├── README.md
└── dags/
    └── etl_dag.py
```

## ▶️ Pasos
1. Copia esta carpeta dentro de tu repo del workshop.
2. Asegúrate de tener corriendo el stack de Airflow (Lab 01):
   ```bash
   docker compose up
   ```
3. Entra a la UI: http://localhost:8080
4. Activa el DAG **etl_dag** y lanza una ejecución manual (Trigger DAG).

## 🔎 ¿Qué hace cada tarea?
- **extract**: crea `/opt/airflow/dags/data/sales_YYYYMMDD.csv` con datos ficticios.
- **transform**: lee el CSV, calcula total y promedio y genera `/opt/airflow/dags/data/metrics_YYYYMMDD.json`.
- **load**: simula cargar las métricas a un sistema destino (solo imprime en logs).

## 🧹 Limpieza
Los archivos se escriben bajo `dags/data/`. Puedes borrarlos si deseas reiniciar el ejercicio.

---

✅ Consejo: Abre el DAG → pestaña **Graph** para ver el flujo ETL, ejecuta y revisa **Logs** de cada tarea.
