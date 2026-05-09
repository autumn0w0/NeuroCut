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
    character_profile = _character_profile(script["topic"])
    scenes = []
    for index in range(scene_count):
        visual_action = _visual_action(script["topic"], narration_chunks[index], index + 1)
        scenes.append(
            {
                "scene_number": index + 1,
                "duration": duration,
                "narration": narration_chunks[index],
                "character_profile": character_profile,
                "visual_action": visual_action,
                "image_prompt": _image_prompt(
                    script["topic"],
                    narration_chunks[index],
                    style,
                    visual_action,
                    character_profile,
                ),
                "camera_motion": motions[index % len(motions)],
                "transition": transitions[index % len(transitions)],
                "music_mood": _music_mood(style),
            }
        )
    return scenes


def _chunk_narration(narration: str, count: int) -> list[str]:
    sentences = [part.strip() for part in narration.replace("\n", " ").split(".") if part.strip()]
    if not sentences:
        return ["Quiet cinematic moment."] * count

    per_chunk = max(1, ceil(len(sentences) / count))
    chunks = [sentences[index : index + per_chunk] for index in range(0, len(sentences), per_chunk)]
    while len(chunks) < count:
        chunks.append([sentences[-1]])
    return [". ".join(chunk).strip() + "." if chunk else sentences[-1] + "." for chunk in chunks]


def _image_prompt(
    topic: str,
    narration: str,
    style: dict[str, Any],
    visual_action: str,
    character_profile: str,
) -> str:
    return (
        "clean 2D faceless storytime animation still, thick black outlines, smooth vector cartoon, "
        "round white simple characters with dot eyes, expressive body language, warm YouTube explainer style, "
        "detailed cozy background, polished digital illustration, 16:9 frame, "
        "keep the same recurring main character design in every scene, "
        f"main character: {character_profile}, "
        f"scene action: {visual_action}, topic: {topic}, narration context: {narration}"
    ).strip()


def _music_mood(style: dict[str, Any]) -> str:
    genres = style.get("music_style", {}).get("genres", ["ambient"])
    return genres[0]


def _visual_action(topic: str, narration: str, scene_number: int) -> str:
    text = f"{topic} {narration}".lower()

    if any(word in text for word in ("restaurant", "cafe", "shop", "store")):
        if any(word in text for word in ("wake", "morning", "sunrise", "open", "unlock")):
            return (
                "early morning outside a small restaurant, main character unlocking the front door, "
                "warm sunrise light, empty street, signboard, shutters half open"
            )
        if any(word in text for word in ("customer", "people", "order", "serve")):
            return (
                "inside a small busy restaurant, faceless customers at tables, main character serving food, "
                "counter, menu board, warm kitchen light"
            )
        if any(word in text for word in ("close", "night", "evening", "tomorrow")):
            return (
                "quiet restaurant after closing, main character wiping a table, chairs stacked, "
                "soft evening light through the windows"
            )
        return (
            "inside a small restaurant kitchen, main character preparing the first orders, pans, counter, "
            "warm light and clean cartoon details"
        )

    if any(word in text for word in ("baker", "bakery", "bread", "flour", "oven")):
        if any(word in text for word in ("wake", "morning", "sunrise", "before")):
            return (
                "early morning bakery exterior, faceless baker opening the bakery door, warm light inside, "
                "quiet street and bread sign"
            )
        if any(word in text for word in ("knead", "flour", "hands", "loaves")):
            return (
                "inside a cozy bakery kitchen, faceless baker kneading dough on a wooden table, flour, "
                "bread trays, glowing oven"
            )
        if any(word in text for word in ("people", "street", "depends", "remember")):
            return (
                "bakery counter with townspeople waiting for fresh bread, faceless baker handing over loaves, "
                "warm cheerful morning interior"
            )
        return "cozy bakery interior with oven glow, bread loaves, flour table, faceless baker working quietly"

    if any(word in text for word in ("wake", "morning", "sunrise")):
        return "main character waking up in a small warm room at sunrise, simple faceless cartoon style"
    if any(word in text for word in ("work", "hands", "routine")):
        return "main character doing daily work with focused hands, tools on table, warm detailed interior"
    if any(word in text for word in ("evening", "night", "tomorrow")):
        return "quiet evening room, main character standing near window, soft lamp light, reflective mood"

    beats = [
        "establishing shot of the main character entering their daily world",
        "medium shot of the main character doing the central routine",
        "two faceless characters having a quiet emotional moment indoors",
        "main character pausing thoughtfully in a detailed warm room",
    ]
    return beats[(scene_number - 1) % len(beats)]


def _character_profile(topic: str) -> str:
    text = topic.lower()
    if any(word in text for word in ("restaurant", "cafe", "shop", "store")):
        return (
            "faceless young restaurant owner, round white head with small black dot eyes, "
            "short black hair, teal apron over cream shirt, dark trousers, simple white hands"
        )
    if any(word in text for word in ("baker", "bakery", "bread")):
        return (
            "faceless medieval baker, round white head with small black dot eyes, "
            "tan linen shirt, brown apron, rolled sleeves, simple white hands"
        )
    if any(word in text for word in ("student", "school", "college")):
        return (
            "faceless student, round white head with small black dot eyes, "
            "navy hoodie, backpack strap, simple white hands"
        )
    return (
        "faceless main character, round white head with small black dot eyes, "
        "blue sweater, dark trousers, simple white hands"
    )
