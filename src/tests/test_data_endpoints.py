import unittest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app

client = TestClient(app)

class TestDataEndpoints(unittest.TestCase):
    def test_get_data_endpoint(self):
        response = client.get("/api/data/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("stock_data", response.json())

    def test_post_data_validation(self):
        valid_data = {
            "datetime": "2024-03-20T10:00:00",
            "open": 100.50,
            "high": 101.20,
            "low": 99.80,
            "close": 100.90,
            "volume": 1000
        }
        response = client.post("/api/data/", json=valid_data)
        self.assertEqual(response.status_code, 200)

        invalid_datetime = valid_data.copy()
        invalid_datetime["datetime"] = "invalid-date"
        response = client.post("/api/data/", json=invalid_datetime)
        self.assertEqual(response.status_code, 422)

        invalid_numeric = valid_data.copy()
        invalid_numeric["open"] = "not-a-number"
        response = client.post("/api/data/", json=invalid_numeric)
        self.assertEqual(response.status_code, 422)

        missing_fields = {
            "datetime": "2024-03-20T10:00:00",
            "open": 100.50
        }
        response = client.post("/api/data/", json=missing_fields)
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main() 
