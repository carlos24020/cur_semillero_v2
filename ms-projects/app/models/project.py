from sqlalchemy import Boolean, Column, Date, Integer, String

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    lider_id = Column(Integer, nullable=False)  # FK a ms-leaders
    descripcion = Column(String(500))
    fecha_inicio = Column(Date, nullable=False)
    estado = Column(Boolean, default=True)
