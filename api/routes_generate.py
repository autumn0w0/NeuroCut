from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from pipeline.run_pipeline import run_pipeline

router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    base_idea: str = Field(..., min_length=1)
    provider: str | None = None


@router.post("")
def generate_video_plan(request: GenerateRequest) -> dict[str, Any]:
    try:
        return run_pipeline(
            title=request.title,
            base_idea=request.base_idea,
            provider=request.provider,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
