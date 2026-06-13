from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password
)
from database import get_db
from models import User
from schemas import (
    LoginRequest,
    RegisterRequest
)

router = APIRouter()


# =====================================
# Register API
# =====================================

@router.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_email = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    existing_user = (
        db.query(User)
        .filter(User.username == request.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password)
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
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    if not verify_password(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        {
            "sub": user.email
        }
    )

    return {
        "message": "Login successful",
        "token_type": "Bearer",
        "access_token": access_token
    }


# =====================================
# Protected Route
# =====================================

@router.get("/protected")
def protected_route(
    current_user: User = Depends(get_current_user)
):

    return {
        "message": "Access granted",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }