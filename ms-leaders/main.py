from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.leaders import router as leaders_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS Leaders API", version="0.1.0")

# Configurar CORS - Permitir todas las solicitudes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=False,  # Cambiar a False para mejor compatibilidad
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(leaders_router)


@app.get("/health", tags=["health"])
def root_health():
    return {"status": "up", "service": "ms-leaders", "port": 8001}
