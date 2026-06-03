from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session
import re

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

from database import (
    Base,
    engine,
    get_db
)

from models import User


app = FastAPI()

Base.metadata.create_all(bind=engine)


# =====================================
# Register Request Schema
# =====================================

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value):

        if len(value) < 3:
            raise ValueError(
                "Username must be at least 3 characters"
            )

        if len(value) > 20:
            raise ValueError(
                "Username cannot exceed 20 characters"
            )

        if not re.match(
            r"^[a-zA-Z0-9_]+$",
            value
        ):
            raise ValueError(
                "Username can contain only letters, numbers and underscore"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters"
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not re.search(
            r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",
            value
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value


# =====================================
# Register API
# =====================================

@app.post("/register", status_code=201)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_email = db.query(User).filter(
        User.email == request.email
    ).first()

    existing_user = db.query(User).filter(
        User.username == request.username
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        request.password
    )

    user = User(
        username=request.username,
        email=request.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "message": "User registered successfully"
    }


# =====================================
# Login Request Schema
# =====================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if not value.strip():
            raise ValueError(
                "Password cannot be empty"
            )

        return value


# =====================================
# Login API
# =====================================

@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Username/Password not matched"
        )

    token = create_access_token(
        {"sub": request.email}
    )

    return {
        "message": "Login successful",
        "token_type": "Bearer",
        "access_token": token
    }