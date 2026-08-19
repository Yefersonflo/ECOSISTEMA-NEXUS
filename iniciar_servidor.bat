@echo off
title Servidor Plataforma Web NEXUS
echo ===================================================
echo   INICIANDO SERVIDOR DE LA PLATAFORMA WEB (NEXUS)
echo ===================================================
echo.
cd /d "%~dp0"

:: Liberar el puerto 8000 si ya esta en uso para evitar errores de enlace
echo [*] Buscando procesos activos en el puerto 8000...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($p) { Stop-Process -Id $p.OwningProcess -Force -ErrorAction SilentlyContinue }"

:: Abrir el navegador en segundo plano tras 3 segundos
echo [*] Preparando navegador para abrir la aplicacion...
start /min powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0abrir_navegador.ps1"

if exist "venv\Scripts\python.exe" (
    echo Iniciando Django usando el entorno virtual (venv)...
    venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
) else (
    echo [ERROR] No se encontro el entorno virtual en: venv\Scripts\python.exe
    echo Intentando iniciar con el comando de python del sistema...
    python manage.py runserver 0.0.0.0:8000
)
pause

