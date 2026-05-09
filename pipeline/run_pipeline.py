from typing import Any
import zlib

from config import DEFAULT_STYLE, DEFAULT_VIDEO_MINUTES, EXPORTS_DIR
from helpers.file_utils import ensure_dir, utc_job_id, write_json, write_text
from helpers.load_style import load_style
from pipeline.assemble_video import assemble_video
from pipeline.generate_audio import generate_audio
from pipeline.generate_captions import generate_captions
from pipeline.generate_images import generate_images
from pipeline.generate_scenes import generate_scenes
from pipeline.generate_script import generate_script


def run_pipeline(
    topic: str,
    style_name: str = DEFAULT_STYLE,
    video_minutes: int = DEFAULT_VIDEO_MINUTES,
    scene_duration: int | None = None,
    provider: str | None = None,
    max_images: int | None = None,
) -> dict[str, Any]:
    style = load_style(style_name)
    job_id = utc_job_id()
    job_dir = ensure_dir(EXPORTS_DIR / job_id)
    frames_dir = ensure_dir(job_dir / "frames")
    audio_dir = ensure_dir(job_dir / "audio")

    script = generate_script(topic, style, video_minutes, provider=provider)
    scenes = generate_scenes(script, style, video_minutes, scene_duration)
    total_duration = sum(int(scene["duration"]) for scene in scenes)
    job_seed = zlib.crc32(f"{topic}:{style_name}".encode("utf-8")) % 100000

    write_text(job_dir / "script.txt", script["narration"])
    write_json(job_dir / "script.json", script)
    write_json(job_dir / "scenes.json", scenes)

    image_limit = max_images if max_images is not None else (6 if len(scenes) > 12 else None)
    image_result = generate_images(scenes, frames_dir, job_seed=job_seed, max_images=image_limit)
    audio_result = generate_audio(script, audio_dir, total_duration)
    captions_result = generate_captions(scenes, audio_dir)
    render_result = assemble_video(job_dir)

    metadata = {
        "job_id": job_id,
        "topic": topic,
        "style_name": style.get("style_name", style_name),
        "style_id": style_name,
        "video_minutes": video_minutes,
        "scene_count": len(scenes),
        "scene_duration": scenes[0]["duration"] if scenes else scene_duration,
        "total_duration": total_duration,
        "job_seed": job_seed,
        "character_profile": scenes[0].get("character_profile") if scenes else None,
        "image_generation_limit": image_limit,
        "llm_provider": script["provider"],
        "llm_model": script["model"],
        "phases": {
            "images": image_result,
            "audio": audio_result,
            "captions": captions_result,
            "render": render_result,
        },
    }

    write_json(job_dir / "metadata.json", metadata)

    return {
        "job_id": job_id,
        "job_dir": str(job_dir),
        "script": script,
        "scenes": scenes,
        "metadata": metadata,
    }
