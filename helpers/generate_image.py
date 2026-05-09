import base64
from pathlib import Path
from urllib.parse import quote

import requests

from config import AUTOMATIC1111_BASE_URL, IMAGE_HEIGHT, IMAGE_PROVIDER, IMAGE_WIDTH


NEGATIVE_PROMPT = (
    "photorealistic, realistic human face, detailed facial features, horror, gore, "
    "messy lines, low quality, blurry, distorted hands, extra fingers, watermark, text"
)


def generate_scene_image(prompt: str, output_path: Path, seed: int) -> dict:
    provider = IMAGE_PROVIDER.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if provider == "automatic1111":
            return _automatic1111(prompt, output_path, seed)
        if provider == "pollinations":
            return _pollinations(prompt, output_path, seed)
    except requests.RequestException as exc:
        return {"status": "failed", "provider": provider, "error": str(exc)}

    return {"status": "skipped", "provider": provider, "error": f"Unknown image provider: {provider}"}


def _pollinations(prompt: str, output_path: Path, seed: int) -> dict:
    encoded = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&seed={seed}&model=flux&nologo=true"
    )
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    output_path.write_bytes(response.content)
    return {"status": "created", "provider": "pollinations", "path": str(output_path)}


def _automatic1111(prompt: str, output_path: Path, seed: int) -> dict:
    response = requests.post(
        f"{AUTOMATIC1111_BASE_URL}/sdapi/v1/txt2img",
        json={
            "prompt": prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "width": IMAGE_WIDTH,
            "height": IMAGE_HEIGHT,
            "steps": 28,
            "cfg_scale": 6.5,
            "seed": seed,
            "sampler_name": "DPM++ 2M Karras",
        },
        timeout=300,
    )
    response.raise_for_status()
    image = response.json()["images"][0]
    output_path.write_bytes(base64.b64decode(image.split(",", 1)[-1]))
    return {"status": "created", "provider": "automatic1111", "path": str(output_path)}
