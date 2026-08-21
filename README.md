# EduVision — Diagram to Speech Pipeline & Web UI

EduVision converts diagram images (charts, graphs, flowcharts, schematics) into clear, spoken educational audio narratives.

---

## Features
- **Diagram Understanding (Groq Vision API)**: Analyzes structure, axes, titles, legends, and data trends using Groq vision models (`qwen/qwen3.6-27b`). Automatically falls back to OCR (`pytesseract`) + Groq text model if vision is unavailable or rate-limited.
- **Educational Explanation (Groq Text LLM)**: Synthesizes a 3-5 sentence spoken-style explanation ideal for student learning.
- **Text-to-Speech (gTTS)**: Synthesizes narration into an MP3 audio file (with offline `pyttsx3` fallback).
- **Interactive Web UI**: Modern dark-mode web application featuring drag-and-drop file upload, diagram preview, real-time 3-step progress indicators, sample diagram picker, and an integrated audio player.

---

## Folder Structure

```
Mini-Project-3/
├── backend/                     # FastAPI backend
│   ├── main.py                  # App entrypoint — run this to start the server
│   ├── config.py                # Env vars, paths, model names
│   ├── routes/                  # API route handlers
│   ├── services/                # Business logic services
│   │   └── diagram_to_speech.py # Core 3-step AI pipeline
│   ├── models/                  # Pydantic schemas
│   └── utils/                   # Shared helpers
├── frontend/                    # React/Vite web UI
├── ai_pipeline/                 # CV + GenAI pipeline modules
├── scripts/                     # Dev & seeding utilities
│   ├── generate_samples.py      # Generate sample diagram PNGs
│   └── seed_data.py             # Seed demo lecture metadata
├── tests/                       # Test suites
├── docs/                        # Project documentation
├── static/                      # Served static frontend assets
├── storage/                     # Runtime data (gitignored)
├── sample_diagrams/             # Sample diagram images
├── demo_lectures/               # Source lecture videos
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (GROQ_API_KEY)
└── .env.example                 # Environment variable template
```

---

## Setup & Installation

### 1. Prerequisites
Ensure Python 3.9+ and system Tesseract OCR are installed:
```bash
# On macOS via Homebrew (optional, for OCR fallback):
brew install tesseract
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. API Key Configuration
Copy the template and fill in your key:
```bash
cp .env.example .env
# Edit .env and set GROQ_API_KEY=your_groq_api_key_here
```

---

## How to Run

### Option A: Interactive Web UI (Recommended)

Start the backend server from the project root:
```bash
./venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

**Usage in Web UI:**
1. Drag and drop any diagram image into the upload box (or click to browse).
2. Or click one of the pre-loaded sample diagrams ("Line Graph", "Flowchart", "Bar Chart").
3. Watch the real-time progress steps: **Understanding → Educational Explanation → Speech Synthesis**.
4. Listen to the spoken audio narrative directly in the browser or download the `.mp3` file.

---

### Option B: Command Line Interface (CLI)

Run the diagram-to-speech service directly:

```bash
./venv/bin/python -m backend.services.diagram_to_speech sample_diagrams/sample_diagram_1.png

# Process with custom audio output path
./venv/bin/python -m backend.services.diagram_to_speech sample_diagrams/sample_diagram_2.png --output my_explanation.mp3
```

---

## Dev Utilities

### Regenerating Sample Diagrams
```bash
./venv/bin/python scripts/generate_samples.py
```

### Seeding Demo Lecture Data
```bash
./venv/bin/python scripts/seed_data.py
```