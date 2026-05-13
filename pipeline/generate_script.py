from typing import Any

from helpers.call_llm import call_llm


def generate_script(
    title: str,
    base_idea: str,
    video_minutes: int = 8,
    provider: str | None = None,
) -> dict[str, Any]:
    target_words = video_minutes * 125
    system = (
        "You are an elite YouTube scriptwriter for high-retention faceless storytelling videos. "
        "Write in second person using short, cinematic, punchy lines."
    )
    prompt = f"""
Video title: {title}
Base idea: {base_idea}

Write a full {video_minutes} minute YouTube script.
Target words: about {target_words} words.

Use an invisible level-based progression structure.
Each stage should feel like growth, pressure, risk, consequences, or deeper emotional involvement.

Rules:
- Start immediately. No long intro.
- Do not physically write "Level 1", "Level 2", or level labels in the script.
- Use second-person perspective: "you".
- Use short, impactful sentences.
- Keep a dark, serious, cinematic, immersive tone.
- Show increasing stakes.
- Include money pressure, risk, consequences, emotional shifts, and realistic details.
- Every sentence should move the story forward.
- End with a powerful consequence, downfall, twist, or cycle continuation.

Return a complete narration only. Use short sensory paragraphs and a quiet emotional arc.
Do not include labels, notes, directions, markdown, or timing comments.
"""
    try:
        result = call_llm(prompt, system=system, provider=provider)
        narration = result.text.strip() or _fallback_script(title, base_idea, video_minutes)
    except Exception as exc:
        result = type("LLMFallback", (), {"provider": "fallback", "model": exc.__class__.__name__})()
        narration = _fallback_script(title, base_idea, video_minutes)
    narration = _fit_word_budget(narration, target_words)
    return {
        "title": title,
        "base_idea": base_idea,
        "narration": narration,
        "provider": result.provider,
        "model": result.model,
    }


def _fallback_script(title: str, base_idea: str, video_minutes: int) -> str:
    if video_minutes <= 1:
        return "\n\n".join(
            [
                f"You step into {title}.",
                base_idea,
                "At first, it feels simple.",
                "Then the pressure starts showing up in small ways.",
                "Money becomes tight. Time becomes smaller. Sleep becomes something you borrow.",
                "By the end, you understand that surviving the system is not the same as winning it.",
            ]
        )
    beats = _neet_beats(title, base_idea) if "neet" in title.lower() else _generic_beats(title, base_idea)
    target_paragraphs = max(8, min(len(beats), video_minutes * 3))
    return "\n\n".join(beats[:target_paragraphs])


def _neet_beats(title: str, base_idea: str) -> list[str]:
    return [
        (
            "You finish tenth standard and everyone says the same sentence. "
            "If you are serious about becoming a doctor, you go to Kota."
        ),
        (
            "So you pack two bags, one water bottle, and a version of yourself that still believes hard work has a clean result."
        ),
        (
            "The hostel room is smaller than the photos. The mattress is thin. The fan makes noise. The city does not wait for you to adjust."
        ),
        (
            "Your first lecture starts before your body understands the schedule. Biology feels manageable. Physics does not. Chemistry moves like a train you almost catch."
        ),
        (
            "Food becomes the first enemy. The mess dal is watery. The rotis are cold. You call home and say it is fine because your mother already sounds worried."
        ),
        (
            "Money becomes the second enemy. Coaching fees are paid. Hostel rent is due. Test series costs extra. Even a notebook starts feeling expensive."
        ),
        (
            "You learn the map of Kota through pressure. Coaching building. Hostel gate. Mess line. Medical shop. Photocopy counter. Same roads. Same tired faces."
        ),
        (
            "The first minor test breaks your confidence quietly. You do not fail loudly. You just score less than the students who look like they are not even trying."
        ),
        (
            "You start waking earlier. You stop watching videos. You delete games. You tell yourself discipline will fix everything."
        ),
        (
            "But discipline does not stop loneliness. At night, the room becomes too quiet. Other students cry on calls. Some pretend they are stronger than they are."
        ),
        (
            "Your parents ask about marks. You talk about improvement. You do not mention the panic before every test or the guilt after every bad result."
        ),
        (
            "Months pass. The syllabus becomes heavier. Revision becomes a mountain. Every student starts calculating rank, cutoff, category, luck, and backup plans."
        ),
        (
            "On exam day, your hands are cold. The paper is not impossible. That makes it worse. Because every mistake feels personal."
        ),
        (
            "The result comes like a number with no emotion. Not enough. Not this year. Not after all that rent, all those calls, all those mornings."
        ),
        (
            "Then someone says the next sentence. Take a drop. One more year. One more room. One more chance to become the person everyone already announced you would be."
        ),
    ]


def _generic_beats(title: str, base_idea: str) -> list[str]:
    return [
        f"You enter the world of {title} with one simple belief.",
        base_idea,
        "At first, the rules look clear.",
        "Then the small costs begin.",
        "You lose time first.",
        "Then money.",
        "Then the easy version of your confidence.",
        "Every day adds a new task, a new mistake, and a new reason not to quit.",
        "People outside the system think progress is visible.",
        "Inside it, progress feels like surviving one more day without falling apart.",
        "The deeper you go, the more normal the pressure becomes.",
        "By the end, you are not the same person who started.",
    ]


def _fit_word_budget(narration: str, target_words: int) -> str:
    words = narration.split()
    max_words = int(target_words * 1.12)
    if len(words) <= max_words:
        return narration

    sentences = [part.strip() for part in narration.replace("\n", " ").split(".") if part.strip()]
    kept: list[str] = []
    count = 0
    for sentence in sentences:
        sentence_words = len(sentence.split())
        if count + sentence_words > max_words:
            break
        kept.append(sentence)
        count += sentence_words
    return ". ".join(kept).strip() + "."
