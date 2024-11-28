from fastapi import APIRouter, Depends, HTTPException, status
from ..crud import user 
from ..schemas import UserCreate, User, AppointmentResponse
from ..database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta 
from typing import List
from ..models import User as DBUser , Appointment
from sqlalchemy.orm import Session
from ..crud import  create_user, get_user_by_id, get_users, delete_user,get_user
from ..utils import get_hashed_password,verify_password,create_access_token,get_current_user,create_refresh_token

router = APIRouter()
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_routes(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, username=user.username)  
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = get_hashed_password(user.password)
    return create_user(db, user=UserCreate(username=user.username, role=user.role, firstName=user.firstName, lastName=user.lastName, password=hashed_password))  

@router.get("/me", response_model=User)
def get_current_user_info(current_user: DBUser = Depends(get_current_user)):  
    return current_user


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(subject=user.username) 

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username,
           
        }
    }
