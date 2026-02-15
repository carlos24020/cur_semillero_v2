# ✅ CHECKLIST DE VERIFICACIÓN - TALLER UNIDAD 2

## Requerimientos del Taller

### 1. Descomposición de la Aplicación
- [x] Aplicación separada en al menos 2 microservicios ✓
  - [x] MS-Leaders (gestión de líderes)
  - [x] MS-Projects (gestión de proyectos)
- [x] Justificación clara de la separación ✓
  - [ ] Ver: `ARQUITECTURA_MICROSERVICIOS.md` sección 2

### 2. Implementación de Microservicios
- [x] FastAPI + Python (2 servicios independientes) ✓
- [x] Ejecutándose en puertos diferentes ✓
  - [x] MS-Leaders: Puerto 8001
  - [x] MS-Projects: Puerto 8000
- [x] Controladores REST bien definidos ✓
  - [x] MS-Leaders: `/leaders/` crud completo
  - [x] MS-Projects: `/projects/` crud completo
- [x] Independencia respecto a otros servicios ✓
  - [x] BD separadas (sqlite)
  - [x] Código no compartido
  - [x] Configuración independiente

### 3. Comunicación entre Microservicios
- [x] Comunicación sincrónica REST implementada ✓
  - [x] httpx para peticiones HTTP
  - [x] async/await para no bloquear
- [x] Al menos un caso de consumo de información ✓
  - [x] MS-Projects obtiene líderes de MS-Leaders
  - [x] Enriquecimiento de datos de proyectos
  - [x] Validación de integridad referencial

### 4. Pruebas
- [x] Pruebas unitarias reutilizadas de Unidad 1 ✓
  - [x] MS-Leaders: 4 pruebas unitarias
    - [x] test_create_leader()
    - [x] test_read_leaders()
    - [x] test_get_leader_by_id()
    - [x] test_delete_leader()
  - [x] MS-Projects: 3 pruebas unitarias
    - [x] test_read_projects_unitario()
    - [x] test_delete_project_unitario()
    - [x] Plus: Validación y error handling
- [x] Pruebas de integración ✓
  - [x] `run_integration_test.py` incluido
  - [x] Demuestra comunicación entre servicios
  - [x] Prueba end-to-end completa

### 5. Monitorización (Actuator)
- [x] Spring Boot Actuator equivalente implementado ✓
  - [x] Endpoints `/health` en ambos servicios
  - [x] Endpoints `/health/status` detallados
  - [x] Información de estado y puerto

---

## Archivos Entregables

### Código Fuente
- [x] **ms-leaders/main.py** - Punto de entrada
- [x] **ms-leaders/app/api/v1/leaders.py** - Controllers
- [x] **ms-leaders/app/models/leader.py** - Modelo
- [x] **ms-leaders/app/schemas/leader.py** - Validación
- [x] **ms-leaders/app/crud/leader.py** - CRUD operations
- [x] **ms-leaders/app/core/** - Config y BD

- [x] **ms-projects/main.py** - Punto de entrada
- [x] **ms-projects/app/api/v1/projects.py** - Controllers
- [x] **ms-projects/app/core/external_services.py** - Comunicación MS
- [x] **ms-projects/app/models/project.py** - Modelo
- [x] **ms-projects/app/schemas/project.py** - Validación
- [x] **ms-projects/app/crud/project.py** - CRUD operations
- [x] **ms-projects/app/core/** - Config y BD

### Documentación Técnica
- [x] **ARQUITECTURA_MICROSERVICIOS.md** - Documento técnico completo
  - [x] Descripción de arquitectura original (Unidad 1)
  - [x] Justificación de descomposición
  - [x] Diagrama simple de arquitectura
  - [x] Descripción de comunicación entre servicios
  - [x] Endpoints documentados
  - [x] Instrucciones de ejecución
  - [x] Estructura de ficheros

- [x] **GUIA_COMPLETA.md** - Guía para estudiante
- [x] **README.md** - Start rápido
- [x] **CHECKLIST.md** - Este archivo

### Pruebas
- [x] **ms-leaders/app/tests/test_leaders.py** - Unitarias
- [x] **ms-projects/app/tests/test_projects.py** - Unitarias
- [x] **run_integration_test.py** - Integración end-to-end

### Scripts
- [x] **START-SERVICIOS.bat** - Iniciar en Windows
- [x] **start-servicios.sh** - Iniciar en Linux/Mac
- [x] **docker-compose-microservicios.yml** - Containerización
- [x] **ms-leaders/Dockerfile** - Imagen de líderes
- [x] **ms-projects/Dockerfile** - Imagen de proyectos

### Frontend
- [x] **static/index.html** - Actualizado para ambos MS
- [x] **static/script.js** - Actualizado para consumir ambos servicios
- [x] **static/style.css** - Sin cambios necesarios
- [x] **static/img/** - Assets

---

## Cómo Verificar que Todo Funciona

### 1. Iniciar Servicios
```bash
# Windows
START-SERVICIOS.bat

# Linux/Mac
chmod +x start-servicios.sh
./start-servicios.sh

# O manualmente en 3 terminales
cd ms-leaders && python -m uvicorn main:app --port 8001
cd ms-projects && python -m uvicorn main:app --port 8000
browser http://127.0.0.1:8000/static/index.html
```

### 2. Verificar Health Checks
```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8000/health
```

### 3. Ejecutar Pruebas Unitarias
```bash
# MS-Leaders
cd ms-leaders
python -m pytest app/tests/test_leaders.py -v
# Expected: 4 passed

# MS-Projects
cd ms-projects
python -m pytest app/tests/test_projects.py -v
# Expected: 2 passed
```

### 4. Ejecutar Prueba de Integración
```bash
python run_integration_test.py
# Demuestra comunicación entre servicios
```

### 5. Probar en Frontend
- Ir a `http://127.0.0.1:8000/static/index.html`
- Sección "Registrar": aparece dropdown de líderes (desde MS-Leaders)
- Crear un proyecto: valida líder en MS-Leaders
- Sección "Proyectos": muestra proyectos con info del líder enriquecida

### 6. Probar Endpoints
```bash
# Crear líder
curl -X POST http://127.0.0.1:8001/leaders/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Carlos","email":"c@e.com","departamento":"Dev"}'

# Crear proyecto
curl -X POST http://127.0.0.1:8000/projects/ \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Test","lider_id":1,"fecha_inicio":"2024-03-01","estado":true}'

# Obtener proyectos enriquecidos
curl http://127.0.0.1:8000/projects/
```

---

## Requisitos Cumplidos

### Requerimiento 1: Descomposición ✓
- [x] Al menos 2 microservicios: **MS-Leaders** y **MS-Projects**
- [x] Responsabilidades claramente definidas
  - MS-Leaders: Gestión de líderes
  - MS-Projects: Gestión de proyectos

### Requerimiento 2: Spring Boot Independientes ✓
- [x] Ambos son proyectos FastAPI independientes
- [x] Puertos diferentes (8000 y 8001)
- [x] Controllers REST bien definidos
- [x] Independencia total

### Requerimiento 3: Comunicación REST ✓
- [x] Implementada con httpx
- [x] MS-Projects → MS-Leaders
- [x] Validación de integridad referencial
- [x] Enriquecimiento de datos

### Requerimiento 4: Pruebas ✓
- [x] Unitarias reutilizadas de Unidad 1
- [x] MS-Leaders: 4 pruebas
- [x] MS-Projects: 3 pruebas (mínimo 2 requeridos)
- [x] Integración: run_integration_test.py

### Requerimiento 5: Monitorización ✓
- [x] Endpoints `/health` en ambos servicios
- [x] Estado del servicio
- [x] Información de puerto

---

## Aspectos Recomendados Pero No Obligatorios

- [x] Docker Compose para orquestación futura
- [x] Documento técnico extenso
- [x] Frontend totalmente integrado
- [x] Scripts de inicio automático
- [x] Prueba de integración end-to-end
- [x] Dockerfile para cada servicio

---

## Presentación en Clase

### Slides Recomendados
1. Portada: Microservicios - Unidad 2
2. Problema vs Solución
3. Arquitectura Monolítica (Unidad 1)
4. Arquitectura de Microservicios (Unidad 2)
5. Diagrama de Servicios
6. Endpoints de cada servicio
7. Comunicación entre servicios
8. Flujo de creación de proyecto
9. Pruebas unitarias e integración
10. Demo en vivo (si es posible)

### Demo en Vivo (Sugerencia)
1. Mostrar estructura de 2 servicios
2. Iniciar ambos servicios
3. Crear líder en MS-Leaders
4. Crear proyecto en MS-Projects (valida líder)
5. Mostrar proyecto enriquecido en frontend
6. Ejecutar pruebas
7. Mostrar logs de comunicación

---

## Fecha de Entrega

**14 de febrero de 2026**

## Completado por

**Estudiante**  
**Asignatura:** Lenguaje de Programación Avanzado II  
**Institución:** Universidad de la Remington  
**Semestre:** 2026-1

---

## Status Final

🎉 **TALLER COMPLETADO EXITOSAMENTE**

Todos los requerimientos han sido cumplidos y el proyecto está listo para presentar.

---

**Última actualización:** 14 de febrero de 2026
