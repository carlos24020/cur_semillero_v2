from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.external_services import get_leader, get_all_leaders
from app.crud.project import create, get_all, remove
from app.schemas.project import ProjectCreate, ProjectRead, ProjectWithLeader

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectWithLeader])
async def read_projects(db: Session = Depends(get_db)):
    """Obtiene todos los proyectos con información de los líderes"""
    projects = get_all(db)
    leaders_map = {}
    
    # Obtiene todos los líderes de una sola llamada
    leaders = await get_all_leaders()
    for leader in leaders:
        leaders_map[leader["id"]] = leader
    
    # Enriquece los proyectos con información del líder
    result = []
    for project in projects:
        project_dict = {
            "id": project.id,
            "titulo": project.titulo,
            "lider_id": project.lider_id,
            "descripcion": project.descripcion,
            "fecha_inicio": project.fecha_inicio,
            "estado": project.estado,
            "lider": leaders_map.get(project.lider_id)
        }
        result.append(project_dict)
    
    return result


@router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proyecto"""
    # Valida que el líder exista en ms-leaders
    leader = await get_leader(proj.lider_id)
    if not leader:
        raise HTTPException(status_code=404, detail="Líder no encontrado en ms-leaders")
    
    return create(db, proj)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Elimina un proyecto"""
    success = remove(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="El proyecto no existe")
    return None


@router.get("/health/status", tags=["health"])
def health_check():
    return {"status": "up", "service": "ms-projects", "port": 8000}
