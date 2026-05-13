from typing import Any
import zlib

from config import DEFAULT_VIDEO_MINUTES, EXPORTS_DIR
from helpers.file_utils import ensure_dir, utc_job_id, write_json, write_text
from pipeline.assemble_video import assemble_video
from pipeline.generate_audio import generate_audio
from pipeline.generate_captions import generate_captions
from pipeline.generate_images import generate_images
from pipeline.generate_scenes import generate_scenes
from pipeline.generate_script import generate_script


def run_pipeline(
    title: str,
    base_idea: str,
    provider: str | None = None,
) -> dict[str, Any]:
    job_id = utc_job_id()
    job_dir = ensure_dir(EXPORTS_DIR / job_id)
    frames_dir = ensure_dir(job_dir / "frames")
    audio_dir = ensure_dir(job_dir / "audio")

    script = generate_script(title, base_idea, DEFAULT_VIDEO_MINUTES, provider=provider)
    scenes = generate_scenes(script, DEFAULT_VIDEO_MINUTES, None)
    total_duration = sum(int(scene["duration"]) for scene in scenes)
    job_seed = zlib.crc32(f"{title}:{base_idea}".encode("utf-8")) % 100000

    write_text(job_dir / "script.txt", script["narration"])
    write_json(job_dir / "script.json", script)
    write_json(job_dir / "scenes.json", scenes)
    for part_number, prompt_part in enumerate(_prompt_parts(scenes, 4), start=1):
        write_json(job_dir / f"image_prompts_part_{part_number}.json", prompt_part)

    image_result = generate_images(scenes, frames_dir, job_seed=job_seed)
    audio_result = generate_audio(script, audio_dir, total_duration)
    captions_result = generate_captions(scenes, audio_dir)
    render_result = assemble_video(job_dir)

    metadata = {
        "job_id": job_id,
        "title": title,
        "base_idea": base_idea,
        "video_minutes": DEFAULT_VIDEO_MINUTES,
        "scene_count": len(scenes),
        "scene_duration": scenes[0]["duration"] if scenes else None,
        "total_duration": total_duration,
        "job_seed": job_seed,
        "character_profile": scenes[0].get("character_profile") if scenes else None,
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


def _prompt_parts(scenes: list[dict[str, Any]], parts: int) -> list[list[dict[str, Any]]]:
    chunk_size = max(1, (len(scenes) + parts - 1) // parts)
    chunks = []
    for index in range(parts):
        chunk = scenes[index * chunk_size : (index + 1) * chunk_size]
        chunks.append(
            [
                {
                    "scene_number": scene["scene_number"],
                    "narration": scene["narration"],
                    "visual_action": scene["visual_action"],
                    "prompt": scene["image_prompt"],
                }
                for scene in chunk
            ]
        )
    return chunks
