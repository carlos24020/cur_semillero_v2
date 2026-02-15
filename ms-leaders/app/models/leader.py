from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Leader(Base):
    __tablename__ = "leaders"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    email = Column(String(100))
    departamento = Column(String(100))
