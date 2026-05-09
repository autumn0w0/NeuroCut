import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, data: Any) -> Path:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")
    return path


def write_text(path: Path, content: str) -> Path:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")
    return path


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "untitled"


def utc_job_id(prefix: str = "job") -> str:
    return f"{prefix}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
