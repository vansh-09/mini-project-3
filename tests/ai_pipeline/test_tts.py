import unittest
import os
from pathlib import Path
from ai_pipeline.tts.tts_service import TTSService

class TestTTS(unittest.TestCase):
    def test_synthesize_bilingual(self):
        tts = TTSService()
        res = tts.synthesize_bilingual("Test English audio", "परीक्षण हिंदी ऑडियो", "test_evt")
        self.assertIn("audio_en", res)
        self.assertIn("audio_hi", res)
        self.assertTrue(res["audio_en"].startswith("/storage/audio/"))
        self.assertTrue(res["audio_hi"].startswith("/storage/audio/"))

if __name__ == "__main__":
    unittest.main()
