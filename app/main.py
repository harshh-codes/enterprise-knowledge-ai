
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description=(
        "An evidence-grounded assistant for searching "
        "HR policies and employee handbooks."
    ),
    version=settings.app_version,
)


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
