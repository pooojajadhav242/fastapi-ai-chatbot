from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session
import re
from ai_service import ask_gemini
from fastapi import Header
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Request
from models import (User, ChatMessage)
security = HTTPBearer()


from schemas import (
    RegisterRequest,
    LoginRequest,
    AIRequest
)

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

app = FastAPI()

Base.metadata.create_all(bind=engine)

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

# =====================================
# AUthentication API
# =====================================    

@app.get("/protected")
def protected_route(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "message": "Access granted",
        "user": payload
    }

# =====================================
# AI API
# =====================================    

@app.post("/ask-ai")
def ask_ai(request:AIRequest, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email = payload["sub"]

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.add(ChatMessage(
        user_id = user.id,
        role="User",
        message=request.question
    ))
    db.commit()


    try:
        answer = ask_gemini(request.question)

    except Exception as e:
        error_message = str(e)

        if "429" in error_message:

            raise HTTPException(
                status_code=429,
                detail=
                "Too many requests 😄 Please wait a little and try again."
            )

        raise HTTPException(
            status_code=500,
            detail=
            "Something went wrong with AI response."
        ) 

    db.add(ChatMessage(
        user_id = user.id,
        role="AI",
        message=answer
    ))
    db.commit()
    
    return {
        "email":email,
        "answer" : answer
    }