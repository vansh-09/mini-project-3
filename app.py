import os
import uuid
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

import diagram_to_speech

load_dotenv()

app = FastAPI(title="EduVision Diagram to Speech API")

# Directories setup
BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
AUDIO_DIR = STORAGE_DIR / "audio"
SAMPLES_DIR = BASE_DIR / "sample_diagrams"
STATIC_DIR = BASE_DIR / "static"

for d in [STORAGE_DIR, UPLOAD_DIR, AUDIO_DIR, SAMPLES_DIR, STATIC_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static/sample_diagrams", StaticFiles(directory=str(SAMPLES_DIR)), name="sample_diagrams")
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")


@app.get("/")
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.is_file():
        return FileResponse(index_file)
    return JSONResponse({"message": "EduVision API is active. Upload diagrams via /api/process"})


@app.post("/api/process")
async def process_uploaded_diagram(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPG, WEBP, etc.)")

    ext = Path(file.filename).suffix or ".png"
    file_id = str(uuid.uuid4())[:8]
    saved_image_name = f"diagram_{file_id}{ext}"
    saved_image_path = UPLOAD_DIR / saved_image_name

    # Save uploaded file
    try:
        contents = await file.read()
        with open(saved_image_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded image: {e}")

    # Process pipeline
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


@app.post("/api/process-sample/{sample_name}")
async def process_sample_diagram(sample_name: str):
    sample_path = SAMPLES_DIR / sample_name
    if not sample_path.is_file():
        raise HTTPException(status_code=404, detail=f"Sample diagram '{sample_name}' not found")

    file_id = str(uuid.uuid4())[:8]
    try:
        understanding = diagram_to_speech.detect_and_understand(str(sample_path))
        explanation = diagram_to_speech.generate_explanation(understanding)

        audio_filename = f"sample_{file_id}.mp3"
        audio_target_path = AUDIO_DIR / audio_filename
        diagram_to_speech.text_to_speech(explanation, str(audio_target_path))

        return {
            "success": True,
            "understanding": understanding,
            "explanation": explanation,
            "image_url": f"/static/sample_diagrams/{sample_name}",
            "audio_url": f"/storage/audio/{audio_filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
