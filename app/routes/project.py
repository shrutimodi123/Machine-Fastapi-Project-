from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.models.client import Client
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/projects/")
def create_project(project_name: str, client_id: int, users: list[int],
                   db: Session = Depends(get_db), user=Depends(get_current_user)):

    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client not found")

    user_list = db.query(User).filter(User.id.in_(users)).all()
    if len(user_list) != len(users):
        raise HTTPException(status_code=400, detail="Some users not found")

    project = Project(project_name=project_name, client_id=client_id)
    project.users = user_list

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "project_name": project.project_name,
        "client": client.client_name,
        "users": [u.name for u in user_list]
    }

@router.get("/projects/")
def get_projects(db: Session = Depends(get_db), user=Depends(get_current_user)):
    projects = db.query(Project).filter(Project.users.any(id=user.id)).all()

    result = []
    for p in projects:
        client = db.query(Client).filter(Client.id == p.client_id).first()

        result.append({
            "id": p.id,
            "project_name": p.project_name,
            "client": client.client_name if client else None,
            "users": [u.name for u in p.users]
        })

    return result

@router.delete("/projects/{id}")
def delete_project(id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    return {"msg": "Project deleted"}