from math import ceil
from typing import Any

from config import DEFAULT_SCENE_DURATION_SECONDS


def generate_scenes(
    script: dict[str, Any],
    style: dict[str, Any],
    video_minutes: int = 1,
    scene_duration: int | None = None,
) -> list[dict[str, Any]]:
    duration = scene_duration or style.get("scene_system", {}).get(
        "default_scene_duration", DEFAULT_SCENE_DURATION_SECONDS
    )
    scene_count = max(1, ceil((video_minutes * 60) / duration))
    narration_chunks = _chunk_narration(script["narration"], scene_count)

    motions = style.get("scene_system", {}).get("camera_motion", ["slow zoom"])
    transitions = style.get("scene_system", {}).get("scene_transition", ["fade"])
    return [
        {
            "scene_number": index + 1,
            "duration": duration,
            "narration": narration_chunks[index],
            "image_prompt": _image_prompt(script["topic"], narration_chunks[index], style),
            "camera_motion": motions[index % len(motions)],
            "transition": transitions[index % len(transitions)],
            "music_mood": _music_mood(style),
        }
        for index in range(scene_count)
    ]


def _chunk_narration(narration: str, count: int) -> list[str]:
    sentences = [part.strip() for part in narration.replace("\n", " ").split(".") if part.strip()]
    if not sentences:
        return ["Quiet cinematic moment."] * count

    per_chunk = max(1, ceil(len(sentences) / count))
    chunks = [sentences[index : index + per_chunk] for index in range(0, len(sentences), per_chunk)]
    while len(chunks) < count:
        chunks.append([sentences[-1]])
    return [". ".join(chunk).strip() + "." if chunk else sentences[-1] + "." for chunk in chunks]


def _image_prompt(topic: str, narration: str, style: dict[str, Any]) -> str:
    visual = style.get("visual_style", {})
    required = ", ".join(style.get("image_prompt_rules", {}).get("must_include", []))
    lighting = ", ".join(visual.get("lighting", []))
    palette = ", ".join(visual.get("color_palette", []))
    perspective = visual.get("perspective", "cinematic POV")
    return (
        f"{perspective}, {topic}, {narration} "
        f"{required}, {lighting}, {palette}, detailed cinematic frame"
    ).strip()


def _music_mood(style: dict[str, Any]) -> str:
    genres = style.get("music_style", {}).get("genres", ["ambient"])
    return genres[0]
