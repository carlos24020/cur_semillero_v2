#!/usr/bin/env python3
"""
Script para crear líderes de prueba en MS-Leaders
Ejecutar después de que MS-Leaders esté corriendo en puerto 8001
"""

import requests
import json

MS_LEADERS_URL = "http://127.0.0.1:8001"

# Líderes de prueba (del proyecto original)
LIDERES_PRUEBA = [
    {"nombre": "carlos", "email": "carlos@uniremington.edu.co", "departamento": "Desarrollo"},
    {"nombre": "jose", "email": "jose@uniremington.edu.co", "departamento": "Diseño"},
    {"nombre": "mello", "email": "mello@uniremington.edu.co", "departamento": "QA"},
    {"nombre": "Ana Gómez", "email": "ana@uniremington.edu.co", "departamento": "Producto"},
    {"nombre": "Pedro López", "email": "pedro@uniremington.edu.co", "departamento": "Backend"},
]

def crear_lideres():
    print("\n" + "="*60)
    print("Inserting Test Leaders into MS-Leaders")
    print("="*60 + "\n")
    
    # Verificar que MS-Leaders esté disponible
    try:
        r = requests.get(f"{MS_LEADERS_URL}/health", timeout=2)
        print(f"✓ MS-Leaders disponible: {r.status_code}\n")
    except Exception as e:
        print(f"✗ Error: MS-Leaders no responde en {MS_LEADERS_URL}")
        print(f"  Asegúrate de que esté corriendo: cd ms-leaders && python -m uvicorn main:app --port 8001")
        return False
    
    # Obtener líderes existentes
    try:
        r = requests.get(f"{MS_LEADERS_URL}/leaders/")
        lideres_existentes = r.json()
        print(f"Líderes existentes: {len(lideres_existentes)}\n")
        
        if lideres_existentes:
            print("Líderes actuales:")
            for l in lideres_existentes:
                print(f"  - {l['nombre']}")
            print("\n✓ Ya hay líderes. No es necesario agregar más.\n")
            return True
    except Exception as e:
        print(f"Error al obtener líderes: {e}")
    
    # Crear nuevos líderes
    print("Creando líderes de prueba...\n")
    
    líderes_creados = 0
    for lider in LIDERES_PRUEBA:
        try:
            r = requests.post(f"{MS_LEADERS_URL}/leaders/", json=lider, timeout=5)
            
            if r.status_code == 201:
                data = r.json()
                print(f"✓ Líder creado: {lider['nombre']} (ID: {data['id']})")
                líderes_creados += 1
            else:
                print(f"✗ Error al crear {lider['nombre']}: {r.status_code}")
                print(f"  Respuesta: {r.text}")
        except Exception as e:
            print(f"✗ Error de conexión para {lider['nombre']}: {e}")
    
    print(f"\n✓ Total de líderes creados: {líderes_creados}")
    print("\n" + "="*60)
    print("¡Ahora abre el navegador y prueba a registrar un proyecto!")
    print("="*60 + "\n")
    
    return líderes_creados > 0

if __name__ == "__main__":
    crear_lideres()
