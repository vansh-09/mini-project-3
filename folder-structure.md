# EduVision — Recommended Folder Structure

```
eduvision/
├── PRD.md
├── architecture.md
├── milestones.md
├── README.md
│
├── frontend/                          # Member 1
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
│   │   │   └── useSyncedPlayback.js    # pause -> AD -> resume logic
│   │   ├── api/
│   │   │   └── lectures.js             # calls to FastAPI
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                           # Member 2
│   ├── main.py
│   ├── routes/
│   │   ├── lectures.py                # /lectures, /lectures/{id}, /upload
│   │   └── status.py                  # /lectures/{id}/status
│   ├── services/
│   │   ├── storage_service.py         # file upload/storage handling
│   │   ├── frame_extractor.py         # OpenCV frame extraction + timestamps
│   │   ├── pipeline_orchestrator.py   # triggers AI pipeline as background job
│   │   └── groq_client.py             # thin wrapper around Groq API calls
│   ├── models/
│   │   └── schemas.py                 # Pydantic models for the 3 data contracts
│   ├── utils/
│   │   └── ffmpeg_helpers.py
│   ├── requirements.txt
│   └── config.py                      # env vars, Groq model name, paths
│
├── ai_pipeline/                       # Members 3 + 4
│   ├── detection/                     # Member 3
│   │   ├── detector.py                # YOLO/DETR/custom diagram detector
│   │   ├── event_grouping.py          # merge consecutive frame detections
│   │   └── models/                    # trained/downloaded detector weights
│   ├── ocr/                           # Member 3
│   │   └── ocr_service.py             # PaddleOCR / Tesseract wrapper
│   ├── vlm/                           # Member 3
│   │   └── vlm_service.py             # Groq-hosted VLM calls
│   ├── explanation/                   # Member 4
│   │   ├── prompts.py                 # educational explanation prompt templates
│   │   └── llm_service.py             # Groq LLM calls (EN + HI)
│   ├── tts/                           # Member 4
│   │   └── tts_service.py             # Coqui TTS / IndicTTS wrapper
│   ├── process_lecture.py             # single entrypoint: python process_lecture.py lecture.mp4
│   └── requirements.txt
│
├── storage/                           # shared runtime data (gitignored)
│   ├── videos/
│   │   └── physics_lecture_01.mp4
│   ├── frames/
│   │   └── physics_lecture_01/
│   │       └── frame_150.jpg
│   ├── audio/
│   │   └── physics_lecture_01/
│   │       ├── ad_001_en.mp3
│   │       └── ad_001_hi.mp3
│   └── metadata/
│       └── physics_lecture_01.json    # final Contract 3 output
│
├── demo_lectures/                     # source content for the 3-5 demo lectures
│   ├── physics_motion_1d.mp4
│   ├── biology_plant_cell.mp4
│   └── chemistry_molecular_bonds.mp4
│
├── tests/
│   ├── frontend/
│   ├── backend/
│   └── ai_pipeline/
│       ├── test_detection.py
│       ├── test_ocr.py
│       ├── test_vlm.py
│       ├── test_explanation.py
│       └── test_tts.py
│
├── docs/
│   ├── data_contracts.md              # the 3 JSON contracts, kept in sync
│   └── accessibility_checklist.md
│
└── .env.example                       # GROQ_API_KEY, model names, storage paths
```

## Notes on the layout

- **`ai_pipeline/` is split into subfolders by team member** (`detection/`, `ocr/`, `vlm/` for Member 3; `explanation/`, `tts/` for Member 4) so both can work in the same top-level directory without stepping on each other's files.
- **`storage/` is gitignored** — it holds generated runtime artifacts (frames, audio, metadata), not source code. Only `demo_lectures/` (the raw source videos for the 3–5 demo lectures) should be committed or tracked via Git LFS if the videos are large.
- **`process_lecture.py`** is the single command-line entrypoint that runs the entire offline pipeline (`python process_lecture.py physics_lecture_01.mp4`) — useful for Members 3/4 to test their modules together without needing the backend running.
- **`docs/data_contracts.md`** should mirror the three JSON contracts in `architecture.md` — keep one as the source of truth and reference it from schemas in `backend/models/schemas.py` so frontend, backend, and pipeline never drift out of sync.
- **`backend/services/groq_client.py`** is the single choke point for all Groq API calls (used by both `vlm_service.py` and `llm_service.py` in `ai_pipeline/`) — keeping the API key, model name, and retry/backoff logic in one place makes it trivial to swap models or providers later.
