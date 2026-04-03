from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.tasks.router import router as tasks_router
import app.tasks.models  # noqa: F401 — ensures Task is registered in SQLAlchemy's class registry

app = FastAPI(title="Todo API", description="Learning project: FastAPI for JS developers")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
