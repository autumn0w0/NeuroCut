from pathlib import Path


def generate_images(scenes: list[dict], frames_dir: Path) -> list[dict]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    return [
        {
            "scene_number": scene["scene_number"],
            "status": "skipped",
            "reason": "Image generation is reserved for Phase 2.",
            "prompt": scene["image_prompt"],
        }
        for scene in scenes
    ]
