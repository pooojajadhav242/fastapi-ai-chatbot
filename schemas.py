from pydantic import BaseModel, EmailStr, field_validator
import re

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
# AI Request Schema
# =====================================

class AIRequest(BaseModel):
    username:str
    question:str