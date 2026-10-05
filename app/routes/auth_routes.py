from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserOut
from app.services.auth_service import register_user, authenticate_user, create_tokens_for_user
from app.database.session import get_db
from app.security.auth import get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Hash password before storing
    hashed = get_password_hash(user_in.password)
    user_in.password = hashed
    user = register_user(db, user_in)
    return user

@router.post("/login")
def login(form_data: dict, db: Session = Depends(get_db)):
    username_or_email = form_data.get("username_or_email")
    password = form_data.get("password")
    user = authenticate_user(db, username_or_email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/email or password")
    tokens = create_tokens_for_user(user)
    return tokens
