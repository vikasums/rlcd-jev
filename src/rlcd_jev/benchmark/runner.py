"""
Benchmark Execution Engine for System One (Jev RLCD Firewall) vs System Two.
"""

import time
from typing import Dict, Any, List
from rlcd_jev.firewall import ComplianceFirewall
from rlcd_jev.benchmark.evaluator import SystemTwoLLMEvaluator
from rlcd_jev.benchmark.dataset import BENCHMARK_DATASET
from rlcd_jev.core.logger import logger


class BenchmarkRunner:

    def __init__(self, dataset: List[Dict[str, Any]] = None):
        self.dataset = dataset or BENCHMARK_DATASET
        self.firewall = ComplianceFirewall()
        self.llm_evaluator = SystemTwoLLMEvaluator()

    def run_benchmark(self) -> Dict[str, Any]:
        logger.info("Starting Benchmark Execution...")
        print("===============================================================")
        print("       JEV RLCD SYSTEM ONE COMPLIANCE BENCHMARK HARNESS        ")
        print("===============================================================\n")

        # Scenario A: Standard System Two Only
        print("--> Running Scenario A: Traditional System Two LLM Pipeline (100% LLM)...")
        total_cost_a = 0.0
        total_latency_a = 0.0
        total_tokens_a = 0

        for sample in self.dataset:
            res = self.llm_evaluator.evaluate(sample["prompt"])
            total_latency_a += res["latency_ms"]
            total_cost_a += res["cost_usd"]
            total_tokens_a += res["tokens_used"]

        # Scenario B: System One Jev RLCD Firewall Gateway
        print("--> Running Scenario B: Jev RLCD Compliance Firewall Two-Tier Architecture...")
        total_cost_b = 0.0
        total_latency_b = 0.0
        total_tokens_b = 0
        brier_score_sum = 0.0
        correct_classifications = 0

        for sample in self.dataset:
            fw_res = self.firewall.process_request(sample["prompt"])
            decision = self.firewall.engine.evaluate(sample["prompt"])

            actual = 1.0 if sample["ground_truth"] != "SAFE" else 0.0
            prob = decision.is_threat.probability if decision.is_threat.decision else (1.0 - decision.is_threat.probability)
            brier_score_sum += (prob - actual) ** 2

            if decision.category.selected == sample["ground_truth"]:
                correct_classifications += 1

            total_latency_b += fw_res["latency_ms"]

            if fw_res["status"] == "ESCALATED_SYSTEM_TWO":
                llm_res = self.llm_evaluator.evaluate(sample["prompt"])
                total_latency_b += llm_res["latency_ms"]
                total_cost_b += llm_res["cost_usd"]
                total_tokens_b += llm_res["tokens_used"]
            else:
                total_cost_b += 0.00001
                total_tokens_b += 5

        n = len(self.dataset)
        avg_lat_a = total_latency_a / n
        avg_lat_b = total_latency_b / n
        speedup = avg_lat_a / max(1.0, avg_lat_b)

        cost_saving_pct = ((total_cost_a - total_cost_b) / max(0.0001, total_cost_a)) * 100.0
        token_saving_pct = ((total_tokens_a - total_tokens_b) / max(1, total_tokens_a)) * 100.0
        brier_score = brier_score_sum / n
        accuracy_pct = (correct_classifications / n) * 100.0

        metrics = {
            "num_samples": n,
            "scenario_a_lat_ms": round(avg_lat_a, 2),
            "scenario_b_lat_ms": round(avg_lat_b, 2),
            "speedup_factor": round(speedup, 1),
            "scenario_a_cost_usd": round(total_cost_a, 4),
            "scenario_b_cost_usd": round(total_cost_b, 4),
            "cost_saving_pct": round(cost_saving_pct, 2),
            "token_saving_pct": round(token_saving_pct, 2),
            "brier_calibration_score": round(brier_score, 4),
            "classification_accuracy_pct": round(accuracy_pct, 2),
            "firewall_stats": self.firewall.get_metrics()
        }

        self.print_summary(metrics)
        return metrics

    def print_summary(self, m: Dict[str, Any]):
        print("\n===============================================================")
        print("                 BENCHMARK RESULTS SUMMARY                     ")
        print("===============================================================")
        print(f" Total Samples Evaluated        : {m['num_samples']}")
        print(f" Classification Accuracy         : {m['classification_accuracy_pct']}%")
        print(f" Brier Calibration Score         : {m['brier_calibration_score']} (0.00 = perfect calibration)")
        print("---------------------------------------------------------------")
        print(f" Baseline System Two Latency     : {m['scenario_a_lat_ms']} ms / req")
        print(f" System One Firewall Latency    : {m['scenario_b_lat_ms']} ms / req")
        print(f" SPEEDUP FACTOR                 : {m['speedup_factor']}x FASTER ⚡")
        print("---------------------------------------------------------------")
        print(f" Baseline Cost (100% LLM)        : ${m['scenario_a_cost_usd']}")
        print(f" System One Two-Tier Cost        : ${m['scenario_b_cost_usd']}")
        print(f" NET COST REDUCTION              : {m['cost_saving_pct']}% 💰")
        print(f" TOKEN REDUCTION                 : {m['token_saving_pct']}%")
        print("===============================================================\n")
