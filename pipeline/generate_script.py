from typing import Any

from helpers.call_llm import call_llm


def generate_script(
    topic: str,
    style: dict[str, Any],
    video_minutes: int = 1,
    provider: str | None = None,
) -> dict[str, Any]:
    target_words = video_minutes * 125
    system = (
        "You are a cinematic faceless-video scriptwriter. Write immersive narration "
        "that follows the supplied creator style and avoids copying any real creator verbatim."
    )
    prompt = f"""
Topic: {topic}
Target length: {video_minutes} minute(s)
Target words: about {target_words} words
Style profile: {style}

Return a complete narration only. Use short sensory paragraphs and a quiet emotional arc.
Do not include labels, notes, directions, markdown, or timing comments.
"""
    result = call_llm(prompt, system=system, provider=provider)
    narration = result.text.strip() or _fallback_script(topic, style, video_minutes)
    narration = _fit_word_budget(narration, target_words)
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
    if video_minutes <= 1:
        return "\n\n".join(
            [
                f"You wake up as a medieval baker before the town has opened its eyes.",
                "The kitchen is warm, the table is dusty with flour, and the first loaves are already waiting for your hands.",
                "You knead, fold, and listen to the oven breathe behind you.",
                "People will remember the bread, not the tired person who made it.",
                "Still, for one quiet moment, the whole street depends on this small room, this fire, and you.",
                "Tomorrow will begin the same way. Before sunrise. Before applause. Before anyone knows your name.",
            ]
        )
    if any(word in topic.lower() for word in ("restaurant", "cafe", "shop", "store")):
        return _restaurant_script(topic, video_minutes)
    return "\n\n".join(
        [
            f"You wake up inside the world of {topic}. The day has already started without asking your permission.",
            f"The room is quiet, but every object seems to know its job. Your hands move first. Your thoughts arrive later.",
            f"You follow the small rituals that keep this life together. The light changes slowly. The work repeats itself, and somehow the repetition begins to feel like a language.",
            f"By the middle of the day, the weight of this life becomes clear. Not dramatic. Not loud. Just present in the corners, in the pauses, in the things nobody else notices.",
            f"Evening comes softly. You understand that {topic} is not only a role, but a way of being seen by the world.",
            f"And tomorrow, before sunrise, you will begin again. The same room. The same quiet. The same strange comfort of being exactly here.",
        ]
    )


def _restaurant_script(topic: str, video_minutes: int) -> str:
    beats = [
        (
            "You wake up while the street is still blue and quiet. "
            "The restaurant key feels cold in your hand. When the metal shutter rises, the sound rolls down the empty road like an announcement that the day has begun."
        ),
        (
            "Inside, everything waits for you. The chairs are upside down on the tables, the counter smells faintly of yesterday's coffee, and the kitchen is dark except for one tired bulb above the sink."
        ),
        (
            "You turn on the lights one by one. The room changes from a closed box into a place where people will sit, talk, complain, laugh, and leave behind crumbs you will clean after sunset."
        ),
        (
            "The first job is not cooking. It is remembering. You check the cash drawer, wipe the glass door, fill the water bottles, count the bread, and hope nothing important was forgotten last night."
        ),
        (
            "By six, the kitchen starts breathing. Oil warms in the pan, steam climbs from the kettle, and the first chopped onions sting your eyes before the first customer has even arrived."
        ),
        (
            "A delivery worker passes the window. A bus sighs at the corner. Someone looks at your sign, slows down, and keeps walking. You pretend not to notice, but you always notice."
        ),
        (
            "Then the first customer comes in. They do not know they are first. They only ask for something hot, something quick, something normal. To you, it feels like the restaurant has finally woken up."
        ),
        (
            "The morning becomes a chain of tiny emergencies. A spoon is missing, the card machine freezes, one table wants extra sauce, and the bread you thought would last until noon is disappearing too fast."
        ),
        (
            "Still, there are small rewards. The quiet nod from someone who likes the food. The warm plate leaving your hands. The second when the room is full and every chair has a reason to exist."
        ),
        (
            "Around midday, you stop hearing individual sounds. The doorbell, the orders, the pan, the voices, the chairs, the register, all of it becomes one moving machine, and somehow you are inside it."
        ),
        (
            "You think about closing for one minute, just to breathe. But another person walks in, and your face becomes polite before your body has time to be tired."
        ),
        (
            "By afternoon, the rush fades. Plates come back empty. The floor is marked with footprints. The kitchen smells like oil, soap, and effort. You eat standing up because sitting down feels too official."
        ),
        (
            "Evening brings a softer kind of work. You refill, reset, wipe, count, and listen to the room become hollow again. Every table looks innocent once nobody is sitting at it."
        ),
        (
            "When you lock the door, the restaurant becomes quiet in a different way. Not asleep, exactly. More like it is holding its breath until you return."
        ),
        (
            "Tomorrow morning, the key will feel cold again. The street will be empty again. And you will open the door as if this small place depends on you, because in a way, it does."
        ),
    ]
    target_paragraphs = max(6, min(len(beats), video_minutes * 3))
    return "\n\n".join(beats[:target_paragraphs])


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
