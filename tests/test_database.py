"""
Unit tests for audit database module (rlcd_jev.core.database).
"""

import os
import unittest
import tempfile
from rlcd_jev.core.database import AuditDatabase


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.db = AuditDatabase(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_db_initialization(self):
        self.assertTrue(os.path.exists(self.db_path))

    def test_log_decision_and_retrieval(self):
        success = self.db.log_decision(
            status="APPROVED_FAST_PASS",
            risk_level="Low",
            category="SAFE",
            confidence=0.96,
            latency_ms=0.15,
            prompt="Test prompt",
            details={"test_key": "test_val"}
        )
        self.assertTrue(success)

        logs = self.db.get_recent_logs(limit=10)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["status"], "APPROVED_FAST_PASS")
        self.assertEqual(logs[0]["risk_level"], "Low")
        self.assertEqual(logs[0]["category"], "SAFE")
        self.assertEqual(logs[0]["confidence"], 0.96)


if __name__ == "__main__":
    unittest.main()
