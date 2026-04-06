from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils.security import verify_password, create_token, decode_token
from app.database import get_db
from app.models.user import User

router = APIRouter()

SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(p):
    return pwd_context.hash(p)

def verify_password(p, hp):
    return pwd_context.verify(p, hp)

def create_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = decode_token(token)   # ✅ use this
        user = db.query(User).filter(User.id == data["id"]).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
@router.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid login")

    token = create_token({"id": user.id})
    return {"access_token": token, "token_type": "bearer"}