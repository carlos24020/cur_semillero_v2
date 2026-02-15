#!/usr/bin/env python3
"""Script para probar el DELETE directamente"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Primero obtener todos los proyectos
print("1️⃣ Obteniendo lista de proyectos...\n")
res = requests.get(f"{BASE_URL}/projects/")
print(f"Status: {res.status_code}")
projects = res.json()
print(f"Proyectos encontrados: {len(projects)}\n")

if projects:
    # Intentar eliminar el primero
    project_id = projects[0]["id"]
    print(f"2️⃣ Intentando eliminar proyecto ID {project_id}...\n")
    
    delete_res = requests.delete(f"{BASE_URL}/projects/{project_id}")
    print(f"Status: {delete_res.status_code}")
    
    if delete_res.status_code == 404:
        print(f"❌ Error 404: {delete_res.json()}")
    elif delete_res.status_code == 204:
        print("✅ Eliminado correctamente")
    else:
        print(f"Response: {delete_res.text}")
        
print("\n✅ Test completado.\n")
