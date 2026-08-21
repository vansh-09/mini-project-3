import unittest
from fastapi.testclient import TestClient
from app import app

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_status_endpoint(self):
        res = self.client.get("/api/status")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")

    def test_lectures_list(self):
        res = self.client.get("/api/lectures")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["lectures"], list)

if __name__ == "__main__":
    unittest.main()
