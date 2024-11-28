from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = user.password 
    db_user = models.User(username=user.username, password=hashed_password,firstName=user.firstName,lastName=user.lastName,role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, skip: int = 0, limit: int = 10,role=str) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).filter(models.User.role == role).all()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
