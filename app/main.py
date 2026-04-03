from fastapi import FastAPI
from app.auth.router import router as auth_router
import app.tasks.models  # noqa: F401 — ensures Task is registered in SQLAlchemy's class registry

app = FastAPI(title="Todo API", description="Learning project: FastAPI for JS developers")

app.include_router(auth_router)
