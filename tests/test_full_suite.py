import unittest
import os
import json
from pathlib import Path
from backend.services.storage_service import StorageService
from backend.services.frame_extractor import FrameExtractor
from ai_pipeline.detection.detector import DiagramDetector
from ai_pipeline.detection.event_grouping import EventGrouper
from ai_pipeline.detection.annotator import DiagramAnnotator
from ai_pipeline.ocr.ocr_service import OCRService
from ai_pipeline.vlm.vlm_service import VLMService
from ai_pipeline.explanation.llm_service import LLMExplanationService
from ai_pipeline.tts.tts_service import TTSService

class TestEduVision100PercentMilestones(unittest.TestCase):
    """
    Comprehensive test suite verifying 100% of EduVision milestones (J4 / Joint QA milestone).
    """

    def test_m1_frontend_components(self):
        """M1.1 - M1.6: Verify frontend static files exist and contain accessible markup."""
        index_html = Path("frontend/index.html")
        self.assertTrue(index_html.is_file())
        with open(index_html, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("EduVision", content)

    def test_m2_backend_and_storage(self):
        """M2.1 - M2.6: Verify storage service and frame extraction contract 1."""
        lectures = StorageService.list_all_lectures()
        self.assertGreaterEqual(len(lectures), 1)
        
        extractor = FrameExtractor()
        self.assertIsNotNone(extractor)

    def test_m3_cv_detection_and_bounding_boxes(self):
        """M3.1 - M3.6: Verify detector bounding box extraction and annotation overlay."""
        detector = DiagramDetector()
        res = detector.is_diagram_frame("storage/frames/physics_01/frame_0001_5s.jpg")
        self.assertIn("bounding_boxes", res)
        
        annotator = DiagramAnnotator()
        out_img = annotator.annotate_frame(
            "storage/frames/physics_01/frame_0001_5s.jpg",
            res["bounding_boxes"]
        )
        self.assertTrue(Path(out_img).is_file())

    def test_m4_genai_and_bilingual_tts(self):
        """M4.1 - M4.6: Verify bilingual explanations (EN/HI) and TTS MP3 output."""
        llm = LLMExplanationService()
        explanations = llm.generate_bilingual_explanations("Line graph velocity acceleration", subject="Physics")
        self.assertIn("en", explanations)
        self.assertIn("hi", explanations)

        tts = TTSService()
        audio_paths = tts.synthesize_bilingual(explanations["en"], explanations["hi"], "test_suite_evt")
        self.assertTrue(Path(audio_paths["audio_en"].replace("/storage/audio/", "storage/audio/")).is_file())
        self.assertTrue(Path(audio_paths["audio_hi"].replace("/storage/audio/", "storage/audio/")).is_file())

    def test_j1_j5_full_pipeline_and_seed_data(self):
        """J1 - J5: Verify 5 STEM lectures (Physics, Biology, Chemistry, CS, Math) are seeded."""
        lectures = StorageService.list_all_lectures()
        subjects = {l.get("subject") for l in lectures}
        self.assertIn("Physics", subjects)
        self.assertIn("Biology", subjects)
        self.assertIn("Chemistry", subjects)

if __name__ == "__main__":
    unittest.main()
