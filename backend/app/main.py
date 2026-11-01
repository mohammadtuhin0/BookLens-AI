from fastapi import FastAPI
from backend.app.api import health, books

app = FastAPI(
    title = "BookLens AI API",
    description = "An AI-powered visual book understanding and knowledge assistant.",
    version = "0.1.0",
)

@app.get("/")
async def root():
    return {
        "message" : "Welcome to BookLens AI",
        "status" : "running",
        "version" : "0.1.0" 
    }

app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    books.router,
    prefix="/api/v1",
    tags=["Books"],
)