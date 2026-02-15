#!/bin/bash
# Script para iniciar los microservicios en Linux/Mac

echo "======================================"
echo "Iniciando Microservicios - CUR Semillero"
echo "======================================"

# Crear dos terminales para los servicios
echo ""
echo "Iniciando MS-Leaders (Puerto 8001)..."
cd ms-leaders
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload &
LEADERS_PID=$!

# Esperar un poco para que el primer servicio inicie
sleep 2

echo "Iniciando MS-Projects (Puerto 8000)..."
cd ../ms-projects
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
PROJECTS_PID=$!

echo ""
echo "======================================"
echo "Servicios iniciados:"
echo "- MS-Leaders (PID: $LEADERS_PID): http://127.0.0.1:8001"
echo "- MS-Projects (PID: $PROJECTS_PID): http://127.0.0.1:8000"
echo "- Frontend: http://127.0.0.1:8000/static/index.html"
echo "======================================"
echo ""

# Esperar a que ambos procesos finalicen
wait $LEADERS_PID $PROJECTS_PID
