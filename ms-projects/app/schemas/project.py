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
