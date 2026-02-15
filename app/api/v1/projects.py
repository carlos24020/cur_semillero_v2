from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Importaciones de tu propia aplicación
from app.core.database import get_db
from app.crud.project import create, get_all, remove
from app.schemas.project import ProjectCreate, ProjectRead

# Se define el router con el prefijo /projects
router = APIRouter(prefix="/projects", tags=["projects"])


# 1. RUTA PARA VER TODOS LOS PROYECTOS (GET)
@router.get("/", response_model=list[ProjectRead])
def read_projects(db: Session = Depends(get_db)):
    return get_all(db)


# 2. RUTA PARA CREAR UN PROYECTO (POST)
@router.post("/", response_model=ProjectRead, status_code=201)
def new_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    return create(db, proj)


# 3. RUTA PARA ELIMINAR UN PROYECTO (DELETE)
@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    # Llama a la función remove que creamos en crud/project.py
    success = remove(db, project_id)

    # Si la función remove devuelve False, lanzamos error 404
    if not success:
        raise HTTPException(status_code=404, detail="El proyecto no existe")

    # Si todo sale bien, devuelve 204 (Sin contenido, pero exitoso)
    return None
