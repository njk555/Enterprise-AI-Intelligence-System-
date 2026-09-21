from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine

app = FastAPI(
    title="Enterprise AI Intelligence Engine",
    description="AI-powered enterprise intelligence and decision platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "Enterprise AI Intelligence Engine",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }