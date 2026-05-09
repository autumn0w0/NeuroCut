from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
STYLES_DIR = ROOT_DIR / "styles"
EXPORTS_DIR = ROOT_DIR / "exports"
TEMP_DIR = ROOT_DIR / "temp"

DEFAULT_STYLE = "oddly_specific_lives"
DEFAULT_SCENE_DURATION_SECONDS = 10
DEFAULT_VIDEO_MINUTES = 1


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    import os

    value = os.getenv(name)
    return value if value not in ("", None) else default


LLM_PROVIDER = get_env("LLM_PROVIDER", "mock")
GROQ_API_KEY = get_env("GROQ_API_KEY")
GROQ_MODEL = get_env("GROQ_MODEL", "llama-3.1-70b-versatile")
OPENROUTER_API_KEY = get_env("OPENROUTER_API_KEY")
OPENROUTER_MODEL = get_env("OPENROUTER_MODEL", "deepseek/deepseek-chat")
OLLAMA_MODEL = get_env("OLLAMA_MODEL", "llama3")
OLLAMA_BASE_URL = get_env("OLLAMA_BASE_URL", "http://localhost:11434")

IMAGE_PROVIDER = get_env("IMAGE_PROVIDER", "pollinations")
IMAGE_WIDTH = int(get_env("IMAGE_WIDTH", "1280") or "1280")
IMAGE_HEIGHT = int(get_env("IMAGE_HEIGHT", "720") or "720")
AUTOMATIC1111_BASE_URL = get_env("AUTOMATIC1111_BASE_URL", "http://127.0.0.1:7860")
