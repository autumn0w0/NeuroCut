from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from helpers.load_style import list_styles, load_style
from helpers.save_style import save_style
from pipeline.analyze_style import analyze_style

router = APIRouter(prefix="/styles", tags=["styles"])


class StyleCreateRequest(BaseModel):
    style_name: str = Field(..., min_length=1)
    sources: list[str] = Field(default_factory=list)
    custom_prompt: str | None = None
    visual_aesthetic: str | None = None
    profile: dict[str, Any] | None = None
    example_prompts: str | None = None


@router.get("")
def get_styles() -> list[dict[str, Any]]:
    return list_styles()


@router.get("/{style_name}")
def get_style(style_name: str) -> dict[str, Any]:
    try:
        return load_style(style_name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("")
def create_style(request: StyleCreateRequest) -> dict[str, Any]:
    profile = request.profile or analyze_style(
        style_name=request.style_name,
        sources=request.sources,
        custom_prompt=request.custom_prompt,
        visual_aesthetic=request.visual_aesthetic,
    )
    profile["style_name"] = request.style_name
    return save_style(profile, request.example_prompts)
