import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from backend.config import UPLOAD_DIR, AUDIO_DIR, FRAMES_DIR, METADATA_DIR

class StorageService:
    @staticmethod
    def save_lecture_metadata(lecture_id: str, data: Dict[str, Any]) -> Path:
        filepath = METADATA_DIR / f"{lecture_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    @staticmethod
    def get_lecture_metadata(lecture_id: str) -> Optional[Dict[str, Any]]:
        filepath = METADATA_DIR / f"{lecture_id}.json"
        if not filepath.is_file():
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def list_all_lectures() -> List[Dict[str, Any]]:
        lectures = []
        for file in METADATA_DIR.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    lectures.append(data)
            except Exception:
                continue
        return lectures

    @staticmethod
    def get_lecture_video_path(filename: str) -> Path:
        return UPLOAD_DIR / filename

    @staticmethod
    def get_lecture_frames_dir(lecture_id: str) -> Path:
        frames_path = FRAMES_DIR / lecture_id
        frames_path.mkdir(parents=True, exist_ok=True)
        return frames_path
