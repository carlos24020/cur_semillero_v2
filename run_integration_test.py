"""
PRUEBA DE INTEGRACIÓN ENTRE MICROSERVICIOS

Este script demuestra cómo MS-Projects consume datos de MS-Leaders.

Ejecutar con ambos servicios corriendo:
    Terminal 1: cd ms-leaders && python -m uvicorn main:app --port 8001
    Terminal 2: cd ms-projects && python -m uvicorn main:app --port 8000
    Terminal 3: python run_integration_test.py
"""

import requests
import json
from datetime import date

BASE_LEADERS = "http://127.0.0.1:8001"
BASE_PROJECTS = "http://127.0.0.1:8000"

def test_integracion_completa():
    print("\n" + "="*60)
    print("PRUEBA DE INTEGRACIÓN - MS-LEADERS + MS-PROJECTS")
    print("="*60 + "\n")
    
    # 1. Verificar que ambos servicios estén disponibles
    print("1️⃣ Verificando disponibilidad de servicios...")
    try:
        r1 = requests.get(f"{BASE_LEADERS}/health", timeout=2)
        r2 = requests.get(f"{BASE_PROJECTS}/health", timeout=2)
        print(f"   ✓ MS-Leaders: {r1.status_code}")
        print(f"   ✓ MS-Projects: {r2.status_code}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # 2. Crear algunos líderes en MS-Leaders
    print("2️⃣ Creando líderes en MS-Leaders...")
    leaders_data = [
        {"nombre": "Carlos", "email": "carlos@example.com", "departamento": "Desarrollo"},
        {"nombre": "Ana", "email": "ana@example.com", "departamento": "Diseño"},
        {"nombre": "Pedro", "email": "pedro@example.com", "departamento": "QA"},
    ]
    
    leader_ids = []
    for leader in leaders_data:
        r = requests.post(f"{BASE_LEADERS}/leaders/", json=leader)
        if r.status_code == 201:
            lid = r.json()["id"]
            leader_ids.append(lid)
            print(f"   ✓ Líder '{leader['nombre']}' creado (ID: {lid})")
    print()
    
    # 3. Crear proyectos en MS-Projects (referenciando líderes de MS-Leaders)
    print("3️⃣ Creando proyectos en MS-Projects...")
    projects_data = [
        {
            "titulo": "Bio-fertilizante",
            "lider_id": leader_ids[0],
            "descripcion": "Reducir uso de químicos",
            "fecha_inicio": "2024-03-01",
            "estado": True
        },
        {
            "titulo": "Anime Studio",
            "lider_id": leader_ids[1],
            "descripcion": "Plataforma de streaming",
            "fecha_inicio": "2024-02-15",
            "estado": True
        },
        {
            "titulo": "Música Digital",
            "lider_id": leader_ids[2],
            "descripcion": "App de reproducción de música",
            "fecha_inicio": "2024-01-20",
            "estado": True
        },
    ]
    
    project_ids = []
    for project in projects_data:
        r = requests.post(f"{BASE_PROJECTS}/projects/", json=project)
        if r.status_code == 201:
            pid = r.json()["id"]
            project_ids.append(pid)
            print(f"   ✓ Proyecto '{project['titulo']}' creado (ID: {pid})")
        else:
            print(f"   ✗ Error al crear proyecto: {r.text}")
    print()
    
    # 4. Obtener proyectos enriquecidos (con datos de líderes)
    print("4️⃣ Obteniendo proyectos enriquecidos de MS-Projects...")
    r = requests.get(f"{BASE_PROJECTS}/projects/")
    
    if r.status_code == 200:
        projects = r.json()
        print(f"   Total de proyectos: {len(projects)}\n")
        
        for p in projects:
            print(f"   📌 Proyecto #{p['id']}: {p['titulo']}")
            print(f"      - Líder: {p['lider']['nombre']} ({p['lider']['departamento']})")
            print(f"      - Email: {p['lider']['email']}")
            print(f"      - Descripción: {p['descripcion']}")
            print(f"      - Estado: {'Activo' if p['estado'] else 'Finalizado'}")
            print()
    else:
        print(f"   ✗ Error: {r.text}")
        return False
    
    # 5. Validación de integridad referencial
    print("5️⃣ Validando integridad referencial...")
    
    # Intentar crear un proyecto con líder inexistente
    invalid_project = {
        "titulo": "Proyecto Inválido",
        "lider_id": 9999,
        "descripcion": "Este debe fallar",
        "fecha_inicio": "2024-01-01",
        "estado": True
    }
    
    r = requests.post(f"{BASE_PROJECTS}/projects/", json=invalid_project)
    if r.status_code == 404:
        print(f"   ✓ Validación correcta: No permite crear proyecto con líder inexistente")
        print(f"     Error: {r.json()['detail']}\n")
    else:
        print(f"   ✗ Validación falló: Permitió crear proyecto con líder inválido\n")
    
    # 6. Eliminar un proyecto
    print("6️⃣ Eliminando un proyecto...")
    if project_ids:
        r = requests.delete(f"{BASE_PROJECTS}/projects/{project_ids[0]}")
        if r.status_code == 204:
            print(f"   ✓ Proyecto #{project_ids[0]} eliminado correctamente\n")
        else:
            print(f"   ✗ Error al eliminar: {r.text}\n")
    
    # 7. Verificar proyectos finales
    print("7️⃣ Verificando proyectos restantes...")
    r = requests.get(f"{BASE_PROJECTS}/projects/")
    if r.status_code == 200:
        projects = r.json()
        print(f"   Total de proyectos restantes: {len(projects)}\n")
    
    print("="*60)
    print("✅ PRUEBA DE INTEGRACIÓN COMPLETADA")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    test_integracion_completa()
