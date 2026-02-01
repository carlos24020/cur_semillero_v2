from datetime import date

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    titulo: str
    lider: str
    descripcion: str | None = None
    fecha_inicio: date


class ProjectRead(ProjectCreate):
    id: int
    estado: bool

    class Config:
        from_attributes = True
