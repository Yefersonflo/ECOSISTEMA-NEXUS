@echo off
cd /d "%~dp0"
echo Sincronizando Excel particionado de Nexus hacia Archivo Caja...
venv\Scripts\python.exe manage.py sync_excel_carpetas --clear-workers
pause
