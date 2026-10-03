"""
Unit tests for benchmark harness (rlcd_jev.benchmark).
"""

import unittest
from rlcd_jev.benchmark.dataset import BENCHMARK_DATASET
from rlcd_jev.benchmark.evaluator import SystemTwoLLMEvaluator
from rlcd_jev.benchmark.runner import BenchmarkRunner


class TestBenchmark(unittest.TestCase):

    def test_benchmark_dataset_integrity(self):
        self.assertGreater(len(BENCHMARK_DATASET), 5)
        for item in BENCHMARK_DATASET:
            self.assertIn("id", item)
            self.assertIn("prompt", item)
            self.assertIn("ground_truth", item)

    def test_evaluator_response(self):
        evaluator = SystemTwoLLMEvaluator()
        res = evaluator.evaluate("Test prompt for benchmark evaluator")
        self.assertIn("latency_ms", res)
        self.assertIn("tokens_used", res)
        self.assertIn("cost_usd", res)

    def test_benchmark_runner_subset(self):
        subset = BENCHMARK_DATASET[:3]
        runner = BenchmarkRunner(dataset=subset)
        metrics = runner.run_benchmark()

        self.assertEqual(metrics["num_samples"], 3)
        self.assertIn("speedup_factor", metrics)
        self.assertIn("cost_saving_pct", metrics)
        self.assertIn("brier_calibration_score", metrics)


if __name__ == "__main__":
    unittest.main()
