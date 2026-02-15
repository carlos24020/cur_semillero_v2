@echo off
REM Script para iniciar los microservicios en Windows

echo ======================================
echo Iniciando Microservicios - CUR Semillero
echo ======================================

REM Verificar si ya hay procesos escuchando en los puertos
echo.
echo Verificando puertos disponibles...

REM Crear dos ventanas de terminal para los servicios
echo.
echo Iniciando MS-Leaders (Puerto 8001)...
cd ms-leaders
start "MS-Leaders" cmd /k python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload

REM Esperar un poco para que el primer servicio inicie
timeout /t 2

echo Iniciando MS-Projects (Puerto 8000)...
cd ..\ms-projects
start "MS-Projects" cmd /k python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo ======================================
echo Servicios iniciados:
echo - MS-Leaders: http://127.0.0.1:8001
echo - MS-Projects: http://127.0.0.1:8000
echo - Frontend: http://127.0.0.1:8000/static/index.html
echo ======================================
echo.
