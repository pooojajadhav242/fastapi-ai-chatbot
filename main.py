from fastapi import FastAPI

from database import Base, engine

from routes.auth_routes import router as auth_router
from routes.chat_routes import router as chat_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(chat_router)