from pathlib import Path


def generate_captions(script: dict, audio_dir: Path) -> dict:
    audio_dir.mkdir(parents=True, exist_ok=True)
    return {
        "status": "skipped",
        "reason": "Whisper subtitle syncing is reserved for Phase 2.",
        "subtitles_path": None,
    }
