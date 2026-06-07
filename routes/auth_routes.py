import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import RegisterRequest, LoginRequest

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from fastapi import APIRouter

router = APIRouter()

# =====================================
# Register API
# =====================================

@router.post("/register", status_code=201)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user or email exists in a single query block
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(request.password)
    user = User(
        username=request.username,
        email=request.email,
        password=hashed_pw
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "message": "User registered successfully"
    }


# =====================================
# Login API
# =====================================

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    token = create_access_token({"sub": user.email})

    return {
        "message": "Login successful",
        "token_type": "Bearer",
        "access_token": token
    }


# =====================================
# Authentication Test API
# =====================================    

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username
        }
    }
