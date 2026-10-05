from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.security.auth import get_password_hash, verify_password, create_access_token
from app.exceptions.custom_exceptions import NotFoundException
from typing import Optional

def register_user(db: Session, user_in: UserCreate):
    existing = db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first()
    if existing:
        raise Exception("User already exists")
    hashed = get_password_hash(user_in.password)
    user = User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    user = db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_tokens_for_user(user):
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
