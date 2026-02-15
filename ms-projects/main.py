from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api.v1.projects import router as projects_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MS Projects API", version="0.1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (frontend)
static_path = os.path.join(os.path.dirname(__file__), "..", "..", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# Incluir rutas
app.include_router(projects_router)


@app.get("/health", tags=["health"])
def root_health():
    return {"status": "up", "service": "ms-projects", "port": 8000}
