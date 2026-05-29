from auth import hash_password
from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,field_validator
from fastapi import Depends
from database import get_db
from database import engine,Base
from database import get_db
from sqlalchemy.orm import Session
from models import User
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import re

app = FastAPI()
Base.metadata.create_all(bind=engine)

class RegisterRequest(BaseModel):
    username:str
    email:EmailStr    
    password:str

    @field_validator("username")
    @classmethod
    def validate_username(cls,value):
        if len(value) < 3 :
            raise ValueError("Username must be at least 3 characters")
        if len(value) > 20 :
            raise ValueError("Username cannot exceed 20 characters")
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
    def validate_password(cls,value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
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

        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", value):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value    

@app.post("/register",status_code=201)
def register(request:RegisterRequest, db:Session = Depends(get_db)):

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

    hashed_password = hash_password(request.password)
    user = User( username = request.username, email = request.email,password = hashed_password)   
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
    "id": user.id,
    "message": "User registered successfully"
    }
