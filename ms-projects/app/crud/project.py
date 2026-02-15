from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate


def get_all(db: Session):
    return db.query(Project).all()


def get_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create(db: Session, obj_in: ProjectCreate):
    db_obj = Project(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, project_id: int):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False
