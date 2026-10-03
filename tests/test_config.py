"""
Unit tests for configuration module (rlcd_jev.core.config).
"""

import os
import unittest
from rlcd_jev.core.config import Settings, load_dotenv


class TestConfig(unittest.TestCase):

    def test_default_settings(self):
        settings = Settings()
        self.assertIsNotNone(settings.typesafe_model_name)
        self.assertIsNotNone(settings.system_two_model_name)
        self.assertGreaterEqual(settings.confidence_threshold, 0.0)
        self.assertLessEqual(settings.confidence_threshold, 1.0)

    def test_env_loading(self):
        os.environ["FIREWALL_CONFIDENCE_THRESHOLD"] = "0.85"
        settings = Settings()
        self.assertEqual(settings.confidence_threshold, 0.85)

    def test_boolean_env_parsing(self):
        os.environ["FIREWALL_ENABLE_DB_AUDIT"] = "false"
        settings = Settings()
        self.assertFalse(settings.enable_db_audit)


if __name__ == "__main__":
    unittest.main()
