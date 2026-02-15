# CUR Semillero v2 - MICROSERVICIOS

Sistema de gestión de proyectos académicos descompuesto en **dos microservicios independientes**.

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

**En Windows:**
```batch
START-SERVICIOS.bat
```

**En Linux/Mac:**
```bash
chmod +x start-servicios.sh
./start-servicios.sh
```

### Opción 2: Iniciar Manualmente (3 Terminales)

**Terminal 1 - MS-Leaders (Puerto 8001):**
```bash
cd ms-leaders
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 2 - MS-Projects (Puerto 8000):**
```bash
cd ms-projects
pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 3 - Abrir en navegador:**
```
http://127.0.0.1:8000/static/index.html
```

## 📡 Verificar que Funciona

```bash
# Health del MS-Leaders
curl http://127.0.0.1:8001/health

# Health del MS-Projects  
curl http://127.0.0.1:8000/health

# Obtener líderes
curl http://127.0.0.1:8001/leaders/

# Obtener proyectos
curl http://127.0.0.1:8000/projects/
```

## 🧪 Ejecutar Pruebas

### MS-Leaders
```bash
cd ms-leaders
python -m pytest app/tests/test_leaders.py -v
```

### MS-Projects
```bash
cd ms-projects
python -m pytest app/tests/test_projects.py -v
```

## 📚 Documentación Técnica

Ver el archivo completo: [ARQUITECTURA_MICROSERVICIOS.md](./ARQUITECTURA_MICROSERVICIOS.md)

Incluye diagrama de arquitectura, especificaciones de endpoints, y comunicación entre servicios.

---
Backend FastAPI + SQLAlchemy + pytest + Docker + CI/CD