import uuid
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from backend.services.storage_service import StorageService
from backend.services.pipeline_orchestrator import trigger_background_pipeline, get_lecture_status
from backend.config import UPLOAD_DIR

router = APIRouter(prefix="/api/lectures", tags=["lectures"])

@router.get("")
async def list_lectures():
    """Returns catalog of all processed lectures."""
    lectures = StorageService.list_all_lectures()
    return {"success": True, "count": len(lectures), "lectures": lectures}

@router.get("/{lecture_id}")
async def get_lecture(lecture_id: str):
    """Returns details for a specific lecture."""
    metadata = StorageService.get_lecture_metadata(lecture_id)
    if not metadata:
        raise HTTPException(status_code=404, detail=f"Lecture '{lecture_id}' not found")
    return {"success": True, "lecture": metadata}

@router.get("/{lecture_id}/metadata")
async def get_lecture_event_metadata(lecture_id: str):
    """Returns Contract 3 per-event diagram audio metadata for intelligent player."""
    metadata = StorageService.get_lecture_metadata(lecture_id)
    if not metadata:
        raise HTTPException(status_code=404, detail=f"Metadata for lecture '{lecture_id}' not found")
    return {
        "lecture_id": lecture_id,
        "title": metadata.get("title", ""),
        "subject": metadata.get("subject", ""),
        "events": metadata.get("events", [])
    }

@router.get("/{lecture_id}/status")
async def check_status(lecture_id: str):
    """Check processing status for a lecture."""
    status_info = get_lecture_status(lecture_id)
    return {"success": True, "status_info": status_info}

@router.post("/upload")
async def upload_lecture(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Form("Untitled Lecture"),
    subject: str = Form("Physics"),
    description: str = Form("")
):
    """
    Accepts video upload, saves file, and triggers background processing pipeline.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file missing filename")

    lecture_id = f"lec_{str(uuid.uuid4())[:8]}"
    ext = Path(file.filename).suffix or ".mp4"
    video_filename = f"{lecture_id}{ext}"
    saved_video_path = UPLOAD_DIR / video_filename

    try:
        contents = await file.read()
        with open(saved_video_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save video: {e}")

    # Seed initial metadata
    initial_metadata = {
        "lecture_id": lecture_id,
        "title": title,
        "subject": subject,
        "description": description,
        "video_url": f"/storage/uploads/{video_filename}",
        "status": "processing",
        "events_count": 0,
        "events": []
    }
    StorageService.save_lecture_metadata(lecture_id, initial_metadata)

    # Trigger async background pipeline execution
    background_tasks.add_task(
        trigger_background_pipeline,
        video_path=str(saved_video_path),
        lecture_id=lecture_id,
        title=title,
        subject=subject,
        description=description
    )

    return {
        "success": True,
        "message": "Lecture uploaded successfully. AI processing started.",
        "lecture_id": lecture_id,
        "status_url": f"/api/lectures/{lecture_id}/status"
    }
