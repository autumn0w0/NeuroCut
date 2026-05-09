from pathlib import Path
from typing import Any

from config import STYLES_DIR
from helpers.file_utils import read_json, safe_slug


def style_path(style_name: str) -> Path:
    return STYLES_DIR / safe_slug(style_name) / "style.json"


def load_style(style_name: str) -> dict[str, Any]:
    path = style_path(style_name)
    if not path.exists():
        raise FileNotFoundError(f"Style not found: {style_name}")
    return read_json(path)


def list_styles() -> list[dict[str, Any]]:
    styles = []
    if not STYLES_DIR.exists():
        return styles

    for style_file in sorted(STYLES_DIR.glob("*/style.json")):
        data = read_json(style_file)
        styles.append(
            {
                "id": style_file.parent.name,
                "style_name": data.get("style_name", style_file.parent.name),
                "category": data.get("category"),
                "description": data.get("description"),
            }
        )
    return styles
