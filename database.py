from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)


# =====================================
# Database Configuration
# =====================================

DATABASE_URL = "sqlite:///./users_chat.db"


# =====================================
# Database Engine
# =====================================

engine = create_engine(
    DATABASE_URL
)


# =====================================
# Session Factory
# =====================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =====================================
# Base Model
# =====================================

Base = declarative_base()


# =====================================
# Database Dependency
# =====================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()