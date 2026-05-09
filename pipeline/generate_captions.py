from pathlib import Path


def generate_captions(scenes: list[dict], audio_dir: Path) -> dict:
    audio_dir.mkdir(parents=True, exist_ok=True)
    subtitles_path = audio_dir / "subtitles.srt"
    subtitles_path.write_text(_srt_for_scenes(scenes), encoding="utf-8")
    return {
        "status": "created",
        "reason": "Created scene-timed subtitles from generated narration.",
        "subtitles_path": str(subtitles_path),
    }


def _srt_for_scenes(scenes: list[dict]) -> str:
    lines = []
    cursor = 0
    for index, scene in enumerate(scenes, start=1):
        duration = int(scene.get("duration", 10))
        start = _timestamp(cursor)
        end = _timestamp(cursor + duration)
        lines.extend([str(index), f"{start} --> {end}", scene.get("narration", "").strip(), ""])
        cursor += duration
    return "\n".join(lines)


def _timestamp(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02},000"
