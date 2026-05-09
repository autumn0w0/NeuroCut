from pathlib import Path


def generate_audio(script: dict, audio_dir: Path) -> dict:
    audio_dir.mkdir(parents=True, exist_ok=True)
    return {
        "status": "skipped",
        "reason": "Voiceover and music generation are reserved for Phase 2.",
        "voiceover_path": None,
        "music_path": None,
    }
