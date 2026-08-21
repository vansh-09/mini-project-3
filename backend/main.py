import os
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.services import diagram_to_speech
from backend.config import BASE_DIR, STORAGE_DIR, UPLOAD_DIR, AUDIO_DIR, SAMPLES_DIR, STATIC_DIR
from backend.routes.lectures import router as lectures_router
from backend.routes.status import router as status_router

load_dotenv()

app = FastAPI(
    title="EduVision — Accessible Diagram to Speech Pipeline",
    description="Converts educational diagrams & lecture video frames into bilingual spoken audio narratives.",
    version="1.0.0"
)

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static storage routes
app.mount("/static/sample_diagrams", StaticFiles(directory=str(SAMPLES_DIR)), name="sample_diagrams")
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Include Modular API Routers
app.include_router(lectures_router)
app.include_router(status_router)

@app.get("/")
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return JSONResponse({"message": "EduVision API is active. Access catalog via /api/lectures"})

# Single diagram upload route (legacy & demo endpoint)
@app.post("/api/process")
async def process_uploaded_diagram(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPG, WEBP, etc.)")

    ext = Path(file.filename).suffix or ".png"
    file_id = str(uuid.uuid4())[:8]
    saved_image_name = f"diagram_{file_id}{ext}"
    saved_image_path = UPLOAD_DIR / saved_image_name

    try:
        contents = await file.read()
        with open(saved_image_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded image: {e}")

    try:
        understanding = diagram_to_speech.detect_and_understand(str(saved_image_path))
        explanation = diagram_to_speech.generate_explanation(understanding)

        audio_filename = f"explanation_{file_id}.mp3"
        audio_target_path = AUDIO_DIR / audio_filename
        diagram_to_speech.text_to_speech(explanation, str(audio_target_path))

        return {
            "success": True,
            "understanding": understanding,
            "explanation": explanation,
            "image_url": f"/storage/uploads/{saved_image_name}",
            "audio_url": f"/storage/audio/{audio_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
