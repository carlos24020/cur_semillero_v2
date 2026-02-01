from sqlalchemy import Boolean, Column, Date, Integer, String

from app.core.database import Base  # type: ignore


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    lider = Column(String(100), nullable=False)
    descripcion = Column(String(500))
    fecha_inicio = Column(Date, nullable=False)
    estado = Column(Boolean, default=True)
