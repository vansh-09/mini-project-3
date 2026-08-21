from fastapi import APIRouter
from backend.services.storage_service import StorageService

router = APIRouter(prefix="/api/status", tags=["status"])

@router.get("")
async def system_status():
    lectures = StorageService.list_all_lectures()
    total_events = sum(l.get("events_count", 0) for l in lectures)
    return {
        "status": "healthy",
        "service": "EduVision Diagram-to-Speech API",
        "version": "1.0.0",
        "total_lectures": len(lectures),
        "total_audio_descriptions": total_events
    }
