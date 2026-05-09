from typing import Any

from helpers.call_llm import call_llm


def generate_script(
    topic: str,
    style: dict[str, Any],
    video_minutes: int = 1,
    provider: str | None = None,
) -> dict[str, Any]:
    system = (
        "You are a cinematic faceless-video scriptwriter. Write immersive narration "
        "that follows the supplied creator style and avoids copying any real creator verbatim."
    )
    prompt = f"""
Topic: {topic}
Target length: {video_minutes} minute(s)
Style profile: {style}

Return a complete narration only. Use short sensory paragraphs and a quiet emotional arc.
"""
    result = call_llm(prompt, system=system, provider=provider)
    narration = result.text.strip() or _fallback_script(topic, style, video_minutes)
    return {
        "topic": topic,
        "title": _title_for(topic, style),
        "narration": narration,
        "provider": result.provider,
        "model": result.model,
    }


def _title_for(topic: str, style: dict[str, Any]) -> str:
    if topic.lower().startswith(("your life as", "a day in the life", "pov:")):
        return topic
    patterns = style.get("title_patterns") or ["Your Life as a _____"]
    pattern = patterns[0]
    return pattern.replace("_____", topic).replace("POV:", "POV:")


def _fallback_script(topic: str, style: dict[str, Any], video_minutes: int) -> str:
    tone = style.get("core_identity", {}).get("tone", "calm cinematic narration")
    return "\n\n".join(
        [
            f"You wake up inside the world of {topic}. The day has already started without asking your permission.",
            f"The room is quiet, but every object seems to know its job. Your hands move first. Your thoughts arrive later.",
            f"You follow the small rituals that keep this life together. The light changes slowly. The work repeats itself, and somehow the repetition begins to feel like a language.",
            f"By the middle of the day, the weight of this life becomes clear. Not dramatic. Not loud. Just present in the corners, in the pauses, in the things nobody else notices.",
            f"Evening comes softly. You understand that {topic} is not only a role, but a way of being seen by the world.",
            f"And tomorrow, before sunrise, you will begin again. The same room. The same quiet. The same strange comfort of being exactly here.",
            f"Narration direction: {tone}. Target length: about {video_minutes} minute(s).",
        ]
    )
