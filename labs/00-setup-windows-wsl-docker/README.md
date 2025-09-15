# Lab 00 – Setup de entorno: Windows + WSL2 + Docker Desktop

Este laboratorio deja listo tu equipo Windows para ejecutar **Docker** y desarrollar con **Apache Airflow** en los labs siguientes.

## ✅ Objetivo
- Habilitar **WSL2** (Windows Subsystem for Linux).
- Instalar **Ubuntu 22.04 LTS** como distro de Linux.
- Instalar y enlazar **Docker Desktop** con WSL2.
- Verificar que todo funciona con `docker` y `docker compose`.

> Recomendado: Windows 10 21H2+ o Windows 11 con virtualización habilitada (Intel VT-x / AMD‑V) en BIOS.

---

## 1) Habilitar WSL2 (automático con script)
En **PowerShell como Administrador**, ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\setup.ps1
```

El script hará:
- Activar características **WSL** y **VirtualMachinePlatform**.
- Establecer **WSL2** como versión por defecto.
- (Opcional) Descargar el **kernel** de WSL2 y lanzarlo.
- (Opcional) Instalar `Ubuntu-22.04` (puedes comentarlo si prefieres instalar desde Microsoft Store).
- Añadir tu usuario al grupo `docker-users`.
- Mostrar comandos de verificación al final.

> Si el script pide reiniciar, **reinicia** y vuelve a ejecutarlo hasta que todos los pasos marquen `OK`.

---

## 2) Instalar Ubuntu 22.04 LTS (si no lo hiciste en el script)
En PowerShell (usuario normal):
```powershell
wsl --install -d Ubuntu-22.04
```
Abre **Ubuntu** desde el menú Inicio y crea tu **usuario/contraseña** de Linux.

Verifica:
```powershell
wsl -l -v
```
Debe verse `Ubuntu-22.04 … VERSION 2`.

---

## 3) Instalar Docker Desktop e integrar con WSL2
1. Descarga **Docker Desktop** desde https://www.docker.com/products/docker-desktop/ e instálalo (marca la opción *Use WSL 2 instead of Hyper-V*).
2. Abre Docker Desktop → **Settings → Resources → WSL Integration** → activa “Enable integration” y marca `Ubuntu-22.04`.
3. Reinicia Docker Desktop.

Verifica en PowerShell:
```powershell
docker --version
docker info
docker compose version
```

---

## 4) Prueba rápida
```powershell
docker run hello-world
```
Deberías ver el mensaje de bienvenida. Luego, desde el lab `01-setup-airflow`:
```powershell
docker compose pull
docker compose up airflow-init
docker compose up
```
UI de Airflow: http://localhost:8080  (usuario/clave: `airflow`/`airflow`).

---

## 5) Problemas comunes y soluciones

- **`open //./pipe/docker_engine` / “daemon not running”**  
  Abre **Docker Desktop** y espera a “Docker Engine is running”. Si persiste:
  - Asegúrate de que WSL2 funciona: `wsl -l -v`.
  - Integra la distro en *WSL Integration*.
  - Añádete al grupo `docker-users` y **cierra sesión**.

- **`WSL is not supported…`**  
  No están activadas las características. Repite el **Paso 1** (setup.ps1 como Admin) y reinicia.

- **Rutas OneDrive/espacios**  
  Clona los labs en una ruta corta: `C:\dev\apache-airflow-workshop\`.

- **Virtualización deshabilitada**  
  Habilita VT‑x/AMD‑V en BIOS/UEFI. En el Administrador de tareas → Rendimiento → CPU debe decir *Virtualización: Habilitado*.

---

## 6) Comandos útiles
```powershell
wsl --status
wsl -l -v
wsl --set-default-version 2
wsl --set-default Ubuntu-22.04
wsl --shutdown
docker context ls
```

¡Listo! Con esto, tu entorno está preparado para el **Lab 01**.

