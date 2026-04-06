from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password

router = APIRouter()

@router.post("/users/")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(name=name, email=email, password=hash_password(password))
    db.add(user)
    db.commit()

    return {"msg": "User created"}

@router.get("/users/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()