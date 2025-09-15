<#
 Lab 00 Setup - Windows + WSL2 + Docker Desktop helper
 Ejecutar en PowerShell como **Administrador**.
#>

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "OK  $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "!!  $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "XX  $msg" -ForegroundColor Red }

# 0) Comprobar admin
If (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Err "Ejecuta este script en PowerShell **como Administrador**."
    exit 1
}

# 1) Habilitar características
Write-Step "Habilitando características de Windows: WSL y VirtualMachinePlatform"
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart | Out-Null
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart | Out-Null
Write-Ok "Características habilitadas (puede requerir reinicio)."

# 2) Establecer WSL2 por defecto
Write-Step "Estableciendo WSL2 como versión por defecto"
wsl --set-default-version 2
if ($LASTEXITCODE -eq 0) { Write-Ok "WSL2 por defecto." } else { Write-Warn "Reintenta tras reiniciar si falla." }

# 3) (Opcional) Descargar kernel WSL2
$downloadKernel = Read-Host "¿Descargar e iniciar instalador del kernel WSL2? (s/n)"
if ($downloadKernel -match '^[sS]') {
    $url = "https://aka.ms/wsl2kernel"
    $tmp = "$env:TEMP\wsl2kernel.msi"
    Write-Step "Descargando kernel desde $url"
    try {
        Invoke-WebRequest -Uri $url -OutFile $tmp -UseBasicParsing
        Write-Ok "Descarga completa: $tmp"
        Start-Process msiexec.exe -ArgumentList @("/i", "`"$tmp`"", "/passive") -Wait
        Write-Ok "Kernel instalado."
    } catch {
        Write-Err "Fallo al descargar/instalar el kernel: $_"
    }
} else {
    Write-Warn "Saltando descarga del kernel. Asegúrate de instalarlo manualmente si es necesario."
}

# 4) (Opcional) Instalar Ubuntu 22.04
$installDistro = Read-Host "¿Instalar Ubuntu-22.04 ahora? (s/n)"
if ($installDistro -match '^[sS]') {
    Write-Step "Instalando Ubuntu-22.04 (puede tardar)"
    wsl --install -d Ubuntu-22.04
    Write-Ok "Instalación solicitada. Completa la configuración de usuario al abrir Ubuntu."
} else {
    Write-Warn "Puedes instalar luego con: wsl --install -d Ubuntu-22.04"
}

# 5) Añadir usuario al grupo docker-users
Write-Step "Añadiendo usuario actual al grupo local 'docker-users' (si existe)"
$usr = "$env:USERNAME"
cmd.exe /c "net localgroup docker-users $usr /add" | Out-Null
Write-Ok "Usuario $usr añadido (si el grupo existe). Cierra sesión para aplicar."

# 6) Mostrar estado
Write-Step "Estado WSL"
wsl --status
wsl -l -v

Write-Step "Recordatorios"
Write-Host "- Instala Docker Desktop y activa WSL Integration para Ubuntu-22.04" -ForegroundColor Yellow
Write-Host "- Reinicia cuando Windows lo solicite." -ForegroundColor Yellow
