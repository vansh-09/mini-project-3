import unittest
from ai_pipeline.explanation.llm_service import LLMExplanationService

class TestLLMExplanation(unittest.TestCase):
    def test_fallback_explanations(self):
        service = LLMExplanationService()
        res = service.generate_bilingual_explanations("Test VLM analysis", subject="Physics")
        self.assertIn("en", res)
        self.assertIn("hi", res)
        self.assertTrue(len(res["en"]) > 20)
        self.assertTrue(len(res["hi"]) > 20)

if __name__ == "__main__":
    unittest.main()
