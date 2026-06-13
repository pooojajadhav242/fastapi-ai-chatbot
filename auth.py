from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session

from database import get_db
from models import User


# =====================================
# Configuration
# =====================================

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


# =====================================
# Password Utilities
# =====================================

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pbkdf2_sha256.verify(
        plain_password,
        hashed_password
    )


# =====================================
# JWT Token Utilities
# =====================================

def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# =====================================
# Authentication Dependency
# =====================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    token = credentials.credentials

    payload = verify_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload["sub"]

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user