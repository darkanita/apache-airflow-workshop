# Lab 03 – Ejemplos prácticos para crear DAGs

En este lab verás **4 patrones** fundamentales para crear DAGs en Airflow y practicarás dependencias, TaskFlow API/XComs, scheduling/catchup, sensores y retries.

> Requisitos: tener el stack del **Lab 01** corriendo (`docker compose up`) y copiar esta carpeta dentro de `labs/` de tu repo. Los DAGs se cargan desde `labs/03-dag-examples/dags/` al contenedor (si usas el compose del Lab 01, se monta `./dags` del lab).

## Estructura
```
03-dag-examples/
├── dags/
│   ├── 01_etl_chain_bash.py
│   ├── 02_taskflow_xcom.py
│   ├── 03_scheduling_catchup.py
│   └── 04_sensor_file_and_retry.py
└── README.md
```

## Cómo usar
1. Abre la UI en http://localhost:8080
2. **Activa** cada DAG (switch) y haz **Trigger DAG** manual para probar.
3. Revisa las vistas **Graph** y **Grid** y abre los **Logs** de cada tarea.

---

## 1) `01_etl_chain_bash.py` – ETL con BashOperators
- Tres tareas encadenadas: `extract >> transform >> load`.
- Escribe archivos en `/opt/airflow/dags/data/` dentro del contenedor.
- Ideal para explicar dependencias y artefactos simples.

## 2) `02_taskflow_xcom.py` – TaskFlow API + XComs
- Define tareas con `@task` y **retorna valores** que viajan como XCom.
- Muestra cómo **una tarea consume el output** de otra como argumento Python.

## 3) `03_scheduling_catchup.py` – Programación y Catchup
- DAG programado `@hourly` con `start_date` en el pasado.
- Activa `catchup=True` para ver cómo el scheduler **crea runs históricos**.
- Tip: después de la demo, vuelve a `catchup=False` si no quieres llenar el historial.

## 4) `04_sensor_file_and_retry.py` – Sensor + Retries
- `FileSensor` espera a que aparezca `dags/data/input_ready.txt`.
- Luego corre una tarea `process_file` que **falla aleatoriamente** para demostrar `retries` y `retry_delay`.
- Para dispararlo, crea el archivo dentro del contenedor webserver/scheduler:
  ```bash
  docker exec -it <ID_DEL_CONTENEDOR_WEB> bash -lc 'mkdir -p /opt/airflow/dags/data && echo "ready" > /opt/airflow/dags/data/input_ready.txt'
  ```
  (o simplemente crea el archivo desde tu host en `labs/03-dag-examples/dags/data/input_ready.txt` si montas la carpeta).

---

## Limpieza
- Puedes borrar los archivos generados en `dags/data/` y detener el stack con `docker compose down`.

¡Listo! Con estos ejemplos tendrás material suficiente para enseñar a crear DAGs desde cero y discutir buenas prácticas.
