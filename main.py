from fastapi import FastAPI

from database import Base, engine
from routes.auth_routes import router as auth_router
from routes.chat_routes import router as chat_router


# =====================================
# FastAPI Application
# =====================================

app = FastAPI()


# =====================================
# Database Initialization
# =====================================

Base.metadata.create_all(
    bind=engine
)


# =====================================
# Register Routers
# =====================================

app.include_router(auth_router)
app.include_router(chat_router)