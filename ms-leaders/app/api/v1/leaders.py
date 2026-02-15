from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.leader import create, get_all, get_by_id, remove
from app.schemas.leader import LeaderCreate, LeaderRead

router = APIRouter(prefix="/leaders", tags=["leaders"])


@router.get("/health/status", tags=["health"])
def health_check():
    """Health check detallado"""
    return {"status": "up", "service": "ms-leaders", "port": 8001}


@router.get("/", response_model=list[LeaderRead])
def read_leaders(db: Session = Depends(get_db)):
    """Obtener todos los líderes"""
    return get_all(db)


@router.get("/{leader_id}", response_model=LeaderRead)
def read_leader(leader_id: int, db: Session = Depends(get_db)):
    """Obtener un líder por ID"""
    db_leader = get_by_id(db, leader_id)
    if not db_leader:
        raise HTTPException(status_code=404, detail="Líder no encontrado")
    return db_leader


@router.post("/", response_model=LeaderRead, status_code=201)
def create_leader(leader: LeaderCreate, db: Session = Depends(get_db)):
    """Crear un nuevo líder"""
    return create(db, leader)


@router.delete("/{leader_id}", status_code=204)
def delete_leader(leader_id: int, db: Session = Depends(get_db)):
    """Eliminar un líder"""
    success = remove(db, leader_id)
    if not success:
        raise HTTPException(status_code=404, detail="Líder no encontrado")
    return None
