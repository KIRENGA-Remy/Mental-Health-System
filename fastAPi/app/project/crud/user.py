from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import User
from ..schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = user.password 
    db_user = User(username=user.username, password=hashed_password,firstName=user.firstName,lastName=user.lastName,role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, skip: int = 0, limit: int = 10,role=str) -> List[User]:
    return db.query(User).offset(skip).limit(limit).filter(User.role == role).all()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
