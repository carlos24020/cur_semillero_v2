# ARQUITECTURA DE MICROSERVICIOS - CUR SEMILLERO

## Documento Técnico - Unidad 2

---

### 1. DESCRIPCIÓN DE LA ARQUITECTURA ORIGINAL (Unidad 1)

La aplicación desarrollada en la Unidad 1 era una solución **monolítica** construida con:
- **Backend:** FastAPI (Python) + SQLAlchemy
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Base de Datos:** SQLite
- **Puerto:** 8000 (único)

#### Estructura Monolítica Anterior
```
cur_semillero_v2_local/
├── app/
│   ├── api/v1/projects.py      # Controlador
│   ├── models/project.py        # Modelo de datos
│   ├── schemas/project.py       # Validación
│   ├── crud/project.py          # Lógica de negocio
│   ├── core/                    # Configuración
│   ├── tests/                   # Pruebas
│   └── static/                  # Frontend
├── main.py
└── requirements.txt
```

**Limitaciones Identificadas:**
- ✗ Todos los servicios acoplados en una sola aplicación
- ✗ Escalabilidad limitada
- ✗ Reutilización de BD en un único archivo
- ✗ Difícil de mantener y actualizar componentes individuales

---

### 2. JUSTIFICACIÓN DE LA DESCOMPOSICIÓN EN MICROSERVICIOS

Se identificaron dos **responsabilidades bien definidas** que justifican la separación:

#### **Problema x' Solución**
| Aspecto | Problema | Solución |
|--------|---------|----------|
| **Gestión de Líderes** | Acoplada con Proyectos | Microservicio Independiente |
| **Gestión de Proyectos** | Dependía de "string" de líderes | Consumidor REST del MS-Leaders |
| **Escalabilidad** | Monolito rígido | Escalar servicios por demanda |
| **Mantenimiento** | Cambios afectan todo | Cambios aislados por servicio |
| **Pruebas** | Integradas (lento) | Independientes y paralelas |

#### **Criterios de Descomposición**
1. **Responsabilidad Única (SRP):** Cada microservicio hace UNA cosa bien
2. **Autonomía:** No comparten BD, código o dependencias
3. **Independencia de Despliegue:** Se actualizan sin afectar otros servicios
4. **Comunicación Clara:** APIs REST bien definidas

---

### 3. DIAGRAMA DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────┐
│                          FRONTEND                                │
│                    (Static Web - port 8000)                      │
│                  HTML5 + CSS3 + JavaScript                      │
└────────────────┬──────────────────────────────┬──────────────────┘
                 │                              │
                 v                              v
        ┌─────────────────┐        ┌──────────────────────┐
        │   MS-PROJECTS   │        │   MS-LEADERS         │
        │   (Puerto 8000) │        │   (Puerto 8001)      │
        │                 │        │                      │
        ├─────────────────┤        ├──────────────────────┤
        │ GET /projects/  │        │ GET /leaders/        │
        │ POST /projects/ │        │ GET /leaders/{id}    │
        │ DELETE /pr...   │        │ POST /leaders/       │
        │ GET /health     │        │ DELETE /leaders/...  │
        │                 │        │ GET /health          │
        ├─────────────────┤        ├──────────────────────┤
        │ BD: SQLite      │        │ BD: SQLite           │
        │ models:         │        │ models:              │
        │   - Project     │        │   - Leader           │
        └────────┬────────┘        └──────────────────────┘
                 │                         ^
                 │ Consume Data            │ Proporciona Dados
                 └─────────────────────────┘
                    REST API (httpx)

┌─────────────────────────────────────────────────────────────────┐
│                 DOCKER COMPOSE (Opcional)                       │
│    - Container MS-Leaders                                      │
│    - Container MS-Projects                                     │
│    - Container SQLite (volúmenes persistentes)                │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4. ESPECIFICACIÓN DE MICROSERVICIOS

#### **4.1 MS-LEADERS (Microservicio 1)**

**Responsabilidad:** Gestionar líderes/usuarios del sistema

**Puertos:** 8001

**Endpoints:**
```http
GET    /leaders/                 # Obtener todos los líderes
GET    /leaders/{id}             # Obtener líder por ID
POST   /leaders/                 # Crear nuevo líder
DELETE /leaders/{id}             # Eliminar líder
GET    /health                   # Health check
```

**Modelo de Datos:**
```python
class Leader(Base):
    __tablename__ = "leaders"
    id: int (PK)
    nombre: str (unique, required)
    email: str (optional)
    departamento: str (optional)
```

**Base de Datos:** `ms_leaders.db` (SQLite independiente)

**Dependencias:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0

---

#### **4.2 MS-PROJECTS (Microservicio 2)**

**Responsabilidad:** Gestionar proyectos y consumir datos de líderes del MS-Leaders

**Puertos:** 8000

**Endpoints:**
```http
GET    /projects/                # Obtener todos los proyectos (enriquecidos con datos de líderes)
POST   /projects/                # Crear nuevo proyecto (valida líder en MS-Leaders)
DELETE /projects/{id}            # Eliminar proyecto
GET    /health                   # Health check
```

**Modelo de Datos:**
```python
class Project(Base):
    __tablename__ = "projects"
    id: int (PK)
    titulo: str (required)
    lider_id: int (FK - referencia a MS-Leaders)
    descripcion: str (optional)
    fecha_inicio: date (required)
    estado: bool (default=True)
```

**Base de Datos:** `ms_projects.db` (SQLite independiente)

**Dependencias:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- httpx 0.25.1 (para llamadas REST)
- Pydantic 2.5.0

**URL de MS-Leaders:** `http://127.0.0.1:8001`

---

### 5. COMUNICACIÓN ENTRE MICROSERVICIOS

#### **5.1 Tipo de Comunicación: REST Sincrónica**

El MS-Projects consume información del MS-Leaders mediante peticiones HTTP REST síncronas.

#### **5.2 Caso de Uso: Enriquecimiento de Datos**

**Flujo de Lectura de Proyectos:**

```javascript
// 1. Frontend solicita proyectos
GET /projects/

// 2. MS-Projects obtiene proyectos de su BD
projects = [
  {id: 1, titulo: "Musical", lider_id: 1, ...},
  {id: 2, titulo: "Anime", lider_id: 2, ...}
]

// 3. MS-Projects llama a MS-Leaders para obtener detalles
GET http://127.0.0.1:8001/leaders/1
GET http://127.0.0.1:8001/leaders/2

// 4. Enriquece los datos (agrega objeto lider completo)
{
  id: 1,
  titulo: "Musical",
  lider_id: 1,
  lider: {
    id: 1,
    nombre: "Carlos",
    email: "carlos@example.com",
    departamento: "Desarrollo"
  }
}

// 5. Retorna al frontend datos completos
```

**Implementación en Python:**
```python
async def read_projects(db: Session = Depends(get_db)):
    projects = get_all(db)
    leaders_map = {}
    
    # Obtiene todos los líderes de MS-Leaders
    leaders = await get_all_leaders()
    for leader in leaders:
        leaders_map[leader["id"]] = leader
    
    # Enriquece los proyectos
    result = []
    for project in projects:
        project_dict = {
            **project.dict(),
            "lider": leaders_map.get(project.lider_id)
        }
        result.append(project_dict)
    
    return result
```

#### **5.3 Validación de Integridad Referencial**

Cuando se crea un proyecto, MS-Projects valida que el líder exista en MS-Leaders:

```python
@router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    # Valida que el líder exista en ms-leaders
    leader = await get_leader(proj.lider_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Líder no encontrado en ms-leaders")
    
    return create(db, proj)
```

---

### 6. ESTRATEGIA DE PRUEBAS

#### **6.1 Pruebas Unitarias**

**MS-Leaders:** (2 pruebas por servicio)
```python
test_create_leader()          # Verifica creación de líder
test_read_leaders()           # Verifica lectura de líderes
test_get_leader_by_id()       # Verifica obtención por ID
test_delete_leader()          # Verifica eliminación
```

**MS-Projects:** (2 pruebas por servicio)
```python
test_read_projects_unitario()         # Lectura de proyectos
test_delete_project_unitario()        # Eliminación de proyectos
```

#### **6.2 Pruebas de Integración**

**Nota:** Las pruebas de integración validarán la comunicación entre servicios cuando ambos están corriendo:

```bash
# Terminal 1
python -m uvicorn ms_leaders.main:app --port 8001

# Terminal 2
python -m pytest ms_projects/app/tests/test_integration.py -v
```

#### **6.3 Ejecución de Pruebas**

```bash
# MS-Leaders
cd ms-leaders
pip install -r requirements.txt
python -m pytest app/tests/test_leaders.py -v

# MS-Projects
cd ../ms-projects
pip install -r requirements.txt
python -m pytest app/tests/test_projects.py -v
```

---

### 7. MONITORIZACIÓN (ACTUATOR)

Ambos microservicios incluyen endpoints de health check para monitorización:

#### **Endpoints de Salud**

```http
GET /health              # Health check básico
GET /health/status       # Estado detallado del servicio
```

**Ejemplo de Respuesta:**
```json
{
  "status": "up",
  "service": "ms-projects",
  "port": 8000
}
```

---

### 8. INSTRUCCIONES DE EJECUCIÓN

#### **8.1 Instalación de Dependencias**

```bash
# MS-Leaders
cd ms-leaders
pip install -r requirements.txt

# MS-Projects
cd ../ms-projects
pip install -r requirements.txt
```

#### **8.2 Iniciar los Servicios**

**En Windows:**
```bash
START-SERVICIOS.bat
```

**En Linux/Mac:**
```bash
chmod +x start-servicios.sh
./start-servicios.sh
```

**O Manualmente (3 terminales):**

**Terminal 1 - MS-Leaders:**
```bash
cd ms-leaders
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 2 - MS-Projects:**
```bash
cd ms-projects
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 3 - Visualizar en el navegador:**
```
http://127.0.0.1:8000/static/index.html
```

#### **8.3 Verificar que Funciona**

```bash
# Verificar health de MS-Leaders
curl http://127.0.0.1:8001/health

# Verificar health de MS-Projects
curl http://127.0.0.1:8000/health

# Obtener líderes
curl http://127.0.0.1:8001/leaders/

# Obtener proyectos
curl http://127.0.0.1:8000/projects/
```

---

### 9. ESTRUCTURA DE FICHEROS

```
cur_semillero_v2_local/
├── ms-leaders/
│   ├── app/
│   │   ├── api/v1/leaders.py
│   │   ├── core/config.py
│   │   ├── core/database.py
│   │   ├── models/leader.py
│   │   ├── schemas/leader.py
│   │   ├── crud/leader.py
│   │   └── tests/
│   │       ├── conftest.py
│   │       └── test_leaders.py
│   ├── main.py
│   └── requirements.txt
│
├── ms-projects/
│   ├── app/
│   │   ├── api/v1/projects.py
│   │   ├── core/config.py
│   │   ├── core/database.py
│   │   ├── core/external_services.py
│   │   ├── models/project.py
│   │   ├── schemas/project.py
│   │   ├── crud/project.py
│   │   └── tests/
│   │       ├── conftest.py
│   │       └── test_projects.py
│   ├── main.py
│   └── requirements.txt
│
├── static/                     # Frontend (sin cambios de ubicación)
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── img/
│
├── START-SERVICIOS.bat
├── start-servicios.sh
└── ARQUITECTURA.md (este documento)
```

---

### 10. VENTAJAS DE LA ARQUITECTURA DE MICROSERVICIOS

| Aspecto | Ventaja |
|--------|---------|
| **Escalabilidad** | Escalar MS-Leaders independientemente de MS-Projects |
| **Mantenibilidad** | Cambios en líderes no afectan proyectos |
| **Desarrollo Paralelo** | Equipos pueden trabajar en paralelo |
| **Reusabilidad** | MS-Leaders puede ser consumido por otros servicios |
| **Tolerancia a Fallos** | Si un servicio cae, el otro puede continuar |
| **Despliegue Independiente** | Actualizar sin afectar toda la aplicación |
| **Tecnología Flexible** | Cada servicio puede usar diferentes tecnologías |

---

### 11. MEJORAS FUTURAS

- [ ] Implementar Circuit Breaker para resiliencia
- [ ] Agregar autenticación (JWT)
- [ ] Containerizar con Docker
- [ ] Implementar API Gateway
- [ ] Logging centralizado (ELK Stack)
- [ ] Métricas con Prometheus
- [ ] Comunicación asincrónica (RabbitMQ/Kafka)
- [ ] Cache distribuido (Redis)

---

### 12. CONCLUSIÓN

La migración a microservicios mejora significativamente la arquitectura permitiendo:
- ✓ Desarrollo y despliegue independiente
- ✓ Mejor escalabilidad
- ✓ Mantenimiento simplificado
- ✓ Reutilización de servicios

La comunicación REST entre microservicios permite que MS-Projects enriquezca sus datos con información de MS-Leaders, demostrando la integración exitosa entre servicios.

---

**Documentado:** 14 de febrero de 2026
**Autor:** Estudiante
**Institución:** Universidad de la Remington
**Semestre:** 2026-1
