import os
import sys
import json
import time
from pathlib import Path

# Ensure project root is on sys.path so backend/ai_pipeline packages resolve
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.config import METADATA_DIR, AUDIO_DIR, UPLOAD_DIR, FRAMES_DIR
from ai_pipeline.tts.tts_service import TTSService
from ai_pipeline.detection.annotator import DiagramAnnotator

def seed_demo_lectures():
    print("Seeding 5 full STEM demo lectures data (Milestone J5)...")
    tts = TTSService()
    annotator = DiagramAnnotator()

    demo_data = [
        {
            "lecture_id": "physics_01",
            "title": "Physics — Motion in One Dimension & Velocity-Time Graphs",
            "subject": "Physics",
            "description": "Understanding kinematic equations, constant velocity vs uniform acceleration curves, and slope meanings.",
            "events": [
                {
                    "event_id": "physics_01_evt_001",
                    "timestamp": 5.0,
                    "start_time": 5.0,
                    "end_time": 15.0,
                    "diagram_type": "chart/graph",
                    "ocr_text": "Velocity vs Time Graph. Y-axis: Velocity (m/s), X-axis: Time (s). Linear upward slope from (0,0) to (10,50).",
                    "vlm_analysis": "A line graph titled 'Velocity vs Time'. The vertical axis represents velocity in meters per second, and the horizontal axis represents time in seconds. A straight blue line ascends steadily from the origin.",
                    "explanation_en": "This velocity-time graph shows uniform acceleration. The blue line ascends steadily from zero to 50 meters per second over a 10-second interval, indicating a constant rate of acceleration of 5 meters per second squared.",
                    "explanation_hi": "यह वेग-समय ग्राफ एकसमान त्वरण को दर्शाता है। नीली रेखा 10 सेकंड के अंतराल में शून्य से 50 मीटर प्रति सेकंड तक लगातार ऊपर उठती है, जो 5 मीटर प्रति सेकंड वर्ग की स्थिर त्वरण दर का संकेत देती है।"
                }
            ]
        },
        {
            "lecture_id": "biology_01",
            "title": "Biology — Plant Cell Anatomy & Organelle Functions",
            "subject": "Biology",
            "description": "Detailed diagram breakdown of the rigid cell wall, central vacuole, chloroplasts, and cytoplasm in plant cells.",
            "events": [
                {
                    "event_id": "biology_01_evt_001",
                    "timestamp": 8.0,
                    "start_time": 8.0,
                    "end_time": 20.0,
                    "diagram_type": "biological/anatomical",
                    "ocr_text": "Plant Cell Structure. Cell Wall, Cell Membrane, Chloroplast, Large Central Vacuole, Nucleus.",
                    "vlm_analysis": "A detailed cross-section diagram of a eukaryotic plant cell displaying a prominent green cell wall, large central vacuole, oval nucleus with nucleolus, green oval chloroplasts, and mitochondria.",
                    "explanation_en": "This plant cell diagram highlights key structural organelles. The thick green outer boundary represents the rigid cell wall, which provides structural support. Inside, the large central vacuole maintains turgor pressure, while oval green chloroplasts house chlorophyll for photosynthesis.",
                    "explanation_hi": "यह पादप कोशिका आरेख प्रमुख संरचनात्मक अंगों को उजागर करता है। मोटी हरी बाहरी सीमा कठोर कोशिका भित्ति का प्रतिनिधित्व करती है। अंदर, बड़ी केंद्रीय रसधानी कोशिका के आकार को बनाए रखती है, जबकि हरे अंडाकार क्लोरोप्लास्ट प्रकाश संश्लेषण करते हैं।"
                }
            ]
        },
        {
            "lecture_id": "chemistry_01",
            "title": "Chemistry — Covalent vs Ionic Chemical Bonds",
            "subject": "Chemistry",
            "description": "Exploring electron sharing in water (H2O) molecules versus electron transfer in Sodium Chloride (NaCl) lattices.",
            "events": [
                {
                    "event_id": "chemistry_01_evt_001",
                    "timestamp": 12.0,
                    "start_time": 12.0,
                    "end_time": 25.0,
                    "diagram_type": "diagram",
                    "ocr_text": "Covalent Bonding in Water (H2O). Oxygen atom sharing electron pairs with two Hydrogen atoms.",
                    "vlm_analysis": "A molecular diagram illustrating covalent electron pair sharing between one central oxygen atom and two surrounding hydrogen atoms to form a stable water molecule.",
                    "explanation_en": "This chemistry diagram demonstrates covalent bonding in a water molecule. The central oxygen atom shares one pair of valence electrons with each of the two hydrogen atoms, completing outer electron shells and forming strong single covalent bonds.",
                    "explanation_hi": "यह रसायन विज्ञान आरेख एक जल अणु में सहसंयोजक बंधन को दर्शाता है। केंद्रीय ऑक्सीजन परमाणु दो हाइड्रोजन परमाणुओं में से प्रत्येक के साथ वैलेंस इलेक्ट्रॉनों की एक जोड़ी साझा करता है, जिससे मजबूत सहसंयोजक बंधन बनते हैं।"
                }
            ]
        },
        {
            "lecture_id": "cs_01",
            "title": "Computer Science — Binary Search Algorithm Flowchart",
            "subject": "Computer Science",
            "description": "Step-by-step logic flow: checking mid-elements, splitting arrays into halves, and logarithmic O(log n) time complexity.",
            "events": [
                {
                    "event_id": "cs_01_evt_001",
                    "timestamp": 6.0,
                    "start_time": 6.0,
                    "end_time": 18.0,
                    "diagram_type": "flowchart/schematic",
                    "ocr_text": "Binary Search Flowchart. Start -> Calculate Mid -> Is Target == Mid? Yes: Return Mid. No: Target < Mid? Yes: High = Mid - 1. No: Low = Mid + 1.",
                    "vlm_analysis": "A structured computer science flowchart with diamond decision nodes and rectangular action boxes depicting the binary search logarithmic search algorithm.",
                    "explanation_en": "This computer science flowchart illustrates the binary search algorithm logic. Starting with a sorted array, the algorithm compares the target value against the middle element. If unequal, the search space is halved, guaranteeing efficient logarithmic search complexity.",
                    "explanation_hi": "यह कंप्यूटर विज्ञान फ़्लोचार्ट बाइनरी खोज एल्गोरिदम तर्क को दर्शाता है। एक सॉर्ट किए गए सरणी से शुरू करके, एल्गोरिथ्म मध्य तत्व के खिलाफ लक्ष्य मूल्य की तुलना करता है। यदि असमान है, तो खोज स्थान आधा हो जाता है।"
                }
            ]
        },
        {
            "lecture_id": "math_01",
            "title": "Mathematics — Calculus Curves & Area Under Integral",
            "subject": "Mathematics",
            "description": "Visualizing definite integrals as the limit of Riemann sums beneath parabolic functions.",
            "events": [
                {
                    "event_id": "math_01_evt_001",
                    "timestamp": 10.0,
                    "start_time": 10.0,
                    "end_time": 22.0,
                    "diagram_type": "chart/graph",
                    "ocr_text": "Definite Integral Area. Curve f(x) = x^2 from x=a to x=b. Shaded region under curve represents integral.",
                    "vlm_analysis": "A mathematical graph showing a continuous curve f(x) above the horizontal x-axis with vertical dashed lines at bounds a and b, enclosing a shaded area representing the definite integral.",
                    "explanation_en": "This calculus graph depicts the geometric interpretation of a definite integral. The shaded purple area under the function curve between points a and b represents the cumulative net area calculated by integrating the function.",
                    "explanation_hi": "यह कलन (कैलकुलस) ग्राफ एक निश्चित समाकल की ज्यामितीय व्याख्या को प्रस्तुत करता है। बिंदुओं a और b के बीच फ़ंक्शन वक्र के तहत छायांकित क्षेत्र संचयी कुल क्षेत्रफल का प्रतिनिधित्व करता है।"
                }
            ]
        }
    ]

    for item in demo_data:
        lec_id = item["lecture_id"]
        lec_frames_dir = FRAMES_DIR / lec_id
        lec_frames_dir.mkdir(parents=True, exist_ok=True)

        for evt in item["events"]:
            # Generate audio files
            audio_paths = tts.synthesize_bilingual(
                evt["explanation_en"],
                evt["explanation_hi"],
                evt["event_id"]
            )
            evt["audio_en"] = audio_paths["audio_en"]
            evt["audio_hi"] = audio_paths["audio_hi"]

            # Create mock diagram frame & annotated overlay image
            raw_frame_path = lec_frames_dir / f"frame_0001_{int(evt['timestamp'])}s.jpg"
            annotated_frame_path = lec_frames_dir / f"annotated_{evt['event_id']}.jpg"

            if not raw_frame_path.is_file():
                with open(raw_frame_path, "wb") as f:
                    f.write(b"MOCK_FRAME_DATA")

            annotator.annotate_frame(
                str(raw_frame_path),
                [{"x": 40, "y": 40, "w": 400, "h": 250}],
                label=f"{evt['diagram_type'].upper()}",
                output_path=str(annotated_frame_path)
            )

            evt["image_url"] = f"/storage/frames/{lec_id}/{raw_frame_path.name}"
            evt["annotated_image_url"] = f"/storage/frames/{lec_id}/{annotated_frame_path.name}"

        meta = {
            "lecture_id": lec_id,
            "title": item["title"],
            "subject": item["subject"],
            "description": item["description"],
            "video_url": f"/storage/uploads/{lec_id}.mp4",
            "status": "completed",
            "processed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "events_count": len(item["events"]),
            "events": item["events"]
        }

        meta_file = METADATA_DIR / f"{lec_id}.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        print(f" -> Seeded demo STEM lecture: {lec_id} ({item['subject']})")

    print("All 5 STEM demo lectures successfully seeded!")

if __name__ == "__main__":
    seed_demo_lectures()
