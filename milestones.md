# EduVision — Milestones

Organized by team member, with a shared integration phase at the end. All four members can start in parallel — Member 1's UI does not depend on AI being ready, and Members 3/4 can develop against a handful of sample diagram images before the full pipeline exists.

---

## 👤 Member 1 — Frontend + Accessibility

**Owns:** Everything the student/faculty interacts with.

- **M1.1 — UI/UX design:** landing page (hero, problem statement, how-it-works, footer), accessibility-first visual design.
- **M1.2 — Lecture catalog:** browsable list of lectures (Physics / Biology / Chemistry), each with title, subject, description, "Play Lecture" action.
- **M1.3 — Video player UI:** play/pause, volume, progress bar, fullscreen, language selector, Audio Description toggle. At this stage the video is a plain MP4 with no AI behavior wired in.
- **M1.4 — Accessibility pass:** full keyboard navigation (Tab/Enter/Space/Arrows), ARIA labels, screen-reader-friendly controls, large hit targets, visible focus states, high-contrast support.
- **M1.5 — Frontend ↔ backend integration:** replace hardcoded lecture data with real calls to Member 2's `/lectures` endpoints.
- **M1.6 — Intelligent player:** wire in the pause → play AD → resume logic against real event metadata (Contract 3, from Member 4/2).
- **M1.7 — UI polish:** responsive/mobile layout, loading states, error states, empty states.

**Deliverable:** complete accessible EduVision web app with working intelligent video player.

---

## 👤 Member 2 — Backend + Video Processing Foundation

**Owns:** The infrastructure everything else plugs into.

- **M2.1 — FastAPI setup:** project skeleton (`main.py`, `routes/`, `services/`, `models/`, `utils/`).
- **M2.2 — Lecture APIs:** `GET /lectures`, `GET /lectures/{id}`, `POST /lectures/upload`, `GET /lectures/{id}/status`, `GET /lectures/{id}/metadata`.
- **M2.3 — Video upload & storage:** accept lecture uploads, validate files, store video + derived assets, track lecture metadata.
- **M2.4 — Video processing utilities:** OpenCV-based frame extraction, FFmpeg/MoviePy for any needed video ops.
- **M2.5 — Frame extraction + timestamp management:** produce `frames/` with each frame tagged to its source timestamp (Contract 1, feeds Member 3).
- **M2.6 — Event/metadata system:** define and implement the shared metadata schema that ties Member 3/4's output to Member 1's player (Contract 3). This is the most important cross-team artifact — lock it early.
- **M2.7 — Pipeline orchestration:** trigger the AI pipeline as a background job on upload; expose progress via `/status`.

**Deliverable:** FastAPI backend + video handling + frame/timestamp pipeline + lecture metadata API.

---

## 👤 Member 3 — Computer Vision (Detection, OCR, VLM)

**Owns:** Finding diagrams and understanding their visual content.

- **M3.1 — Diagram detection:** given extracted frames, detect diagram/graph/chart/slide presence and its timestamp (YOLO / DETR / custom detector).
- **M3.2 — Event grouping:** merge consecutive frame-level detections of the same diagram into a single `(start, end)` diagram event — critical to avoid duplicate downstream processing.
- **M3.3 — OCR:** extract text from each grouped diagram event (PaddleOCR or Tesseract).
- **M3.4 — VLM integration:** feed diagram image + OCR text into a VLM (via Groq API — e.g. a Groq-hosted vision-capable model) to produce a structured understanding: diagram type, elements, axes/labels, relationships.
- **M3.5 — Category testing:** validate detection + understanding across the diagram types the demo needs — graphs, flowcharts, biological diagrams, circuit diagrams, equations, tables.
- **M3.6 — Output formatting:** emit Contract 2 (`timestamp`, `image`, `ocr_text`, `vlm_analysis`) for Member 4 to consume.

**Deliverable:** reliable diagram detection + grouping + OCR + VLM-based visual understanding.

---

## 👤 Member 4 — GenAI Explanation + TTS

**Owns:** Turning visual understanding into something a student can listen to.

- **M4.1 — Educational prompt design:** design LLM prompts (via Groq API) that turn VLM + OCR output into structured, subject-aware educational explanations — not generic captions.
- **M4.2 — LLM explanation generation:** implement the generation step; validate against a rubric of accuracy, completeness, simplicity, and educational usefulness.
- **M4.3 — Hindi/English generation:** produce explanations in both languages (either via bilingual prompting or a translation step).
- **M4.4 — TTS:** synthesize each explanation to audio in English and Hindi (Coqui TTS / IndicTTS), producing files like `ad_001_en.mp3` / `ad_001_hi.mp3`.
- **M4.5 — Audio metadata assembly:** emit the final per-event metadata (`timestamp`, `audio_en`, `audio_hi`) that Member 2's API serves and Member 1's player consumes (Contract 3).
- **M4.6 — Pipeline integration:** connect Member 3's output → LLM → TTS → metadata, end to end for a single lecture.

**Deliverable:** educational explanation generation + bilingual support + TTS + final audio-description metadata.

---

## 🔗 Shared Contracts (finalize before deep implementation)

**Contract 1 — Member 2 → Member 3**
```json
{ "frame_path": "frames/frame_150.jpg", "timestamp": 150.2 }
```

**Contract 2 — Member 3 → Member 4**
```json
{
  "timestamp": 150.2,
  "image": "diagram_01.jpg",
  "ocr_text": "Velocity-Time Graph...",
  "vlm_analysis": "..."
}
```

**Contract 3 — Member 4 → Member 1/2**
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

---

## 🤝 Joint Team Milestones (all 4 members)

- **J1 — Full pipeline dry run:** run one real lecture through the entire chain — detection → OCR/VLM → LLM → TTS → metadata — and confirm every contract holds end to end.
- **J2 — Player integration test:** confirm pause → AD → resume works against real (not mock) metadata, in both languages, with AD toggled on/off.
- **J3 — Accessibility testing:** keyboard-only and screen-reader-only pass through the entire user flow; confirm lecture audio and AD audio never overlap.
- **J4 — AI accuracy testing:** evaluate detection (precision/recall/F1), OCR correctness, VLM understanding, LLM explanation quality, and TTS clarity/pronunciation (EN + HI) individually.
- **J5 — Demo dataset prep:** process 3–5 full lectures (Physics: Motion in 1D; Biology: Plant Cell Structure; Chemistry: Molecular Bonds), each with clear diagrams.
- **J6 — Deployment:** deploy frontend, backend, and confirm the AI-processed lecture storage is correctly served end to end.
- **J7 — Final demo run-through:** faculty opens EduVision → selects a lecture → plays it → diagram triggers pause/AD/resume → confirms the full experience works without manual intervention.

## Suggested Build Order

Frontend UI can start day one, in parallel with backend scaffolding. Detection/OCR/VLM and LLM/TTS should be prototyped against a handful of sample diagram images before the full frame-extraction pipeline is ready, so Members 3 and 4 aren't blocked on Member 2. Lock the three data contracts early — they're what let all four people build in parallel without integration surprises at the end.
