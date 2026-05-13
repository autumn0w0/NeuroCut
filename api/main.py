from fastapi import FastAPI

from api.routes_export import router as export_router
from api.routes_generate import router as generate_router

app = FastAPI(
    title="NeuroCut API",
    description="AI video generation backend for creator-style analysis and scene-based video planning.",
    version="0.1.0",
)

app.include_router(generate_router)
app.include_router(export_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "NeuroCut API",
        "docs": "/docs",
        "health": "/health",
    }
