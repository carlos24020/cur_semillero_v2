#!/usr/bin/env python3
"""
Script de prueba para verificar que el UI de creación de líderes funciona correctamente.
Prueba:
1. Obtener lista de líderes actual
2. Crear un nuevo líder
3. Verificar que fue creado
4. Listar todos los líderes
"""

import httpx
import json
import asyncio
from datetime import datetime

# Configuración
MS_LEADERS_URL = "http://127.0.0.1:8001/leaders"

async def main():
    async with httpx.AsyncClient(timeout=10) as client:
        print("=" * 60)
        print("PRUEBA: Sistema de Creación de Líderes vía Web UI")
        print("=" * 60)
        
        # 1. Obtener líderes actuales
        print("\n1️⃣  Obteniendo líderes actuales...")
        try:
            res = await client.get(MS_LEADERS_URL + "/")
            res.raise_for_status()
            lideres_actuales = res.json()
            print(f"   ✅ Se encontraron {len(lideres_actuales)} líderes")
            for l in lideres_actuales:
                print(f"      - {l['nombre']} ({l['email']})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # 2. Crear un nuevo líder
        print("\n2️⃣  Creando nuevo líder...")
        nuevo_lider = {
            "nombre": f"TestLider_{datetime.now().timestamp()}",
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "departamento": "Testing"
        }
        
        try:
            res = await client.post(
                MS_LEADERS_URL + "/",
                json=nuevo_lider,
                headers={"Content-Type": "application/json"}
            )
            res.raise_for_status()
            lider_creado = res.json()
            print(f"   ✅ Líder creado exitosamente")
            print(f"      - ID: {lider_creado['id']}")
            print(f"      - Nombre: {lider_creado['nombre']}")
            print(f"      - Email: {lider_creado['email']}")
            print(f"      - Departamento: {lider_creado['departamento']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # 3. Obtener líderes nuevamente
        print("\n3️⃣  Verificando lista actualizada de líderes...")
        try:
            res = await client.get(MS_LEADERS_URL + "/")
            res.raise_for_status()
            lideres_nuevos = res.json()
            print(f"   ✅ Ahora hay {len(lideres_nuevos)} líderes:")
            for l in lideres_nuevos:
                marcador = " ← NUEVO" if l['id'] == lider_creado['id'] else ""
                print(f"      - {l['nombre']} ({l['email']}){marcador}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # 4. Obtener un líder específico
        print(f"\n4️⃣  Obteniendo líder específico (ID: {lider_creado['id']})...")
        try:
            res = await client.get(f"{MS_LEADERS_URL}/{lider_creado['id']}")
            res.raise_for_status()
            lider = res.json()
            print(f"   ✅ Líder obtenido:")
            print(f"      {json.dumps(lider, indent=6)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # 5. Health check
        print("\n5️⃣  Verificando salud del servicio MS-Leaders...")
        try:
            res = await client.get("http://127.0.0.1:8001/leaders/health/status")
            res.raise_for_status()
            health = res.json()
            print(f"   ✅ Servicio sano: {health}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA COMPLETADA")
        print("=" * 60)
        print("\n📝 Próximos pasos:")
        print("1. Abre http://127.0.0.1:8000 en tu navegador")
        print("2. Haz clic en 'Líderes' en la navegación")
        print("3. Completa el formulario con:")
        print(f"   - Nombre: {nuevo_lider['nombre']}")
        print(f"   - Email: {nuevo_lider['email']}")
        print(f"   - Departamento: {nuevo_lider['departamento']}")
        print("4. Haz clic en 'Crear Líder'")
        print("5. Verifica que aparezca en la tabla de abajo")
        print("6. Ve a 'Registrar' y verifica que aparezca el líder en el dropdown")

if __name__ == "__main__":
    asyncio.run(main())
