from pathlib import Path


def assemble_video(job_dir: Path) -> dict:
    return {
        "status": "skipped",
        "reason": "Final FFmpeg rendering is reserved for Phase 2.",
        "final_video_path": str(job_dir / "final_video.mp4"),
    }
