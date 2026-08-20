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
├── app.py                      # FastAPI Web Application & API Server
├── diagram_to_speech.py        # Core 3-Step AI Pipeline & CLI Wrapper
├── generate_samples.py         # Utility script to generate sample diagrams
├── requirements.txt            # Python dependencies
├── .env                        # Environment variable configuration (GROQ_API_KEY)
├── sample_diagrams/            # Organized sample diagram images
│   ├── sample_diagram_1.png
│   ├── sample_diagram_2.png
│   └── sample_diagram_3.png
├── static/                     # Web UI frontend assets
│   └── index.html
└── storage/                    # Uploaded diagrams and generated audio files
    ├── audio/
    └── uploads/
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
Add your Groq API key to `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## How to Run

### Option A: Interactive Web UI (Recommended)

Start the web application server:
```bash
python app.py
```
Open your browser and navigate to:
[http://localhost:8000](http://localhost:8000)

**Usage in Web UI:**
1. Drag and drop any diagram image into the upload box (or click to browse).
2. Or click one of the pre-loaded sample diagrams ("Line Graph", "Flowchart", "Bar Chart").
3. Watch the real-time progress steps: **Understanding -> Educational Explanation -> Speech Synthesis**.
4. Listen to the spoken audio narrative directly in the browser or download the `.mp3` file.

---

### Option B: Command Line Interface (CLI)

Run the script on any diagram image:

```bash
# Process a sample diagram
python diagram_to_speech.py sample_diagrams/sample_diagram_1.png

# Process with custom audio output path
python diagram_to_speech.py sample_diagrams/sample_diagram_2.png --output my_explanation.mp3
```

**CLI Output Example:**
```
[Step 1/3] Analyzing diagram: sample_diagrams/sample_diagram_1.png...
 -> Successfully analyzed diagram using Vision API.

[Step 2/3] Generating educational spoken explanation...
 -> Educational explanation generated successfully.

[Step 3/3] Synthesizing audio to 'output_audio.mp3'...
 -> Audio file successfully saved using gTTS.

============================================================
GENERATED EDUCATIONAL EXPLANATION:
============================================================
This line graph, titled "Global Temperature Anomaly (1980 - 2020)," tracks average global temperature changes over a 40-year period...
============================================================

AUDIO FILE SAVED AT: /path/to/output_audio.mp3
============================================================
```

---

## Regenerating Sample Diagrams
To regenerate sample images in `sample_diagrams/`:
```bash
python generate_samples.py
```