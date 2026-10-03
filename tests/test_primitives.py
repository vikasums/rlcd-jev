"""
Unit tests for typed primitives (rlcd_jev.primitives).
"""

import unittest
from rlcd_jev.primitives import Choice, Score, Noul, RiskLevel


class TestPrimitives(unittest.TestCase):

    def test_choice_primitive(self):
        choice = Choice(selected="SAFE", options=["SAFE", "UNSAFE"], confidence=0.95)
        self.assertEqual(choice.selected, "SAFE")
        self.assertTrue(choice.is_confident(0.90))
        self.assertFalse(choice.is_confident(0.98))

    def test_score_primitive_levels(self):
        score_low = Score.from_rating(1.0, max_val=5.0)
        self.assertEqual(score_low.level, RiskLevel.LOW)

        score_med = Score.from_rating(2.0, max_val=5.0)
        self.assertEqual(score_med.level, RiskLevel.MEDIUM)

        score_high = Score.from_rating(3.5, max_val=5.0)
        self.assertEqual(score_high.level, RiskLevel.HIGH)

        score_crit = Score.from_rating(4.5, max_val=5.0)
        self.assertEqual(score_crit.level, RiskLevel.CRITICAL)

    def test_noul_primitive(self):
        noul_true = Noul(decision=True, probability=0.98, proposition="is_threat")
        self.assertTrue(noul_true.exceeds_threshold(0.90))

        noul_false = Noul(decision=False, probability=0.05, proposition="is_threat")
        self.assertTrue(noul_false.exceeds_threshold(0.90))


if __name__ == "__main__":
    unittest.main()
