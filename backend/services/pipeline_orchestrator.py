import asyncio
from typing import Dict, Any
from backend.services.storage_service import StorageService
from ai_pipeline.process_lecture import LecturePipeline

# Status tracking in memory
PROCESSING_STATUS: Dict[str, Dict[str, Any]] = {}

def trigger_background_pipeline(
    video_path: str,
    lecture_id: str,
    title: str,
    subject: str,
    description: str
):
    """
    Triggers the AI processing pipeline for a lecture with real-time status & percentage updates.
    """
    PROCESSING_STATUS[lecture_id] = {
        "status": "processing",
        "progress_pct": 5,
        "progress_message": "Initializing video upload and frame extractor",
        "lecture_id": lecture_id
    }

    def update_progress(pct: int, msg: str):
        PROCESSING_STATUS[lecture_id] = {
            "status": "processing",
            "progress_pct": pct,
            "progress_message": msg,
            "lecture_id": lecture_id
        }

    try:
        pipeline = LecturePipeline()
        pipeline.process_video(
            video_path=video_path,
            lecture_id=lecture_id,
            title=title,
            subject=subject,
            description=description,
            progress_callback=update_progress
        )
        PROCESSING_STATUS[lecture_id] = {
            "status": "completed",
            "progress_pct": 100,
            "progress_message": "Pipeline finished successfully",
            "lecture_id": lecture_id
        }
    except Exception as e:
        print(f"Pipeline error for lecture {lecture_id}: {e}")
        PROCESSING_STATUS[lecture_id] = {
            "status": "failed",
            "progress_pct": 0,
            "error": str(e),
            "lecture_id": lecture_id
        }

def get_lecture_status(lecture_id: str) -> Dict[str, Any]:
    if lecture_id in PROCESSING_STATUS:
        return PROCESSING_STATUS[lecture_id]
    
    # Check if metadata exists on disk
    meta = StorageService.get_lecture_metadata(lecture_id)
    if meta:
        return {
            "status": "completed",
            "progress_pct": 100,
            "progress_message": "Completed",
            "lecture_id": lecture_id,
            "events_count": meta.get("events_count", 0)
        }
    
    return {"status": "not_found", "progress_pct": 0, "lecture_id": lecture_id}
