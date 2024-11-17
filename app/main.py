from fastapi import FastAPI
from app.auth import router as auth_router
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My API",
    description="API Documentation",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc UI endpoint
)

app.include_router(auth_router)
