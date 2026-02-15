from sqlalchemy.orm import Session
from app.models.leader import Leader
from app.schemas.leader import LeaderCreate


def get_all(db: Session):
    return db.query(Leader).all()


def get_by_id(db: Session, leader_id: int):
    return db.query(Leader).filter(Leader.id == leader_id).first()


def get_by_nombre(db: Session, nombre: str):
    return db.query(Leader).filter(Leader.nombre == nombre).first()


def create(db: Session, obj_in: LeaderCreate):
    db_obj = Leader(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, leader_id: int):
    db_leader = db.query(Leader).filter(Leader.id == leader_id).first()
    if db_leader:
        db.delete(db_leader)
        db.commit()
        return True
    return False
