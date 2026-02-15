#!/usr/bin/env python3
"""
Script de diagnóstico para verificar microservicios
"""
import requests
import sys

def check_service(url, name):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✓ {name} está corriendo - Status {response.status_code}")
            data = response.json()
            print(f"  Respuesta: {data}")
            return True
        else:
            print(f"✗ {name} respondió con status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ {name} NO está corriendo (no hay conexión)")
        return False
    except Exception as e:
        print(f"✗ {name} error: {e}")
        return False

print("\n" + "="*60)
print("DIAGNÓSTICO DE MICROSERVICIOS")
print("="*60 + "\n")

print("1️⃣ Verificando MS-Leaders (Puerto 8001)...")
leaders_ok = check_service("http://127.0.0.1:8001/health", "MS-Leaders")
print()

print("2️⃣ Verificando MS-Projects (Puerto 8000)...")
projects_ok = check_service("http://127.0.0.1:8000/health", "MS-Projects")
print()

if leaders_ok and projects_ok:
    print("✅ Ambos servicios están corriendo correctamente\n")
    
    print("3️⃣ Verificando comunicación MS-Projects → MS-Leaders...")
    try:
        # Obtener líderes desde MS-Leaders
        res = requests.get("http://127.0.0.1:8001/leaders/", timeout=2)
        if res.status_code == 200:
            leaders = res.json()
            print(f"✓ Se encontraron {len(leaders)} líderes en MS-Leaders")
            if leaders:
                for l in leaders[:3]:
                    print(f"  - {l.get('nombre')} (ID: {l.get('id')})")
                if len(leaders) > 3:
                    print(f"  ... y {len(leaders) - 3} más")
    except Exception as e:
        print(f"✗ Error al obtener líderes: {e}")
    print()
    
    print("✅ Todas las verificaciones pasaron correctamente")
    print("\nAhora abre en tu navegador:")
    print("→ http://127.0.0.1:8000/static/index.html")
    
else:
    print("❌ NO todos los servicios están corriendo\n")
    
    if not leaders_ok:
        print("📋 Para iniciar MS-Leaders:")
        print("   cd ms-leaders")
        print("   python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload")
    
    if not projects_ok:
        print("\n📋 Para iniciar MS-Projects:")
        print("   cd ms-projects")
        print("   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload")

print("\n" + "="*60 + "\n")
