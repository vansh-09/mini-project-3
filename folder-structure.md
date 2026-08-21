# EduVision — Folder Structure

```
Mini-Project-3/
├── PRD.md
├── architecture.md
├── milestones.md
├── README.md
├── requirements.txt               # Single root Python requirements file
├── .env                           # GROQ_API_KEY (gitignored)
├── .env.example                   # Template — safe to commit
├── Dockerfile
├── docker-compose.yml
│
├── backend/                       # Member 2
│   ├── main.py                    # FastAPI app entrypoint — run to start server
│   ├── config.py                  # Env vars, Groq model names, storage paths
│   ├── routes/
│   │   ├── lectures.py            # /lectures, /lectures/{id}, /upload
│   │   └── status.py              # /lectures/{id}/status
│   ├── services/
│   │   ├── diagram_to_speech.py   # Core 3-step AI pipeline (Vision→LLM→TTS)
│   │   ├── storage_service.py     # File upload/storage handling
│   │   ├── frame_extractor.py     # OpenCV frame extraction + timestamps
│   │   ├── pipeline_orchestrator.py # Triggers AI pipeline as background job
│   │   └── groq_client.py         # Thin wrapper around Groq API calls
│   ├── models/
│   │   └── schemas.py             # Pydantic models for the 3 data contracts
│   └── utils/
│       └── ffmpeg_helpers.py
│
├── frontend/                      # Member 1
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── player/
│   │   │   │   ├── VideoPlayer.jsx
│   │   │   │   ├── AccessibilityControls.jsx
│   │   │   │   └── LanguageSelector.jsx
│   │   │   ├── catalog/
│   │   │   │   ├── LectureCard.jsx
│   │   │   │   └── LectureCatalog.jsx
│   │   │   └── layout/
│   │   │       ├── Navbar.jsx
│   │   │       └── Footer.jsx
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Catalog.jsx
│   │   │   └── LecturePlayer.jsx
│   │   ├── hooks/
│   │   │   └── useSyncedPlayback.js    # pause → AD → resume logic
│   │   ├── api/
│   │   │   └── lectures.js             # calls to FastAPI
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── ai_pipeline/                   # Members 3 + 4
│   ├── detection/                 # Member 3
│   │   ├── detector.py            # YOLO/DETR/custom diagram detector
│   │   ├── event_grouping.py      # Merge consecutive frame detections
│   │   ├── annotator.py           # Draw bounding-box overlays on frames
│   │   └── models/                # Trained/downloaded detector weights
│   ├── ocr/                       # Member 3
│   │   └── ocr_service.py         # PaddleOCR / Tesseract wrapper
│   ├── vlm/                       # Member 3
│   │   └── vlm_service.py         # Groq-hosted VLM calls
│   ├── explanation/               # Member 4
│   │   ├── prompts.py             # Educational explanation prompt templates
│   │   └── llm_service.py         # Groq LLM calls (EN + HI)
│   ├── tts/                       # Member 4
│   │   └── tts_service.py         # Coqui TTS / IndicTTS wrapper
│   └── process_lecture.py         # Single entrypoint: python process_lecture.py lecture.mp4
│
├── scripts/                       # Dev & seeding utilities
│   ├── generate_samples.py        # Generate sample diagram PNG images
│   └── seed_data.py               # Seed 5 STEM demo lectures (Milestone J5)
│
├── storage/                       # Shared runtime data (gitignored)
│   ├── videos/
│   ├── frames/
│   ├── audio/
│   ├── uploads/
│   └── metadata/
│
├── demo_lectures/                 # Source content for 3-5 demo lectures
│
├── sample_diagrams/               # Sample diagram images for demo/testing
│   ├── sample_diagram_1.png
│   ├── sample_diagram_2.png
│   └── sample_diagram_3.png
│
├── static/                        # Served static frontend assets
│   └── index.html
│
├── tests/
│   ├── test_full_suite.py         # End-to-end milestone test suite
│   ├── backend/
│   │   └── test_api.py
│   └── ai_pipeline/
│       ├── test_detection.py
│       ├── test_explanation.py
│       ├── test_ocr.py
│       ├── test_tts.py
│       └── test_vlm.py
│
└── docs/
    └── MILESTONES_STATUS.md
```

## Notes on the layout

- **`backend/main.py`** is the single FastAPI entrypoint. Start the server with:
  `uvicorn backend.main:app --reload`
- **`backend/services/diagram_to_speech.py`** is the core 3-step AI pipeline (Vision → LLM → TTS). It is imported by `backend/main.py` and can also be run from the CLI as a module:
  `python -m backend.services.diagram_to_speech path/to/diagram.png`
- **`scripts/`** holds dev utilities that are not core runtime code. Run them from the project root.
- **`ai_pipeline/`** is split into subfolders by team member (`detection/`, `ocr/`, `vlm/` for Member 3; `explanation/`, `tts/` for Member 4).
- **`storage/` is gitignored** — it holds generated runtime artifacts (frames, audio, metadata).
- **`backend/services/groq_client.py`** is the single choke point for all Groq API calls — keeping the API key, model name, and retry/backoff logic in one place makes it trivial to swap models or providers later.
- **Root `requirements.txt`** is the single dependency file for the entire Python project (backend + ai_pipeline share the same venv).
