# 📋 GUÍA COMPLETA - TALLER UNIDAD 2: MICROSERVICIOS

## 🎯 Objetivo Cumplido

Transformar la aplicación monolítica de la **Unidad 1** en una arquitectura de **microservicios independientes** con comunicación REST entre servicios.

---

## ✅ REQUERIMIENTOS CUMPLIDOS

### 1. ✓ Descomposición de la Aplicación
- [x] Aplicación separada en 2 microservicios independientes
- [x] Responsabilidades claramente definidas:
  - **MS-Leaders:** Gestiona líderes
  - **MS-Projects:** Gestiona proyectos

### 2. ✓ Implementación de Microservicios
- [x] Ambos implementados en **FastAPI + Python**
- [x] Ejecutándose en puertos diferentes (8001 y 8000)
- [x] Controladores REST bien definidos
- [x] Independencia total entre servicios

### 3. ✓ Comunicación entre Microservicios
- [x] Comunicación sincrónica via **httpx (REST)**
- [x] MS-Projects consume datos de MS-Leaders
- [x] **Enriquecimiento de datos:** Proyectos incluyen detalles completos del líder
- [x] **Validación de integridad referencial:** No permite crear proyecto con líder inexistente

### 4. ✓ Pruebas
- [x] **Pruebas unitarias reutilizadas de Unidad 1**
- [x] **MS-Leaders:** 4 pruebas unitarias
  - `test_create_leader()`
  - `test_read_leaders()`
  - `test_get_leader_by_id()`
  - `test_delete_leader()`
- [x] **MS-Projects:** 3 pruebas unitarias
  - `test_read_projects_unitario()`
  - `test_delete_project_unitario()`
- [x] **Prueba de integración incluida:** `run_integration_test.py`

### 5. ✓ Monitorización (Actuator Equivalente)
- [x] Spring Boot Actuator implementado en FastAPI
- [x] Endpoints de health check en ambos servicios:
  - `GET /health` (básico)
  - `GET /health/status` (detallado)
- [x] Respuesta con estado del servicio y puerto

---

## 📁 ESTRUCTURA DEL PROYECTO

```
cur_semillero_v2_local/
│
├── ms-leaders/                          ⭐ MICROSERVICIO 1
│   ├── app/
│   │   ├── api/v1/leaders.py            Endpoints REST
│   │   ├── models/leader.py             Modelo de datos
│   │   ├── schemas/leader.py            Validación Pydantic
│   │   ├── crud/leader.py               Operaciones BD
│   │   ├── core/
│   │   │   ├── config.py                Configuración
│   │   │   └── database.py              Conexión SQLite
│   │   └── tests/
│   │       ├── conftest.py              Fixture de tests
│   │       └── test_leaders.py          Pruebas unitarias
│   ├── main.py                          Punto de entrada
│   ├── Dockerfile                       Para containerizar
│   ├── requirements.txt
│   └── pytest.ini
│
├── ms-projects/                         ⭐ MICROSERVICIO 2
│   ├── app/
│   │   ├── api/v1/projects.py           Endpoints REST
│   │   ├── models/project.py            Modelo de datos
│   │   ├── schemas/project.py           Validación Pydantic
│   │   ├── crud/project.py              Operaciones BD
│   │   ├── core/
│   │   │   ├── config.py                Configuración
│   │   │   ├── database.py              Conexión SQLite
│   │   │   └── external_services.py     Comunicación con MS-Leaders ⭐
│   │   └── tests/
│   │       ├── conftest.py              Fixture de tests
│   │       └── test_projects.py         Pruebas unitarias
│   ├── main.py                          Punto de entrada
│   ├── Dockerfile                       Para containerizar
│   ├── requirements.txt
│   └── pytest.ini
│
├── static/                              Frontend (sin cambios de ubicación)
│   ├── index.html                       Actualizado para consumir ambos MS
│   ├── script.js                        Actualizado: consume MS-Leaders + MS-Projects
│   ├── style.css
│   └── img/
│
├── ARQUITECTURA_MICROSERVICIOS.md       ⭐ Documento Técnico
├── README.md                            Instrucciones de inicio rápido
├── GUIA_COMPLETA.md                     Este documento
├── START-SERVICIOS.bat                  Script para iniciar en Windows
├── start-servicios.sh                   Script para iniciar en Linux/Mac
├── run_integration_test.py              Prueba de integración end-to-end
├── docker-compose-microservicios.yml    Docker Compose (opcional)
│
└── [archivos anteriores de Unidad 1]
```

---

## 🚀 CÓMO EJECUTAR

### Opción 1: Automática (Recomendada)

**Windows:**
```batch
START-SERVICIOS.bat
```

**Linux/Mac:**
```bash
chmod +x start-servicios.sh
./start-servicios.sh
```

### Opción 2: Manual (1 por terminal)

**Terminal 1:**
```bash
cd ms-leaders
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 2:**
```bash
cd ms-projects
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 3:**
Abrir navegador: `http://127.0.0.1:8000/static/index.html`

---

## 🧪 EJECUTAR PRUEBAS

### Pruebas Unitarias - MS-Leaders
```bash
cd ms-leaders
python -m pytest app/tests/test_leaders.py -v
```

**Resultado esperado:**
```
test_leaders.py::test_create_leader PASSED
test_leaders.py::test_read_leaders PASSED
test_leaders.py::test_get_leader_by_id PASSED
test_leaders.py::test_delete_leader PASSED

4 passed in 0.15s
```

### Pruebas Unitarias - MS-Projects
```bash
cd ms-projects
python -m pytest app/tests/test_projects.py -v
```

**Resultado esperado:**
```
test_projects.py::test_read_projects_unitario PASSED
test_projects.py::test_delete_project_unitario PASSED

2 passed in 0.10s
```

### Prueba de Integración (con ambos servicios corriendo)
```bash
python run_integration_test.py
```

**Demuestra:**
1. ✓ Ambos servicios disponibles
2. ✓ Crear líderes en MS-Leaders
3. ✓ Crear proyectos en MS-Projects
4. ✓ Obtener proyectos **enriquecidos** con datos de líderes
5. ✓ Validación de integridad referencial
6. ✓ Eliminar proyectos

---

## 📡 API ENDPOINTS

### MS-Leaders (Puerto 8001)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/leaders/` | Obtener todos los líderes |
| `GET` | `/leaders/{id}` | Obtener líder por ID |
| `POST` | `/leaders/` | Crear nuevo líder |
| `DELETE` | `/leaders/{id}` | Eliminar líder |
| `GET` | `/health` | Estado del servicio |

**Ejemplo - Crear líder:**
```bash
curl -X POST http://127.0.0.1:8001/leaders/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos",
    "email": "carlos@example.com",
    "departamento": "Desarrollo"
  }'
```

### MS-Projects (Puerto 8000)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/projects/` | Obtener proyectos (enriquecidos) |
| `POST` | `/projects/` | Crear nuevo proyecto |
| `DELETE` | `/projects/{id}` | Eliminar proyecto |
| `GET` | `/health` | Estado del servicio |

**Ejemplo - Crear proyecto:**
```bash
curl -X POST http://127.0.0.1:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Bio-fertilizante",
    "lider_id": 1,
    "descripcion": "Reducir uso de químicos",
    "fecha_inicio": "2024-03-01",
    "estado": true
  }'
```

---

## 🔄 COMUNICACIÓN ENTRE MICROSERVICIOS

### Flujo de Datos

```
Frontend (navegador)
    │
    ├─ GET /projects/  ──→  MS-Projects:8000
    │                           │
    │                           ├─ Obtiene proyectos de BD local
    │                           │
    │                           └─ Llama a MS-Leaders:8001
    │                               GET /leaders/1,2,3...
    │
    └─ ← Retorna proyectos ENRIQUECIDOS con datos de líderes
```

### Código de Integración (MS-Projects → MS-Leaders)

```python
# app/core/external_services.py
async def get_leader(leader_id: int):
    """Obtiene información de un líder desde MS-Leaders"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://127.0.0.1:8001/leaders/{leader_id}",
            timeout=5.0
        )
        if response.status_code == 200:
            return response.json()
        return None

# En el endpoint de proyectos
@router.get("/")
async def read_projects(db: Session = Depends(get_db)):
    projects = get_all(db)
    leaders = await get_all_leaders()  # Llama a MS-Leaders
    
    # Enriquece los datos
    result = []
    for project in projects:
        result.append({
            **project.dict(),
            "lider": leaders_map.get(project.lider_id)
        })
    return result
```

---

## 💡 DIFERENCIAS MONOLITO vs MICROSERVICIOS

| Aspecto | Monolito | Microservicios |
|--------|----------|----------------|
| **Despliegue** | Todo o nada | Un servicio a la vez |
| **Escalabilidad** | Apagón total | Un servicio puede caer |
| **Desarrollo** | Equipo centralizado | Equipos independientes |
| **BD** | Una sola | Una por servicio |
| **Performance** | Rápido (no hay red) | Más lento (llamadas HTTP) |
| **Mantenimiento** | Difícil | Fácil |
| **Testing** | Integrado (lento) | Unitario (rápido) |

---

## 📊 EVIDENCIAS DE FUNCIONAMIENTO

### 1. Health Checks
```bash
curl http://127.0.0.1:8001/health
# {"status": "up", "service": "ms-leaders", "port": 8001}

curl http://127.0.0.1:8000/health
# {"status": "up", "service": "ms-projects", "port": 8000}
```

### 2. Pruebas Unitarias Pasando
```
ms-leaders/app/tests/test_leaders.py::test_create_leader PASSED
ms-leaders/app/tests/test_leaders.py::test_read_leaders PASSED
ms-leaders/app/tests/test_leaders.py::test_get_leader_by_id PASSED
ms-leaders/app/tests/test_leaders.py::test_delete_leader PASSED

ms-projects/app/tests/test_projects.py::test_read_projects_unitario PASSED
ms-projects/app/tests/test_projects.py::test_delete_project_unitario PASSED
```

### 3. Consumo de Servicios desde Frontend
El `script.js` obtiene:
- Líderes desde `http://127.0.0.1:8001/leaders/`
- Proyectos desde `http://127.0.0.1:8000/projects/`
- Los proyectos ya están enriquecidos con datos del líder

### 4. Comunicación Inter-Servicios
MS-Projects valida líderes llamando a MS-Leaders antes de crear proyectos

---

## 🎓 CONCEPTOS DEMOSTRADOS

✓ **SRP (Single Responsibility Principle):** Cada servicio tiene UNA responsabilidad  
✓ **Autonomía:** Servicios independientes con BDs separadas  
✓ **API REST:** Comunicación sincrona via HTTP  
✓ **Async/Await:** Llamadas no bloqueantes con httpx  
✓ **Validación de Datos:** Pydantic en request y response  
✓ **Health Checks:** Monitorización de servicios  
✓ **Testing:** Pruebas unitarias e integración  
✓ **Independencia de Despliegue:** Cada servicio en puerto diferente  

---

## 🔧 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| "Error 404: Líder no encontrado" | Verificar que MS-Leaders esté en puerto 8001 |
| "No responde el servidor" | Verificar que ambos servicios estén corriendo |
| "Puerto ya en uso" | Cambiar en `app/core/config.py` y `script.js` |
| "BD no está actualizada" | Ejecutar primero: `run_integration_test.py` |

---

## 📦 ENTREGABLES

- [x] **Código fuente:** Dos microservicios independientes
- [x] **Documentación técnica:** ARQUITECTURA_MICROSERVICIOS.md
- [x] **Pruebas:** Unitarias e integración
- [x] **Frontend actualizado:** Consume ambos MS
- [x] **Scripts de inicio:** Windows y Linux/Mac
- [x] **Ejemplos de API:** Documentada en README
- [x] **Docker support:** Dockerfile y docker-compose incluidos

---

## 🏁 CONCLUSIÓN

Se ha completado exitosamente la transformación de una arquitectura **monolítica** a **microservicios**, cumpliendo con todos los requerimientos del taller:

✅ Descomposición clara en 2 servicios  
✅ Comunicación REST entre ellos  
✅ Pruebas unitarias reutilizadas  
✅ Health checks configurados  
✅ Frontend integrado  
✅ Documentación completa  

---

**Studentr:** Estudiante  
**Institución:** Universidad de la Remington  
**Fecha:** 14 de febrero de 2026  
**Semestre:** 2026-1  
**Asignatura:** Lenguaje de Programación Avanzado II
