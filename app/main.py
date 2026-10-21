
from fastapi.middleware.cors import CORSMiddleware  
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description=(
        "An evidence-grounded assistant for searching "
        "HR policies and employee handbooks."
    ),
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API is running",
        "status": "healthy",
        "version": settings.app_version,
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
