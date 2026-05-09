from html import escape
from pathlib import Path


def generate_images(scenes: list[dict], frames_dir: Path) -> list[dict]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for scene in scenes:
        frame_path = frames_dir / f"scene_{scene['scene_number']:03}.svg"
        frame_path.write_text(_scene_svg(scene), encoding="utf-8")
        results.append(
            {
                "scene_number": scene["scene_number"],
                "status": "created",
                "path": str(frame_path),
                "kind": "illustrated_scene_svg",
                "prompt": scene["image_prompt"],
            }
        )
    return results


def _scene_svg(scene: dict) -> str:
    seed = int(scene["scene_number"])
    glow_x = 900 + (seed % 3) * 55
    glow_y = 150 + (seed % 4) * 38
    table_y = 510 + (seed % 2) * 14
    steam_shift = (seed % 5) * 12
    caption = escape(_short_caption(scene.get("narration", "")))
    motion = escape(scene.get("camera_motion", "slow zoom"))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs>
    <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#32281f"/>
      <stop offset="52%" stop-color="#594632"/>
      <stop offset="100%" stop-color="#1d1712"/>
    </linearGradient>
    <radialGradient id="fire" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#ffe6a8"/>
      <stop offset="48%" stop-color="#d98736"/>
      <stop offset="100%" stop-color="#3b160c"/>
    </radialGradient>
    <style>
      .caption {{ font: 600 30px Arial, sans-serif; fill: #fff7e5; }}
      .meta {{ font: 700 18px Arial, sans-serif; fill: #f3c982; letter-spacing: 2px; }}
    </style>
  </defs>
  <rect width="1280" height="720" fill="url(#wall)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#140f0b" opacity="0.18"/>
  <circle cx="{glow_x}" cy="{glow_y}" r="270" fill="#f4c06c" opacity="0.16"/>
  <rect x="705" y="130" width="350" height="310" rx="160" fill="#20140d"/>
  <rect x="745" y="170" width="270" height="225" rx="115" fill="url(#fire)"/>
  <ellipse cx="880" cy="414" rx="205" ry="38" fill="#120d0a"/>
  <rect x="96" y="{table_y}" width="1088" height="118" rx="20" fill="#5d3c22"/>
  <rect x="96" y="{table_y}" width="1088" height="28" rx="14" fill="#8f6840" opacity="0.85"/>
  <ellipse cx="360" cy="{table_y}" rx="150" ry="42" fill="#d49a54"/>
  <ellipse cx="360" cy="{table_y - 14}" rx="142" ry="48" fill="#e8bd72"/>
  <path d="M230 {table_y - 18} C275 {table_y - 64}, 438 {table_y - 64}, 492 {table_y - 18}" fill="none" stroke="#fff0c9" stroke-width="8" opacity="0.45"/>
  <ellipse cx="570" cy="{table_y - 4}" rx="78" ry="35" fill="#bb7938"/>
  <ellipse cx="690" cy="{table_y - 10}" rx="92" ry="38" fill="#c78944"/>
  <ellipse cx="815" cy="{table_y - 2}" rx="76" ry="32" fill="#b97133"/>
  <path d="M274 {table_y + 52} C330 {table_y + 8}, 445 {table_y + 6}, 506 {table_y + 48}" fill="#d9b18a"/>
  <path d="M760 {table_y + 56} C820 {table_y + 12}, 935 {table_y + 10}, 994 {table_y + 52}" fill="#d9b18a"/>
  <rect x="178" y="160" width="250" height="205" rx="6" fill="#191512" opacity="0.82"/>
  <rect x="202" y="184" width="92" height="72" fill="#f7d28a" opacity="0.72"/>
  <rect x="310" y="184" width="92" height="72" fill="#f7d28a" opacity="0.54"/>
  <rect x="202" y="272" width="92" height="72" fill="#f7d28a" opacity="0.4"/>
  <rect x="310" y="272" width="92" height="72" fill="#f7d28a" opacity="0.28"/>
  <path d="M520 {390 - steam_shift} C486 {340 - steam_shift}, 560 {310 - steam_shift}, 526 {260 - steam_shift}" fill="none" stroke="#f8e7c8" stroke-width="9" opacity="0.28"/>
  <path d="M610 {374 - steam_shift} C570 {320 - steam_shift}, 660 {292 - steam_shift}, 624 {240 - steam_shift}" fill="none" stroke="#f8e7c8" stroke-width="7" opacity="0.22"/>
  <path d="M115 78 L1170 78 L1170 646 L115 646 Z" fill="none" stroke="#d8b06d" stroke-width="3" opacity="0.5"/>
  <rect x="90" y="590" width="1100" height="70" rx="8" fill="#11100f" opacity="0.68"/>
  <text x="122" y="635" class="caption">{caption}</text>
  <text x="1010" y="116" class="meta">{motion}</text>
</svg>
"""


def _short_caption(text: str) -> str:
    words = text.split()
    if len(words) <= 16:
        return text
    return " ".join(words[:16]) + "..."
