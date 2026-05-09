from pathlib import Path

from helpers.generate_image import generate_scene_image


def generate_images(
    scenes: list[dict],
    frames_dir: Path,
    job_seed: int | None = None,
    max_images: int | None = None,
) -> list[dict]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    base_seed = job_seed or 1000
    results = []
    for scene in scenes:
        if max_images is not None and len(results) >= max_images:
            results.append(
                {
                    "scene_number": scene["scene_number"],
                    "status": "pending",
                    "path": None,
                    "provider": None,
                    "kind": "faceless_cartoon_image",
                    "visual_action": scene.get("visual_action"),
                    "prompt": scene["image_prompt"],
                }
            )
            continue

        image_path = frames_dir / f"scene_{scene['scene_number']:03}.png"
        result = generate_scene_image(
            scene["image_prompt"],
            image_path,
            seed=base_seed + scene["scene_number"],
        )
        if result["status"] != "created":
            fallback_path = frames_dir / f"scene_{scene['scene_number']:03}.svg"
            fallback_path.write_text(_cartoon_scene_svg(scene), encoding="utf-8")
            result = {
                "status": "created",
                "provider": "svg_fallback",
                "path": str(fallback_path),
                "error": result.get("error"),
            }
        results.append(
            {
                "scene_number": scene["scene_number"],
                "status": result["status"],
                "path": result["path"],
                "provider": result.get("provider"),
                "kind": "faceless_cartoon_image",
                "visual_action": scene.get("visual_action"),
                "prompt": scene["image_prompt"],
            }
        )
    return results


def _cartoon_scene_svg(scene: dict) -> str:
    seed = int(scene["scene_number"])
    if seed % 2:
        return _kitchen_scene(seed)
    return _living_room_scene(seed)


def _kitchen_scene(seed: int) -> str:
    man_x = 360 + (seed % 2) * 20
    woman_x = 770 - (seed % 3) * 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <style>
      .line {{ stroke:#151515; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ stroke:#151515; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
      .tile {{ fill:#f7f4ee; stroke:#333; stroke-width:2; }}
    </style>
  </defs>
  <rect width="1280" height="720" fill="#f2d5ad"/>
  <rect x="0" y="210" width="1280" height="240" fill="#f8f8f5"/>
  {_tiles()}
  <rect x="0" y="0" width="210" height="180" fill="#dda76d" class="line"/>
  <rect x="20" y="20" width="170" height="116" fill="#e6b278" class="thin"/>
  <rect x="830" y="0" width="430" height="200" fill="#dda76d" class="line"/>
  <rect x="858" y="22" width="150" height="130" fill="#e6b278" class="thin"/>
  <rect x="1042" y="22" width="150" height="130" fill="#e6b278" class="thin"/>
  <rect x="132" y="352" width="1010" height="112" fill="#7f5638" class="line"/>
  <rect x="150" y="464" width="960" height="128" fill="#d79a61" class="line"/>
  <rect x="690" y="96" width="180" height="128" fill="#dceef8" class="line"/>
  <line x1="780" y1="100" x2="780" y2="220" class="thin"/>
  <line x1="694" y1="160" x2="866" y2="160" class="thin"/>
  <ellipse cx="650" cy="44" rx="135" ry="48" fill="#f3c88a" class="line"/>
  <circle cx="650" cy="42" r="26" fill="#fff6d7" class="thin"/>
  <path d="M236 384 q42 -48 84 0" fill="none" class="line"/>
  <rect x="216" y="382" width="130" height="70" rx="16" fill="#c9c3b7" class="line"/>
  {_person(man_x, 250, "#5d83bd", "thinking", False)}
  {_person(woman_x, 258, "#efa3bd", "neutral", True)}
  <rect x="80" y="590" width="1120" height="112" fill="#c58b55" class="line"/>
  <rect x="120" y="620" width="150" height="52" fill="#f3eadf" class="thin"/>
  <rect x="304" y="628" width="120" height="42" fill="#9eb7cf" class="thin"/>
  <rect x="450" y="618" width="142" height="55" fill="#f2d0d9" class="thin"/>
  <rect x="680" y="604" width="180" height="62" fill="#eaf4f5" class="thin"/>
  <path d="M700 632 l70 -18 l65 30 l-78 14 z" fill="#91b5d5" class="thin"/>
  <rect x="940" y="608" width="205" height="72" fill="#edf3f7" class="line"/>
</svg>"""


def _living_room_scene(seed: int) -> str:
    question_marks = "".join(
        f'<text x="{770 + index * 70}" y="{95 - (index % 2) * 24}" font-size="54" font-family="Arial" fill="#ffffff" stroke="#333" stroke-width="2">?</text>'
        for index in range(4)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <pattern id="flowers" width="58" height="58" patternUnits="userSpaceOnUse">
      <rect width="58" height="58" fill="#e9d7b5"/>
      <circle cx="17" cy="20" r="5" fill="#d79b75"/>
      <circle cx="24" cy="22" r="4" fill="#8fae8a"/>
      <circle cx="40" cy="38" r="5" fill="#b9c0d8"/>
      <path d="M13 31 q10 8 20 0" fill="none" stroke="#8c956b" stroke-width="2"/>
    </pattern>
    <style>
      .line {{ stroke:#151515; stroke-width:5; stroke-linecap:round; stroke-linejoin:round; }}
      .thin {{ stroke:#151515; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }}
    </style>
  </defs>
  <rect width="1280" height="720" fill="url(#flowers)"/>
  <rect x="0" y="530" width="1280" height="190" fill="#af7652" class="line"/>
  <rect x="450" y="358" width="520" height="170" rx="38" fill="#375b8a" class="line"/>
  <rect x="495" y="315" width="430" height="130" rx="34" fill="#476da1" class="line"/>
  <circle cx="520" cy="522" r="50" fill="#375b8a" class="line"/>
  <circle cx="940" cy="522" r="50" fill="#375b8a" class="line"/>
  <rect x="172" y="402" width="170" height="118" fill="#7d4d30" class="line"/>
  <ellipse cx="257" cy="385" rx="60" ry="36" fill="#d5a064" class="line"/>
  <path d="M240 340 q25 -32 50 0" fill="none" class="thin"/>
  <rect x="1010" y="210" width="80" height="250" fill="#e0a75e" class="line"/>
  <path d="M960 210 h180 l-34 -110 h-112 z" fill="#f0cf86" class="line"/>
  <rect x="70" y="180" width="115" height="145" fill="#92735b" class="line"/>
  <rect x="90" y="202" width="74" height="80" fill="#cfc7b8" class="thin"/>
  {_person(405, 215, "#458c94", "talking", True)}
  {_person(825, 225, "#477a42", "confused", False)}
  {question_marks}
</svg>"""


def _person(x: int, y: int, shirt: str, expression: str, hair: bool) -> str:
    hair_shape = ""
    if hair:
        hair_shape = f"""
  <path d="M{x - 88} {y + 64} q22 -118 118 -116 q94 20 96 126 v142 h-228 z" fill="#202124" class="line"/>
  <path d="M{x - 56} {y + 26} q54 56 128 0 q-38 -74 -128 0" fill="#202124"/>
"""
    mouth = {
        "thinking": f'<path d="M{x - 2} {y + 82} q26 -8 45 5" fill="none" class="thin"/>',
        "talking": f'<path d="M{x - 10} {y + 84} q28 16 58 0" fill="none" class="thin"/>',
        "confused": f'<path d="M{x - 4} {y + 84} q24 10 48 -2" fill="none" class="thin"/>',
        "neutral": f'<line x1="{x + 5}" y1="{y + 86}" x2="{x + 54}" y2="{y + 86}" class="thin"/>',
    }[expression]
    hand = (
        f'<path d="M{x - 92} {y + 250} q-42 -48 -2 -82 q34 -6 54 28" fill="#fff" class="line"/>'
        if expression in ("thinking", "talking")
        else f'<ellipse cx="{x - 72}" cy="{y + 266}" rx="42" ry="28" fill="#fff" class="line"/>'
    )
    return f"""
  {hair_shape}
  <path d="M{x - 100} {y + 390} v-160 q0 -78 96 -82 h72 q98 8 105 84 v158 z" fill="{shirt}" class="line"/>
  <circle cx="{x}" cy="{y + 72}" r="92" fill="#ffffff" class="line"/>
  <path d="M{x - 76} {y + 78} q12 68 66 86" fill="none" stroke="#c6d9ef" stroke-width="15" opacity="0.75"/>
  <ellipse cx="{x - 36}" cy="{y + 72}" rx="9" ry="22" fill="#050505"/>
  <ellipse cx="{x + 50}" cy="{y + 74}" rx="9" ry="22" fill="#050505"/>
  {mouth}
  <path d="M{x - 94} {y + 236} q-48 48 -70 116" fill="none" class="line"/>
  <path d="M{x + 104} {y + 238} q62 52 82 122" fill="none" class="line"/>
  {hand}
  <ellipse cx="{x + 122}" cy="{y + 348}" rx="42" ry="28" fill="#fff" class="line"/>
"""


def _tiles() -> str:
    rows = []
    for y in range(230, 430, 34):
        offset = 0 if (y // 34) % 2 else 45
        for x in range(-offset, 1280, 90):
            rows.append(f'<rect x="{x}" y="{y}" width="90" height="34" class="tile"/>')
    return "\n  ".join(rows)
