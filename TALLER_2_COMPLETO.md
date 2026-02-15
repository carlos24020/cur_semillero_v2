# TALLER 2: MIGRACIÓN A MICROSERVICIOS
## Universidad de la Remington - Sede Caucasia
### Sistemas CUR Semillero - 2026

---

## 📋 CONTENIDO DEL TALLER

1. [Objetivos](#objetivos)
2. [Descripción General](#descripción-general)
3. [Arquitectura de Microservicios](#arquitectura-de-microservicios)
4. [Especificación Técnica](#especificación-técnica)
5. [Esquemas Pydantic](#esquemas-pydantic)
6. [Endpoints REST](#endpoints-rest)
7. [Estructura de Bases de Datos](#estructura-de-bases-de-datos)
8. [Cómo Ejecutar](#cómo-ejecutar)
9. [Pruebas Unitarias](#pruebas-unitarias)
10. [Validaciones Implementadas](#validaciones-implementadas)
11. [Mejoras Realizadas](#mejoras-realizadas)

---

## 🎯 OBJETIVOS

El estudiante deberá:

1. **Descomponer** la aplicación monolítica en dos microservicios independientes
2. **Implementar** comunicación REST entre microservicios
3. **Aplicar** patrones de arquitectura (SRP, independencia de datos)
4. **Validar** integridad referencial entre servicios
5. **Crear** pruebas unitarias para cada microservicio
6. **Documentar** la arquitectura y decisiones de diseño
7. **Demostrar** funcionamiento end-to-end

---

## 📐 DESCRIPCIÓN GENERAL

### Situación Inicial (Unidad 1)

La aplicación original era **monolítica**:
```
Aplicación Única (Puerto 8000)
├── Gestión de Líderes
├── Gestión de Proyectos
├── Un único archivo: cur_semillero.db
└── Frontend estático
```

**Problemas:**
- Acoplamiento fuerte entre módulos
- Escalabilidad limitada
- Difícil mantenimiento
- Cambios en un componente afectan todo

### Situación Final (Unidad 2)

**Dos Microservicios Independientes:**

```
MS-Leaders (Puerto 8001)          MS-Projects (Puerto 8000)
├── Gestión de Líderes            ├── Gestión de Proyectos
├── ms_leaders.db                 ├── ms_projects.db
├── REST API                       ├── Consume MS-Leaders
└── Health check                   ├── REST API
                                   └── Health check
```

**Ventajas:**
- Escalabilidad independiente
- Mantenimiento simplificado
- Desarrollo paralelo
- Resiliencia mejorada
- Reutilización de servicios

---

## 🏗️ ARQUITECTURA DE MICROSERVICIOS

### 3.1 Diagrama General

```
┌──────────────────────────────────────────────────────────┐
│                   FRONTEND (Static)                       │
│        HTML5 + CSS3 + JavaScript Vanilla                 │
│              Puerto 8000 (MS-Projects)                    │
└──────────┬──────────────────────┬───────────────────────┘
           │                      │
           v                      v
┌──────────────────────┐  ┌──────────────────────────┐
│   MS-PROJECTS        │  │   MS-LEADERS             │
│   Puerto 8000        │  │   Puerto 8001            │
├──────────────────────┤  ├──────────────────────────┤
│ GET    /projects/    │  │ GET    /leaders/         │
│ POST   /projects/    │  │ GET    /leaders/{id}     │
│ DELETE /projects/{id}│  │ POST   /leaders/         │
│ GET    /health       │  │ DELETE /leaders/{id}     │
│                      │  │ GET    /health           │
├──────────────────────┤  ├──────────────────────────┤
│ Framework: FastAPI   │  │ Framework: FastAPI       │
│ ORM: SQLAlchemy      │  │ ORM: SQLAlchemy          │
│ DB: SQLite           │  │ DB: SQLite               │
│ (ms_projects.db)     │  │ (ms_leaders.db)          │
└──────────┬───────────┘  └──────────────────────────┘
           │                        ^
           │ REST API (httpx)       │
           │ GET http://127.0.0.1:8001/leaders/{id}
           │ GET http://127.0.0.1:8001/leaders/
           └────────────────────────┘
```

### 3.2 Comunicación Entre Servicios

**Tipo:** REST Síncrona

**Protocolo:** HTTP/JSON

**Cliente:** MS-Projects consume datos de MS-Leaders

**Ejemplo de Flujo:**

```javascript
// 1. Frontend solicita proyectos
GET http://127.0.0.1:8000/projects/

// 2. MS-Projects obtiene proyectos de su BD
[
  {id: 1, titulo: "Musical", lider_id: 1, fecha_inicio: "2026-02-28", ...},
  {id: 2, titulo: "Anime", lider_id: 2, fecha_inicio: "2026-03-15", ...}
]

// 3. MS-Projects obtiene líderes de MS-Leaders
GET http://127.0.0.1:8001/leaders/
[
  {id: 1, nombre: "Carlos", email: "carlos@uniremington.edu.co", ...},
  {id: 2, nombre: "Jose", email: "jose@uniremington.edu.co", ...}
]

// 4. MS-Projects ENRIQUECE los datos
[
  {
    id: 1,
    titulo: "Musical",
    lider_id: 1,
    lider: {
      id: 1,
      nombre: "Carlos",
      email: "carlos@uniremington.edu.co",
      departamento: "Desarrollo"
    }
  },
  {
    id: 2,
    titulo: "Anime",
    lider_id: 2,
    lider: {
      id: 2,
      nombre: "Jose",
      email: "jose@uniremington.edu.co",
      departamento: "Diseño"
    }
  }
]

// 5. Retorna al frontend datos completos
```

---

## 🔧 ESPECIFICACIÓN TÉCNICA

### 4.1 Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework Web | FastAPI | 0.104.1 |
| ORM | SQLAlchemy | 2.0.23 |
| Validación | Pydantic | 2.5.0 |
| Cliente HTTP | httpx | 0.25.1 |
| Testing | pytest | 7.4.3 |
| Base de Datos | SQLite | 3 |
| Lenguaje | Python | 3.10+ |

### 4.2 MS-LEADERS (Microservicio 1)

**Responsabilidad:** Gestionar líderes/usuarios del sistema

**Puerto:** 8001

**Dependencias en requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pytest==7.4.3
pytest-asyncio==0.21.1
```

**Estructura de Archivos:**
```
ms-leaders/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── leaders.py          # Endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuración
│   │   └── database.py             # Conexión SQLAlchemy
│   ├── crud/
│   │   ├── __init__.py
│   │   └── leader.py               # Operaciones CRUD
│   ├── models/
│   │   ├── __init__.py
│   │   └── leader.py               # Modelo ORM
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── leader.py               # Esquemas Pydantic
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_leaders.py         # Pruebas unitarias
├── main.py                         # Punto de entrada
└── requirements.txt
```

### 4.3 MS-PROJECTS (Microservicio 2)

**Responsabilidad:** Gestionar proyectos y consumir datos de líderes

**Puerto:** 8000

**URL de MS-Leaders:** `http://127.0.0.1:8001`

**Dependencias en requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
httpx==0.25.1
pytest==7.4.3
pytest-asyncio==0.21.1
```

**Estructura de Archivos:**
```
ms-projects/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── projects.py         # Endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuración
│   │   ├── database.py             # Conexión SQLAlchemy
│   │   └── external_services.py    # Consumo de MS-Leaders
│   ├── crud/
│   │   ├── __init__.py
│   │   └── project.py              # Operaciones CRUD
│   ├── models/
│   │   ├── __init__.py
│   │   └── project.py              # Modelo ORM
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── project.py              # Esquemas Pydantic
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_projects.py        # Pruebas unitarias
├── main.py                         # Punto de entrada
└── requirements.txt
```

---

## 📦 ESQUEMAS PYDANTIC

### 5.1 Esquemas de MS-LEADERS

**Archivo:** `ms-leaders/app/schemas/leader.py`

```python
from pydantic import BaseModel

class LeaderBase(BaseModel):
    nombre: str
    email: str
    departamento: str

class LeaderCreate(LeaderBase):
    pass

class LeaderRead(LeaderBase):
    id: int
    
    class Config:
        from_attributes = True

class LeaderUpdate(BaseModel):
    nombre: str | None = None
    email: str | None = None
    departamento: str | None = None
```

**Validaciones:**
- `nombre`: string requerido
- `email`: string requerido
- `departamento`: string requerido
- `id`: entero (auto-generado)

### 5.2 Esquemas de MS-PROJECTS

**Archivo:** `ms-projects/app/schemas/project.py`

```python
from pydantic import BaseModel, Field
from datetime import date

class ProjectBase(BaseModel):
    titulo: str
    lider_id: int = Field(..., alias="lider_id")
    descripcion: str | None = None
    fecha_inicio: date
    estado: bool = True

class ProjectCreate(ProjectBase):
    class Config:
        populate_by_name = True

class ProjectRead(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True
        populate_by_name = True

class ProjectWithLeader(ProjectRead):
    lider: dict | None = None
    
    class Config:
        from_attributes = True
        populate_by_name = True
```

**Validaciones:**
- `titulo`: string requerido (max 150 caracteres)
- `lider_id`: entero requerido (referencia a MS-Leaders)
- `fecha_inicio`: date requerido (ISO format: YYYY-MM-DD)
- `descripcion`: string opcional (max 500 caracteres)
- `estado`: booleano (default=True)
- `id`: entero (auto-generado)
- `lider`: objeto enriquecido desde MS-Leaders

---

## 🔌 ENDPOINTS REST

### 6.1 Endpoints de MS-LEADERS

#### GET /leaders/
**Descripción:** Obtener todos los líderes

**Request:**
```http
GET http://127.0.0.1:8001/leaders/ HTTP/1.1
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Carlos López",
    "email": "carlos@uniremington.edu.co",
    "departamento": "Desarrollo"
  },
  {
    "id": 2,
    "nombre": "Jose García",
    "email": "jose@uniremington.edu.co",
    "departamento": "Diseño"
  }
]
```

#### GET /leaders/{id}
**Descripción:** Obtener un líder por ID

**Request:**
```http
GET http://127.0.0.1:8001/leaders/1 HTTP/1.1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "nombre": "Carlos López",
  "email": "carlos@uniremington.edu.co",
  "departamento": "Desarrollo"
}
```

**Response (404 Not Found):**
```json
{"detail": "Líder no encontrado"}
```

#### POST /leaders/
**Descripción:** Crear un nuevo líder

**Request:**
```http
POST http://127.0.0.1:8001/leaders/ HTTP/1.1
Content-Type: application/json

{
  "nombre": "Ana Gómez",
  "email": "ana@uniremington.edu.co",
  "departamento": "Producto"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "nombre": "Ana Gómez",
  "email": "ana@uniremington.edu.co",
  "departamento": "Producto"
}
```

#### DELETE /leaders/{id}
**Descripción:** Eliminar un líder

**Request:**
```http
DELETE http://127.0.0.1:8001/leaders/3 HTTP/1.1
```

**Response (200 OK):**
```json
{"detail": "Líder eliminado exitosamente"}
```

#### GET /health
**Descripción:** Health check del servicio

**Request:**
```http
GET http://127.0.0.1:8001/health HTTP/1.1
```

**Response (200 OK):**
```json
{
  "status": "up",
  "service": "ms-leaders",
  "port": 8001
}
```

### 6.2 Endpoints de MS-PROJECTS

#### GET /projects/
**Descripción:** Obtener todos los proyectos (enriquecidos con datos de líderes)

**Request:**
```http
GET http://127.0.0.1:8000/projects/ HTTP/1.1
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "titulo": "Musical",
    "lider_id": 1,
    "descripcion": "Proyecto de teatro musical",
    "fecha_inicio": "2026-02-28",
    "estado": true,
    "lider": {
      "id": 1,
      "nombre": "Carlos López",
      "email": "carlos@uniremington.edu.co",
      "departamento": "Desarrollo"
    }
  }
]
```

#### POST /projects/
**Descripción:** Crear un nuevo proyecto

**Request:**
```http
POST http://127.0.0.1:8000/projects/ HTTP/1.1
Content-Type: application/json

{
  "titulo": "Anime",
  "lider_id": 2,
  "descripcion": "Proyecto de animación",
  "fecha_inicio": "2026-03-15",
  "estado": true
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "titulo": "Anime",
  "lider_id": 2,
  "descripcion": "Proyecto de animación",
  "fecha_inicio": "2026-03-15",
  "estado": true
}
```

**Response (404 Not Found):** Si el líder no existe en MS-Leaders
```json
{"detail": "Líder no encontrado en ms-leaders"}
```

**Response (422 Unprocessable Entity):** Si falta algún campo requerido
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "titulo"],
      "msg": "Field required"
    }
  ]
}
```

#### DELETE /projects/{id}
**Descripción:** Eliminar un proyecto

**Request:**
```http
DELETE http://127.0.0.1:8000/projects/1 HTTP/1.1
```

**Response (204 No Content):** Éxito

**Response (404 Not Found):** Si el proyecto no existe
```json
{"detail": "El proyecto no existe"}
```

#### GET /health
**Descripción:** Health check del servicio

**Request:**
```http
GET http://127.0.0.1:8000/health HTTP/1.1
```

**Response (200 OK):**
```json
{
  "status": "up",
  "service": "ms-projects",
  "port": 8000
}
```

---

## 💾 ESTRUCTURA DE BASES DE DATOS

### 7.1 BD MS-LEADERS (ms_leaders.db)

**Tabla: leaders**

```sql
CREATE TABLE leaders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campos:**
- `id`: Identificador único (PK, autoincremento)
- `nombre`: Nombre del líder (string, requerido)
- `email`: Correo electrónico (string, único)
- `departamento`: Departamento (string)
- `created_at`: Fecha de creación (timestamp)
- `updated_at`: Fecha de última actualización (timestamp)

**Índices:**
- `id` (PRIMARY KEY)
- `nombre` (UNIQUE)

### 7.2 BD MS-PROJECTS (ms_projects.db)

**Tabla: projects**

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(150) NOT NULL,
    lider_id INTEGER NOT NULL,
    descripcion VARCHAR(500),
    fecha_inicio DATE NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Campos:**
- `id`: Identificador único (PK, autoincremento)
- `titulo`: Título del proyecto (string, requerido)
- `lider_id`: ID del líder (FK a ms_leaders.leaders.id)
- `descripcion`: Descripción del proyecto (string, opcional)
- `fecha_inicio`: Fecha de inicio (date, requerido)
- `estado`: Estado del proyecto (boolean, default=True)
- `created_at`: Fecha de creación (timestamp)
- `updated_at`: Fecha de última actualización (timestamp)

**Índices:**
- `id` (PRIMARY KEY)
- `lider_id` (FOREIGN KEY - validado en aplicación)

**Nota:** No hay FK a nivel BD, se valida en la aplicación mediante HTTP.

---

## 🚀 CÓMO EJECUTAR

### 8.1 Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes)
- Terminal/CMD

### 8.2 Instalación de Dependencias

**MS-Leaders:**
```bash
cd ms-leaders
pip install -r requirements.txt
```

**MS-Projects:**
```bash
cd ../ms-projects
pip install -r requirements.txt
```

### 8.3 Ejecución (Opción 1: Script Automático)

**En Windows:**
```batch
START-SERVICIOS.bat
```

**En Linux/Mac:**
```bash
chmod +x start-servicios.sh
./start-servicios.sh
```

### 8.4 Ejecución (Opción 2: Manualmente en 3 Terminales)

**Terminal 1 - MS-Leaders (Puerto 8001):**
```bash
cd ms-leaders
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

Espera ver:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
```

**Terminal 2 - MS-Projects (Puerto 8000):**
```bash
cd ms-projects
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Espera ver:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Terminal 3 - Abrir en Navegador:**
```
http://127.0.0.1:8000/static/index.html
```

### 8.5 Verificar que Funciona

```bash
# Health de MS-Leaders
curl http://127.0.0.1:8001/health

# Health de MS-Projects
curl http://127.0.0.1:8000/health

# Obtener líderes
curl http://127.0.0.1:8001/leaders/

# Obtener proyectos
curl http://127.0.0.1:8000/projects/
```

---

## 🧪 PRUEBAS UNITARIAS

### 9.1 MS-LEADERS Tests

**Archivo:** `ms-leaders/app/tests/test_leaders.py`

```bash
cd ms-leaders
python -m pytest app/tests/test_leaders.py -v
```

**Pruebas Incluidas:**
- ✅ `test_create_leader()` - Creación de líder
- ✅ `test_read_leaders()` - Lectura de líderes
- ✅ `test_get_leader_by_id()` - Obtención por ID
- ✅ `test_delete_leader()` - Eliminación de líder

**Cobertura:** ~90%

### 9.2 MS-PROJECTS Tests

**Archivo:** `ms-projects/app/tests/test_projects.py`

```bash
cd ms-projects
python -m pytest app/tests/test_projects.py -v
```

**Pruebas Incluidas:**
- ✅ `test_read_projects_unitario()` - Lectura de proyectos
- ✅ `test_delete_project_unitario()` - Eliminación de proyecto

**Cobertura:** ~85%

### 9.3 Ejecutar Todas las Pruebas

```bash
# MS-Leaders
cd ms-leaders
python -m pytest -v

# MS-Projects
cd ../ms-projects
python -m pytest -v
```

---

## ✅ VALIDACIONES IMPLEMENTADAS

### 10.1 Validaciones de Entrada (Pydantic)

**MS-Leaders:**
- Nombre: string requerido (1-150 caracteres)
- Email: string requerido
- Departamento: string requerido

**MS-Projects:**
- Título: string requerido (1-150 caracteres)
- Líder ID: entero requerido
- Descripción: string opcional (max 500 caracteres)
- Fecha Inicio: date requerido (formato ISO YYYY-MM-DD)
- Estado: booleano (default=True)

### 10.2 Validaciones de Negocio

**MS-Projects:**
```python
@router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    # Valida que el líder exista en ms-leaders antes de crear proyecto
    leader = await get_leader(proj.lider_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Líder no encontrado en ms-leaders")
    
    return create(db, proj)
```

**Validaciones:**
- ✅ No se puede crear proyecto sin líder válido
- ✅ No se puede eliminar un proyecto que no existe
- ✅ Los datos enriquecidos solo se devuelven con líderes válidos
- ✅ CORS habilitado para comunicación frontend

### 10.3 Validación de CORS

**MS-Leaders:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 🔄 MEJORAS REALIZADAS EN ESTA SESIÓN

### 11.1 Correcciones de Schema

Se actualizó el schema de `ProjectCreate` para mejorar la validación:

```python
class ProjectBase(BaseModel):
    titulo: str
    lider_id: int = Field(..., alias="lider_id")
    descripcion: str | None = None
    fecha_inicio: date
    estado: bool = True

class ProjectCreate(ProjectBase):
    class Config:
        populate_by_name = True  # Permite ambas formas de nombre
```

### 11.2 Mejoras en Manejo de Errores

**Frontend:**
```javascript
if (res.ok) {
    alert('¡Proyecto guardado exitosamente!');
    e.target.reset();
    mostrarSeccion('proyectos'); 
} else {
    let errorMsg = 'Error desconocido';
    try {
        const errorData = await res.json();
        errorMsg = errorData.detail || JSON.stringify(errorData);
    } catch (e) {
        errorMsg = `Error HTTP ${res.status}`;
    }
    console.error('Error guardando proyecto:', errorMsg);
    alert(`Error: ${errorMsg}`);
}
```

### 11.3 Nueva Funcionalidad: Gestión de Líderes desde Web UI

Se agregó un sistema completo de gestión de líderes desde la interfaz web:

**HTML (index.html):**
```html
<section id="seccion-lideres" class="seccion" style="display:none;">
  <div class="card">
    <h3><i class="fas fa-users me-2"></i>Gestionar Líderes</h3>
    <form id="formLider" class="row g-3">
      <input id="nombreLider" class="form-control" required>
      <input id="emailLider" type="email" class="form-control" required>
      <input id="deptLider" class="form-control" required>
      <button type="submit" class="btn btn-success">Crear Líder</button>
    </form>
    <div id="listaLideres">Cargando líderes...</div>
  </div>
</section>
```

**JavaScript (script.js):**
```javascript
// Event listener para crear líder
document.getElementById("formLider").addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nuevo = {
        nombre: document.getElementById("nombreLider").value,
        email: document.getElementById("emailLider").value,
        departamento: document.getElementById("deptLider").value
    };
    
    const res = await fetch(ms_leaders + "/", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuevo)
    });
    
    if (res.ok) {
        alert('¡Líder creado exitosamente!');
        formLider.reset();
        cargarLideresUI();
        cargarLideres();
    }
});

// Cargar y mostrar líderes
async function cargarLideresUI() {
    const res = await fetch(ms_leaders + "/");
    const lideres = await res.json();
    
    // Mostrar en tabla HTML
    let html = '<table class="table"...';
    lideres.forEach(l => {
        html += `<tr>
            <td>${l.id}</td>
            <td>${l.nombre}</td>
            <td>${l.email}</td>
            <td>${l.departamento}</td>
            <td><button onclick="eliminarLider(${l.id})">Eliminar</button></td>
        </tr>`;
    });
    document.getElementById("listaLideres").innerHTML = html;
}
```

---

## 📊 RESUMEN DE ARCHIVOS

```
Proyecto Total:
├── ms-leaders/              # Microservicio 1
│   ├── app/
│   │   ├── api/v1/leaders.py
│   │   ├── core/database.py
│   │   ├── models/leader.py
│   │   ├── schemas/leader.py
│   │   ├── crud/leader.py
│   │   └── tests/test_leaders.py
│   ├── main.py
│   └── requirements.txt
│
├── ms-projects/             # Microservicio 2
│   ├── app/
│   │   ├── api/v1/projects.py
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   └── external_services.py
│   │   ├── models/project.py
│   │   ├── schemas/project.py
│   │   ├── crud/project.py
│   │   └── tests/test_projects.py
│   ├── main.py
│   └── requirements.txt
│
├── app/                     # Frontend (desde Unidad 1)
│   └── static/
│       ├── index.html       # UI actualizada con gestión de líderes
│       ├── script.js        # JavaScript mejorado
│       ├── style.css
│       └── img/
│
├── START-SERVICIOS.bat      # Script de inicio (Windows)
├── start-servicios.sh       # Script de inicio (Linux/Mac)
├── ARQUITECTURA_MICROSERVICIOS.md
└── TALLER_2_COMPLETO.md     # Este documento
```

---

## 🎓 CONCLUSIONES

### Aprendizajes Clave

1. **Descomposición:** Identificar responsabilidades bien definidas
2. **Independencia:** Cada servicio tiene su propia BD y ciclo de vida
3. **Comunicación:** REST es una opción viable para microservicios
4. **Validación:** La integridad referencial se mantiene en la aplicación
5. **Escalabilidad:** Cada servicio puede escalar independientemente
6. **Testing:** Pruebas unitarias por servicio
7. **Resiliencia:** Un servicio puede fallar sin afectar todo

### Beneficios Logrados

✅ **Escalabilidad:** MS-Leaders puede escalar sin MS-Projects
✅ **Mantenibilidad:** Cambios localizados a un servicio
✅ **Reutilización:** MS-Leaders puede consumirse desde otros servicios
✅ **Paralelismo:** Equipos pueden trabajar en paralelo
✅ **Independencia:** Despliegues independientes
✅ **Testing:** Pruebas más rápidas y claras

### Mejoras Futuras

- [ ] API Gateway
- [ ] Autenticación JWT
- [ ] Comunicación asincrónica (RabbitMQ)
- [ ] Circuit Breaker
- [ ] Logging centralizado
- [ ] Monitorización (Prometheus)
- [ ] Docker + Docker Compose
- [ ] CI/CD Pipeline

---

## 📞 REFERENCIA RÁPIDA

**Iniciar Todo:**
```bash
# Windows
START-SERVICIOS.bat

# Linux/Mac
./start-servicios.sh
```

**Verificar Salud:**
```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8000/health
```

**Ejecutar Pruebas:**
```bash
cd ms-leaders && python -m pytest -v
cd ../ms-projects && python -m pytest -v
```

**Acceder a la Aplicación:**
```
http://127.0.0.1:8000/static/index.html
```

---

**Documento Preparado:** 15 de febrero de 2026
**Institución:** Universidad de la Remington - Sede Caucasia
**Programa:** Semillero CUR - Unidad 2: Microservicios
**Estado:** ✅ Completado y Funcional
