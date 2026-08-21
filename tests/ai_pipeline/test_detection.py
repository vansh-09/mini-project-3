import unittest
from ai_pipeline.detection.detector import DiagramDetector
from ai_pipeline.detection.event_grouping import EventGrouper

class TestDiagramDetection(unittest.TestCase):
    def test_detector_instantiation(self):
        detector = DiagramDetector(confidence_threshold=0.5)
        self.assertEqual(detector.confidence_threshold, 0.5)

    def test_nonexistent_frame_detection(self):
        detector = DiagramDetector()
        res = detector.is_diagram_frame("nonexistent_frame.jpg")
        self.assertFalse(res["is_diagram"])

    def test_event_grouping(self):
        grouper = EventGrouper(max_gap_seconds=3.0)
        detections = [
            {"frame_path": "f1.jpg", "timestamp": 1.0, "is_diagram": True, "diagram_type": "chart"},
            {"frame_path": "f2.jpg", "timestamp": 2.0, "is_diagram": True, "diagram_type": "chart"},
            {"frame_path": "f3.jpg", "timestamp": 10.0, "is_diagram": True, "diagram_type": "chart"},
        ]
        events = grouper.group_detections(detections)
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["timestamp"], 1.0)
        self.assertEqual(events[1]["timestamp"], 10.0)

if __name__ == "__main__":
    unittest.main()
