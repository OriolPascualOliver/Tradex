from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from backend.core.database import SessionLocal
from backend.api.models.user import User

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/api-v1/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class UserBase(BaseModel):
    email: EmailStr
    password: str
    device_id: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    device_id: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    device_id: str


@router.post("/register")
def register(user: UserBase, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        email=user.email, hashed_password=pwd_context.hash(user.password), device_id=user.device_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    token = create_access_token({"sub": str(db_user.id), "device_id": user.device_id})
    return {"access_token": token}


@router.post("/login")
def login(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    db_user.device_id = user.device_id
    db.commit()
    token = create_access_token({"sub": str(db_user.id), "device_id": user.device_id})
    return {"access_token": token}


@router.post("/forgotpassword")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == req.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.device_id = req.device_id
    db.commit()
    token = create_access_token(
        {"sub": str(db_user.id), "device_id": req.device_id},
        expires_delta=timedelta(hours=1),
    )
    return {"reset_token": token}


@router.post("/reset")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(req.token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_device_id = payload.get("device_id")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    if token_device_id != req.device_id:
        raise HTTPException(status_code=400, detail="Invalid device")
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.hashed_password = pwd_context.hash(req.new_password)
    db_user.device_id = req.device_id
    db.commit()
    return {"status": "password reset"}
