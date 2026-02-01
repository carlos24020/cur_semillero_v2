from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.project import create, get_all
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectRead])
def read_projects(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/", response_model=ProjectRead, status_code=201)
def new_project(proj: ProjectCreate, db: Session = Depends(get_db)):
    return create(db, proj)
