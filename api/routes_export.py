from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from config import EXPORTS_DIR
from helpers.file_utils import read_json

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get("")
def list_exports() -> list[dict[str, Any]]:
    if not EXPORTS_DIR.exists():
        return []
    jobs = []
    for metadata_file in sorted(EXPORTS_DIR.glob("job_*/metadata.json"), reverse=True):
        jobs.append(read_json(metadata_file))
    return jobs


@router.get("/{job_id}")
def get_export(job_id: str) -> dict[str, Any]:
    metadata_file = EXPORTS_DIR / job_id / "metadata.json"
    if not metadata_file.exists():
        raise HTTPException(status_code=404, detail=f"Export not found: {job_id}")
    return read_json(metadata_file)


@router.get("/{job_id}/scenes")
def get_export_scenes(job_id: str) -> list[dict[str, Any]]:
    scenes_file = EXPORTS_DIR / job_id / "scenes.json"
    if not scenes_file.exists():
        raise HTTPException(status_code=404, detail=f"Scenes not found for export: {job_id}")
    return read_json(scenes_file)


@router.get("/{job_id}/script")
def get_export_script(job_id: str) -> FileResponse:
    script_file = EXPORTS_DIR / job_id / "script.txt"
    if not script_file.exists():
        raise HTTPException(status_code=404, detail=f"Script not found for export: {job_id}")
    return FileResponse(script_file)


@router.get("/{job_id}/video")
def get_export_video(job_id: str) -> FileResponse:
    video_file = EXPORTS_DIR / job_id / "final_video.mp4"
    if not video_file.exists():
        raise HTTPException(status_code=404, detail="Video rendering is not available for this job yet.")
    return FileResponse(video_file, media_type="video/mp4")
