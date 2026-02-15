from pydantic import BaseModel


class LeaderBase(BaseModel):
    nombre: str
    email: str | None = None
    departamento: str | None = None


class LeaderCreate(LeaderBase):
    pass


class LeaderRead(LeaderBase):
    id: int

    class Config:
        from_attributes = True
