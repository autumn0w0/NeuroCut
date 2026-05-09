from typing import Any

from helpers.file_utils import safe_slug


def analyze_style(
    style_name: str,
    sources: list[str] | None = None,
    custom_prompt: str | None = None,
    visual_aesthetic: str | None = None,
) -> dict[str, Any]:
    sources = sources or []
    return {
        "style_id": safe_slug(style_name),
        "style_name": style_name,
        "version": "1.0",
        "category": "Creator-Inspired Faceless Video",
        "description": custom_prompt or "Reusable creator-style profile generated from user inputs.",
        "sources": sources,
        "core_identity": {
            "narrative_style": "second_person_pov",
            "viewer_role": "main_character",
            "immersion_level": "medium",
            "emotional_feel": ["curious", "cinematic", "reflective"],
            "tone": "clear cinematic narration",
        },
        "topics": ["creator-inspired stories", "faceless explainers", "immersive scenarios"],
        "title_patterns": ["Your Life as a _____", "POV: You Are a _____"],
        "hook_style": {
            "type": "direct immersion",
            "length_seconds": 5,
            "pattern": ["direct statement", "sensory detail", "stakes"],
        },
        "story_structure": {
            "intro": {"duration_percent": 10, "purpose": "hook the viewer"},
            "development": {"duration_percent": 55, "purpose": "build the world and routine"},
            "shift": {"duration_percent": 25, "purpose": "add emotional or narrative turn"},
            "ending": {"duration_percent": 10, "purpose": "land a memorable final beat"},
        },
        "visual_style": {
            "perspective": "cinematic POV",
            "lighting": ["cinematic lighting"],
            "color_palette": [visual_aesthetic or "balanced natural colors"],
            "composition": {"focus": "subject and environment", "framing": "immersive"},
        },
        "scene_system": {
            "default_scene_duration": 10,
            "scene_transition": ["fade", "slow dissolve"],
            "camera_motion": ["slow zoom", "slow pan", "depth parallax"],
        },
        "image_prompt_rules": {
            "must_include": ["cinematic lighting", "high detail", "clear composition"],
            "avoid": ["low detail", "visual clutter"],
        },
    }
