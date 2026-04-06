from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.client import Client
from app.models.project import Project
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/clients/")
def create_client(client_name: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    client = Client(client_name=client_name, created_by=user.id)
    db.add(client)
    db.commit()
    db.refresh(client)

    return {
        "id": client.id,
        "client_name": client.client_name,
        "created_by": user.name
    }

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/clients/{id}")
def get_client(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    projects = db.query(Project).filter(Project.client_id == id).all()

    return {
        "id": client.id,
        "client_name": client.client_name,
        "projects": [{"id": p.id, "name": p.project_name} for p in projects]
    }

@router.put("/clients/{id}")
def update_client(id: int, client_name: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.client_name = client_name
    db.commit()

    return {"msg": "Client updated"}

@router.delete("/clients/{id}")
def delete_client(id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"msg": "Client deleted"}