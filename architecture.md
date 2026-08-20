# EduVision — Architecture

## 1. High-Level Architecture

EduVision is split into two clearly separated halves that only communicate through a metadata contract:

1. **Offline AI Processing** — turns a raw lecture video into diagram audio descriptions + timestamp metadata. Runs once per uploaded lecture, asynchronously, not in the user-facing request path.
2. **Web Application** — a normal React frontend + FastAPI backend that serves lectures and drives pause → play AD → resume playback using the metadata produced above.

```
                 OFFLINE AI PROCESSING
                        │
        ┌───────────────┴───────────────┐
        ▼                                ▼
   Lecture Video                   AD Metadata
        │                                │
        │                    timestamp + audio files
        │                                │
        └───────────────┬────────────────┘
                         ▼
                    WEB PLAYER
                         │
                         ▼
                  Play lecture
                         │
               Diagram timestamp reached
                         │
                         ▼
                   PAUSE VIDEO
                         │
                         ▼
                    PLAY AD
                         │
                         ▼
                  RESUME VIDEO
```

**Key architectural decision:** the pause/resume behavior is implemented entirely in the web player, not by re-encoding the source MP4. The lecture video stays untouched; the player watches `currentTime` against an events list and pauses/resumes/plays AD audio in JS. This avoids fragile, one-way video re-cutting and keeps the original lecture file reusable if AD content is regenerated or corrected later.

## 2. AI Pipeline (Offline)

```
lecture.mp4
     │
     ▼
Frame Extraction (OpenCV) ── preserves timestamp per frame
     │
     ▼
Diagram Detection (YOLO / DETR / custom detector)
     │
     ▼
Event Grouping ── merges consecutive same-diagram frames into ONE event
     │
     ├───────────────┬───────────────┐
     ▼                ▼               │
    OCR             VLM               │
 (PaddleOCR /   (Qwen2-VL / LLaVA     │
  Tesseract)      via Groq API)       │
     │                │               │
     └───────┬────────┘               │
             ▼                        │
        LLM Explanation ◄─────────────┘
      (educational, structured,
       subject-aware — via Groq API)
             │
             ▼
            TTS
      (Coqui TTS / IndicTTS,
       English + Hindi)
             │
             ▼
     Timestamp + Audio File
             │
             ▼
      Lecture Metadata JSON
```

**Why OCR *and* VLM, not just one:** OCR reliably extracts literal text (axis labels, titles) but has no understanding of what the diagram *means*. The VLM provides that contextual/visual understanding (e.g., "this is a velocity-time graph, the line trends upward, meaning velocity increases over time"). Passing OCR text into the VLM step as extra context improves grounding — the VLM doesn't have to guess at label text it can read directly from OCR.

**Why LLM as a separate step after VLM:** the VLM output is a structured/technical description of the diagram; the LLM step is responsible for turning that into a natural, pedagogically appropriate spoken explanation, in the correct language, matched to the subject/course context. Keeping this separate from the VLM step means explanation style and language can be iterated on without re-running detection or vision inference.

**Event grouping is a distinct pipeline step**, not a detail of detection: without it, a diagram visible for 15 seconds at 1 fps would produce ~15 duplicate detections and 15 redundant, wasteful VLM/LLM/TTS calls. Grouping consecutive same-diagram detections into a single `(start, end)` event is what makes the rest of the pipeline efficient and coherent.

## 3. Web Application Architecture

```
┌─────────────────────┐        ┌─────────────────────┐
│   React Frontend     │  HTTP  │   FastAPI Backend    │
│                       │◄──────►│                       │
│  - Landing page       │        │  - /lectures          │
│  - Lecture catalog    │        │  - /lectures/{id}      │
│  - Video player       │        │  - /lectures/upload   │
│  - Accessibility UI   │        │  - /lectures/{id}/status│
└─────────────────────┘        │  - /lectures/{id}/metadata│
                                 └───────────┬───────────┘
                                             │
                                   ┌─────────┴─────────┐
                                   ▼                   ▼
                            Lecture Storage      AI Pipeline
                            (video files,        (triggered on
                             audio files,          upload, runs
                             metadata JSON)        as background job)
```

### Backend API surface

| Method | Route | Purpose |
|---|---|---|
| GET | `/lectures` | List all processed lectures (catalog) |
| GET | `/lectures/{id}` | Get details for one lecture |
| POST | `/lectures/upload` | Upload a new lecture video, triggers pipeline |
| GET | `/lectures/{id}/status` | Poll processing status (queued/processing/done/failed) |
| GET | `/lectures/{id}/metadata` | Get the events JSON (timestamp → audio) for playback |

### Player synchronization logic (client-side)

```
on video timeupdate:
    if AD is OFF: do nothing special
    if currentTime crosses an event.timestamp AND event not yet played:
        video.pause()
        play(event.audio[selectedLanguage])
        on audio ended:
            video.play()
            mark event as played
```

This logic must guarantee mutual exclusion between lecture audio and AD audio — the video element is always paused while AD is playing, so there is no code path where both are audible at once.

## 4. Data Contracts Between Modules

These three contracts are the seams between team members' work and should be finalized early, before deep implementation, so modules can be built in parallel.

**1. Frames → Detection**
```json
{ "frame_path": "frames/frame_150.jpg", "timestamp": 150.2 }
```

**2. Detection/OCR/VLM → Explanation/TTS**
```json
{
  "timestamp": 150.2,
  "image": "diagram_01.jpg",
  "ocr_text": "Velocity-Time Graph...",
  "vlm_analysis": "..."
}
```

**3. Explanation/TTS → Backend/Player (final per-lecture metadata)**
```json
{
  "lecture_id": "physics_01",
  "events": [
    {
      "timestamp": 150.2,
      "audio_en": "/audio/ad_001_en.mp3",
      "audio_hi": "/audio/ad_001_hi.mp3"
    }
  ]
}
```

## 5. AI Provider: Groq

All VLM and LLM inference in the pipeline calls **Groq's free API**. Architectural implications:

- **Isolate the client.** All Groq calls go through a single thin wrapper module (e.g. `services/groq_client.py`) so the model/provider can be swapped later without touching detection, OCR, or TTS code.
- **Rate limiting & retries.** The free tier has request-rate and token limits; the offline pipeline should process diagram events with backoff/retry rather than assuming unlimited concurrent calls. Batch lecture processing (multiple diagrams per video) should queue calls rather than fire them all in parallel.
- **Caching.** Cache VLM/LLM responses per diagram-event during development so re-running the pipeline while iterating on downstream steps (TTS, metadata format) doesn't re-spend API quota.
- **Model choice is a config value**, not hardcoded — store the Groq model name in an environment variable/config file so it can be changed as available models evolve.

## 6. Deployment Shape

```
Frontend (React) ──build──► static hosting
Backend (FastAPI) ──────────► app server (handles API + triggers pipeline jobs)
AI Pipeline ─────────────────► runs as background job/worker process, writes to shared storage
Lecture Storage ──────────────► shared filesystem or object storage: videos, audio, metadata JSON
```

The pipeline does not need to run inside the request/response cycle of the web app — it's triggered on upload and the frontend polls `/status` until processing completes, then fetches `/metadata`.
