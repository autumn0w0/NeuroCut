import re
from typing import Any


def generate_scenes(
    script: dict[str, Any],
    video_minutes: int = 8,
    scene_duration: int | None = None,
) -> list[dict[str, Any]]:
    sentences = _sentences(script["narration"])
    total_duration = video_minutes * 60

    if scene_duration:
        target_count = max(1, total_duration // scene_duration)
        sentences = _fit_sentence_count(sentences, target_count)
        durations = [scene_duration] * len(sentences)
    else:
        durations = _spread_duration(total_duration, len(sentences))

    character_profile = _character_profile(script["title"], script["base_idea"])
    scenes = []
    for index, sentence in enumerate(sentences):
        visual_action = _visual_action(script["title"], script["base_idea"], sentence, index + 1)
        scenes.append(
            {
                "scene_number": index + 1,
                "duration": durations[index],
                "narration": sentence,
                "character_profile": character_profile,
                "visual_action": visual_action,
                "image_prompt": _image_prompt(script["title"], sentence, visual_action, character_profile),
                "camera_motion": _camera_motion(index),
                "transition": "cut" if index % 3 else "quick fade",
                "music_mood": "dark cinematic ambient",
            }
        )
    return scenes


def _sentences(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [part.strip() for part in parts if part.strip()]


def _fit_sentence_count(sentences: list[str], target_count: int) -> list[str]:
    if len(sentences) >= target_count:
        return sentences[:target_count]
    return sentences + [sentences[-1]] * (target_count - len(sentences))


def _spread_duration(total_seconds: int, count: int) -> list[int]:
    count = max(1, count)
    base = total_seconds // count
    remainder = total_seconds % count
    return [base + (1 if index < remainder else 0) for index in range(count)]


def _image_prompt(title: str, narration: str, visual_action: str, character_profile: str) -> str:
    return (
        "minimal stickman storytelling YouTube animation frame, clean flat design, beige or light background, "
        "thick dark brown outlines, simple round head character, thin body, minimal facial features, "
        "slightly expressive face, cinematic composition, medium shot or side view, no clutter, "
        "consistent recurring character, "
        f"main character design: {character_profile}, "
        f"video title: {title}, "
        f"scene: {visual_action}, "
        f"matching narration sentence: {narration}"
    )


def _visual_action(title: str, base_idea: str, sentence: str, scene_number: int) -> str:
    text = f"{title} {base_idea} {sentence}".lower()

    if "kota" in text or "neet" in text:
        if any(word in text for word in ("tenth", "10th", "pack", "bags", "move")):
            return "teen student leaving home with two bags while parents stand behind, emotional railway station mood"
        if any(word in text for word in ("hostel", "room", "mattress", "fan")):
            return "small Kota hostel room with thin mattress, noisy ceiling fan, open suitcase, student sitting silently"
        if any(word in text for word in ("lecture", "physics", "chemistry", "biology", "coaching")):
            return "crowded coaching classroom in Kota, student struggling to follow equations on board"
        if any(word in text for word in ("food", "mess", "dal", "roti")):
            return "student in hostel mess looking disappointed at watery dal and cold roti on steel plate"
        if any(word in text for word in ("money", "fees", "rent", "notebook")):
            return "student counting limited cash beside coaching fee receipt, rent note, and empty wallet"
        if any(word in text for word in ("test", "marks", "score", "rank")):
            return "student staring at low test marks on paper while other students compare scores nearby"
        if any(word in text for word in ("night", "lonely", "cry", "panic")):
            return "student alone at night under desk lamp, books open, phone call from home on screen"
        if any(word in text for word in ("exam", "paper")):
            return "NEET exam hall, student holding pen with cold nervous hands, answer sheet on desk"
        if any(word in text for word in ("result", "not enough", "drop")):
            return "student looking at result screen showing not selected, drop year form beside laptop"
        return "Kota student walking between hostel and coaching center carrying books, tired but determined"

    if any(word in text for word in ("restaurant", "cafe", "shop", "store")):
        if any(word in text for word in ("wake", "morning", "open", "unlock")):
            return "early morning outside small restaurant, owner unlocking shutter in quiet street"
        if any(word in text for word in ("customer", "order", "serve")):
            return "small restaurant interior, owner serving first customer at counter"
        if any(word in text for word in ("money", "cash", "rent")):
            return "restaurant owner counting cash beside bills and rent notice"
        return "restaurant owner working behind counter in clean simple interior"

    beats = [
        "main character entering a new difficult world",
        "main character facing the first uncomfortable challenge",
        "main character dealing with money pressure and responsibility",
        "main character sitting alone after a setback",
        "main character continuing despite exhaustion",
    ]
    return beats[(scene_number - 1) % len(beats)]


def _character_profile(title: str, base_idea: str) -> str:
    text = f"{title} {base_idea}".lower()
    if "neet" in text or "kota" in text:
        return (
            "same teenage Indian NEET aspirant, simple stickman body, round white head, "
            "short black hair, blue hoodie, backpack, tired serious expression"
        )
    if any(word in text for word in ("restaurant", "cafe", "shop", "store")):
        return (
            "same young restaurant owner, simple stickman body, round white head, "
            "short black hair, teal apron, serious focused expression"
        )
    return "same simple stickman main character, round white head, blue shirt, serious expression"


def _camera_motion(index: int) -> str:
    motions = ["slow push in", "subtle pan right", "slow zoom out", "still dramatic frame"]
    return motions[index % len(motions)]
