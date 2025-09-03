from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from backend.core.database import SessionLocal
from backend.api.models.user import User
from backend.core.config import settings

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
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


class UserBase(BaseModel):
    email: EmailStr
    password: str
    device_id: str = Field(..., alias="deviceId")

    model_config = ConfigDict(populate_by_name=True)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    device_id: str = Field(..., alias="deviceId")

    model_config = ConfigDict(populate_by_name=True)


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    device_id: str = Field(..., alias="deviceId")

    model_config = ConfigDict(populate_by_name=True)


class RegisterRequest(BaseModel):
    license: str
    team_members: int | None = None
    email: EmailStr
    telephone: str
    first_name: str
    surname1: str
    surname2: str
    nif: str | None = None
    password: str
    confirm_password: str
    company_name: str | None = None
    sector: str
    country: str
    state: str
    zip_code: str | None = None
    terms_accepted: bool
    device_id: str = Field(..., alias="deviceId")

    model_config = ConfigDict(populate_by_name=True)


@router.post("/register")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if not user.terms_accepted:
        raise HTTPException(status_code=400, detail="Terms must be accepted")

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
        device_id=user.device_id,
        license=user.license,
        team_members=user.team_members,
        telephone=user.telephone,
        first_name=user.first_name,
        surname1=user.surname1,
        surname2=user.surname2,
        nif=user.nif,
        company_name=user.company_name,
        sector=user.sector,
        country=user.country,
        state=user.state,
        zip_code=user.zip_code,
        terms_accepted=user.terms_accepted,
        last_login=datetime.utcnow(),
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
    if db_user.sign_in_date is None:
        db_user.sign_in_date = datetime.utcnow()
    db_user.last_login = datetime.utcnow()
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
        payload = jwt.decode(
            req.token, settings.secret_key, algorithms=[settings.algorithm]
        )
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
