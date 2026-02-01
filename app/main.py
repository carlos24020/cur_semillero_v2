from fastapi import FastAPI

from app.api.v1.projects import router as projects_router

app = FastAPI(title="CUR Semillero API", version="0.1.0")
app.include_router(projects_router)
