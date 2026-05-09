from typing import Any

from config import STYLES_DIR
from helpers.file_utils import safe_slug, write_json, write_text


def save_style(profile: dict[str, Any], example_prompts: str | None = None) -> dict[str, Any]:
    style_name = profile.get("style_name") or profile.get("name") or "Untitled Style"
    style_id = safe_slug(style_name)
    style_dir = STYLES_DIR / style_id

    profile = {**profile, "style_id": style_id}
    write_json(style_dir / "style.json", profile)
    if example_prompts is not None:
        write_text(style_dir / "example_prompts.txt", example_prompts)

    return profile
