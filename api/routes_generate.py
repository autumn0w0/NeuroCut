from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config import DEFAULT_STYLE, DEFAULT_VIDEO_MINUTES
from pipeline.run_pipeline import run_pipeline

router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    style_name: str = DEFAULT_STYLE
    video_minutes: int = Field(DEFAULT_VIDEO_MINUTES, ge=1, le=60)
    scene_duration: int | None = Field(default=None, ge=2, le=60)
    provider: str | None = None


@router.post("")
def generate_video_plan(request: GenerateRequest) -> dict[str, Any]:
    try:
        return run_pipeline(
            topic=request.topic,
            style_name=request.style_name,
            video_minutes=request.video_minutes,
            scene_duration=request.scene_duration,
            provider=request.provider,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
