from fastapi import FastAPI
from app.database import Base, engine

from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.client import router as client_router
from app.routes.project import router as project_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(project_router)