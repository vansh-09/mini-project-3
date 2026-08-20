# EduVision — Product Requirements Document

## 1. Problem Statement

Blind and visually impaired (BLV) students cannot access the visual content of pre-recorded lectures — diagrams, graphs, charts, flowcharts, molecular structures, circuit diagrams, and slides. A professor's spoken narration ("as you can see here...") assumes sight and rarely describes the diagram in enough detail to be understood by someone who cannot see it. This creates a persistent learning gap in STEM education specifically, where visual content carries much of the instructional weight.

## 2. Product Vision

EduVision is an AI-powered accessible learning platform that automatically detects diagrams in pre-recorded lecture videos, understands their content, and generates spoken educational explanations — delivered by pausing the lecture at the moment the diagram appears, playing the audio description (AD), and resuming playback once the explanation ends.

The core insight driving the product: audio descriptions should never compete with the professor's live narration for the student's attention. Rather than trying to interleave AD into silent gaps (fragile, hard to guarantee, and often too short for a full explanation), EduVision pauses the video entirely, delivers a complete explanation, then resumes.

## 3. Target Users

- **Primary:** Blind and visually impaired students taking STEM courses (physics, biology, chemistry) that rely on pre-recorded lecture videos.
- **Secondary:** Faculty/institutions who upload lecture content and want it to be accessible without re-recording or manually writing descriptions.

## 4. Goals

- Automatically detect when a diagram, graph, chart, or other visual aid appears in a lecture video.
- Generate an accurate, structured, *educational* explanation of that diagram — not a generic caption like "there is a graph."
- Deliver the explanation as synchronized audio without ever overlapping the professor's own speech.
- Support both English and Hindi.
- Work on pre-recorded lecture videos with no live/real-time constraint.

## 5. Non-Goals (for this version)

- Real-time/live lecture support (only pre-recorded video is in scope).
- Full transcript generation or captioning of spoken lecture content (only diagram description).
- Support for languages beyond English and Hindi.
- Editing/re-encoding the source lecture video permanently (see Architecture — pause/resume is handled by the web player, not by re-cutting the MP4).

## 6. Core User Flow

1. Faculty/admin uploads a pre-recorded lecture video (e.g. `physics_lecture_01.mp4`).
2. The system processes the video offline: extracts frames, detects diagrams, groups diagram events, runs OCR + VLM understanding, generates an educational explanation via LLM, and synthesizes it to speech (EN + HI).
3. The system produces a metadata file mapping each diagram event to a timestamp and an audio file.
4. A student opens EduVision, browses the lecture catalog, and selects a lecture.
5. The student plays the lecture. Audio Description is ON by default and can be toggled; language can be switched between English and Hindi.
6. When playback reaches a diagram timestamp, the video **automatically pauses**, the audio description **plays**, and once it finishes, the video **automatically resumes** — never overlapping the professor's audio.
7. The student can navigate the whole experience via keyboard and screen reader.

## 7. Functional Requirements

### 7.1 Frontend / Accessibility
- Landing page explaining the product.
- Lecture catalog (browsable list of processed lectures by subject).
- Video player page with standard controls (play/pause, volume, progress, fullscreen).
- Audio Description toggle (ON/OFF).
- Language selector (English / Hindi).
- Full keyboard navigation (Tab, Enter, Space, Arrow keys).
- Screen-reader-friendly labels (ARIA) on all interactive elements.
- Responsive layout (desktop + mobile), with loading/error/empty states.

### 7.2 Backend
- Lecture upload endpoint and storage.
- Lecture listing and metadata retrieval endpoints.
- Processing status endpoint (so the frontend can show "processing" state after upload).
- Orchestration of the AI pipeline as an offline/background job.

### 7.3 AI Pipeline
- **Frame extraction:** sample frames from the video at a fixed interval, preserving timestamps.
- **Diagram detection:** classify/detect frames containing diagrams, graphs, charts, or slides.
- **Event grouping:** merge consecutive detections of the same diagram into a single event (start–end range), not one event per frame.
- **OCR:** extract any text present in the diagram (axis labels, titles, legends).
- **VLM understanding:** given the diagram image + OCR text, produce a structured understanding of diagram type, elements, and relationships.
- **LLM explanation generation:** convert the VLM + OCR output into a natural-language, student-friendly educational explanation (not a generic caption).
- **TTS:** synthesize the explanation into audio, in English and Hindi.
- **Metadata assembly:** produce a single JSON file per lecture mapping `timestamp → audio file(s)`.

### 7.4 Playback / Synchronization
- Web player watches the video's current time against the event metadata.
- On reaching an event timestamp: pause video → play the matching AD audio (respecting the selected language and AD on/off setting) → on audio end, resume video.
- Must never play AD and lecture audio simultaneously.

## 8. Data Contracts (cross-team interfaces)

**Frame → Detection input**
```json
{ "frame_path": "frames/frame_150.jpg", "timestamp": 150.2 }
```

**Detection/OCR/VLM → Explanation input**
```json
{
  "timestamp": 150.2,
  "image": "diagram_01.jpg",
  "ocr_text": "Velocity-Time Graph...",
  "vlm_analysis": "..."
}
```

**Explanation/TTS → Player input (final lecture metadata)**
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

## 9. AI Provider

All LLM/VLM inference calls use **Groq's free API tier**. This has two practical implications the team should design around:
- Rate limits on the free tier — batch/offline processing should include retry/backoff and should not assume unlimited throughput.
- Model availability on Groq should be confirmed at implementation time (available hosted models change); the pipeline should isolate the Groq client behind a thin interface so the underlying model can be swapped without touching the rest of the pipeline.

## 10. Success Metrics

- **Detection quality:** precision/recall/F1 of diagram detection against a hand-labeled sample of lecture frames.
- **Explanation quality:** rated by team/faculty for correctness, educational value, and completeness (rubric-based, not automated).
- **Sync correctness:** zero instances of AD audio overlapping lecture audio across full end-to-end test runs.
- **Accessibility:** all core flows completable via keyboard-only and screen-reader-only navigation.
- **Demo readiness:** 3–5 fully processed lectures (Physics, Biology, Chemistry) playable end-to-end without manual intervention.

## 11. Risks / Open Questions

- Diagram detection accuracy on varied lecture styles (slides vs. whiteboard vs. document camera) is unproven — needs early testing on real sample footage.
- Groq free-tier rate limits may slow batch processing of longer lectures; needs a queuing/retry strategy.
- OCR quality on handwritten or low-resolution diagrams may be poor — VLM should not be assumed to compensate fully.
- Pause/resume UX needs real testing with screen-reader users, not just sighted validation.
