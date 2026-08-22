# EduVision — Diagram to Speech Pipeline & Web UI

EduVision converts diagram images (charts, graphs, flowcharts, schematics) into clear, spoken educational audio narratives.

---

## Features
- **Diagram Understanding** — Groq Vision API analyzes structure, axes, titles, legends, and data trends. Falls back to OCR + Groq text model if vision is unavailable.
- **Educational Explanation** — Groq text LLM synthesizes a 3–5 sentence spoken-style explanation tuned for student audio learning.
- **Text-to-Speech** — gTTS converts the explanation to an MP3 audio file. Falls back to `pyttsx3` offline engine if gTTS is unavailable.
- **Web UI** — React + Vite frontend with drag-and-drop upload, real-time 3-step progress, sample diagram picker, and integrated audio player.

---

## Tech Stack

### 🔍 Vision Language Model (VLM) — Diagram Understanding
| Model | Provider | Role |
|-------|----------|------|
| `qwen/qwen3.6-27b` | Groq | Primary VLM (vision + text) |
| `llama-3.2-90b-vision-preview` | Groq / Meta | VLM fallback #1 |
| `llama-3.2-11b-vision-preview` | Groq / Meta | VLM fallback #2 |

Diagrams are base64-encoded and sent directly to the Groq Vision API. Models are tried in order; the first successful response is used.

### 🧠 Text Agent — Educational Explanation Generation
| Model | Provider | Role |
|-------|----------|------|
| `groq/compound` | Groq | Primary text agent |
| `openai/gpt-oss-120b` | OpenAI via Groq | Text fallback #1 |
| `qwen/qwen3.6-27b` | Groq | Text fallback #2 |
| `llama-3.3-70b-versatile` | Groq / Meta | Text fallback #3 |

The text agent receives the VLM's structural analysis and generates a 3–5 sentence spoken-style explanation optimized for TTS audio.

### 📝 OCR — Vision Fallback
| Library | Role |
|---------|------|
| `pytesseract` | Extracts raw text from diagram images when all VLMs fail |
| `Pillow` | Image loading for OCR |
| System `tesseract` | OCR engine (must be installed separately via `brew install tesseract`) |

When VLM calls fail (rate limits, unsupported format, etc.), OCR-extracted text is fed to the text agent instead.

### 🔊 Text-to-Speech (TTS)
| Library | Type | Role |
|---------|------|------|
| `gTTS` (Google TTS) | Online | Primary TTS — natural-sounding MP3 output |
| `pyttsx3` | Offline | Fallback TTS — used when gTTS / network is unavailable |

### 🖥️ Backend
| Technology | Role |
|------------|------|
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **Groq Python SDK** (`groq>=0.9.0`) | API client for all LLM + VLM calls |
| **OpenCV** (`opencv-python`) | Frame extraction from lecture videos |
| **python-dotenv** | `.env` config loading |
| **python-multipart** | File upload parsing |

### 🎨 Frontend
| Technology | Role |
|------------|------|
| **React + Vite** | Component framework and dev server |
| **Vanilla CSS** | Styling (no CSS framework) |
| **Google Fonts (Inter)** | Typography |



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

The project runs as two separate processes: a **FastAPI backend** and a **React/Vite frontend**.

> ⚠️ **Always run backend commands from the project root** (`Mini-Project-3/`), not from inside the `backend/` subfolder — the `backend.main` module path won't resolve otherwise.

---

### Terminal 1 — Backend (FastAPI)

```bash
# From the project root:
cd Mini-Project-3

python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | REST API |
| http://localhost:8000/docs | Interactive Swagger docs |

---

### Terminal 2 — Frontend (React/Vite)

```bash
# From the frontend directory:
cd Mini-Project-3/frontend

npm install       # only needed the first time
npm run dev
```

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | Web UI |

The Vite dev server is pre-configured to proxy `/api` requests to the backend on port 8000.

---

### Option B: Command Line Interface (CLI)

Run the diagram-to-speech pipeline directly without the UI:

```bash
# From the project root:
python3 -m backend.services.diagram_to_speech sample_diagrams/sample_diagram_1.png

# With a custom audio output path:
python3 -m backend.services.diagram_to_speech sample_diagrams/sample_diagram_2.png --output my_explanation.mp3
```

---

## Dev Utilities

### Regenerating Sample Diagrams
```bash
python3 scripts/generate_samples.py
```

### Seeding Demo Lecture Data
```bash
python3 scripts/seed_data.py
```