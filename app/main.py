from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.projects import router as projects_router

app = FastAPI(title="CUR Semillero API", version="0.1.0")

# 1. Definimos los orígenes permitidos (Tu Live Server)
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

# 2. Configuramos el Middleware de CORS (REEMPLAZA el anterior con este)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],  # <--- DELETE es la clave aquí
    allow_headers=["*"],
)

# 3. Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")

# 4. Incluir las rutas de proyectos
app.include_router(projects_router)
