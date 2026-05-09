from fastapi import FastAPI

from api.routes_export import router as export_router
from api.routes_generate import router as generate_router
from api.routes_styles import router as styles_router

app = FastAPI(
    title="NeuroCut API",
    description="AI video generation backend for creator-style analysis and scene-based video planning.",
    version="0.1.0",
)

app.include_router(styles_router)
app.include_router(generate_router)
app.include_router(export_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
