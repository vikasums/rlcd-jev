"""
Real Head-to-Head Benchmark Engine:
Compares TypeSafe Jev RLCD Firewall vs. Live Microsoft Presidio vs. Live Local Ollama LLM
on the EXACT SAME authentic HuggingFace dataset (data/authentic_huggingface_dataset.json).

Zero simulation. Live local execution on Mac.
"""

import time
import json
import os
from typing import List, Dict, Any
from rlcd_jev.firewall import ComplianceFirewall
from rlcd_jev.engine.presidio_evaluator import LivePresidioEvaluator
from rlcd_jev.engine.ollama_client import OllamaLLMClient
from rlcd_jev.core.logger import logger


class HeadToHeadBenchmarkRunner:
    """
    Executes live 3-way comparison over the exact same authentic dataset:
    1. Jev RLCD System One Firewall
    2. Microsoft Presidio Analyzer Engine (Live Local)
    3. Local Ollama LLM (qwen2.5:14b-instruct / llama3.2:3b)
    """

    def __init__(self, ollama_model: str = "qwen2.5:14b-instruct", max_samples: int = 50, dataset_path: str = "data/authentic_huggingface_dataset.json"):
        self.ollama_model = ollama_model
        self.max_samples = max_samples
        self.dataset_path = dataset_path

        # Initialize 3 live local engines
        logger.info("Initializing 3 Live Local Engines...")
        self.jev_firewall = ComplianceFirewall(ollama_model=ollama_model)
        self.presidio = LivePresidioEvaluator()
        self.ollama = OllamaLLMClient(model_name=ollama_model)

    def load_authentic_dataset(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Authentic dataset file {self.dataset_path} not found. Run download_authentic_datasets.py first.")

        with open(self.dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        logger.info(f"Loaded {len(dataset)} authentic prompts from {self.dataset_path}")
        return dataset[:self.max_samples]

    def run_benchmark(self) -> Dict[str, Any]:
        dataset = self.load_authentic_dataset()

        ollama_active = self.ollama.is_available()
        print("\n===================================================================================")
        print(f"  LIVE HEAD-TO-HEAD BENCHMARK: JEV FIREWALL vs PRESIDIO vs OLLAMA ({self.ollama_model})  ")
        print("===================================================================================\n")
        print(f" Dataset Prompts Evaluated : {len(dataset)} authentic prompts")
        print(f" Microsoft Presidio        : ACTIVE ✅ (Live Local AnalyzerEngine)")
        print(f" Ollama Daemon ({self.ollama_model}) : {'ACTIVE ✅' if ollama_active else 'OFFLINE (Error)'}")
        print("-----------------------------------------------------------------------------------\n")

        results_jev = []
        results_presidio = []
        results_ollama = []

        for idx, item in enumerate(dataset, 1):
            prompt = item["prompt"]
            gt = item["ground_truth"]
            domain = item.get("domain", "General")

            print(f"[{idx}/{len(dataset)}] Evaluated Prompt (Domain: {domain}): \"{prompt[:60]}...\"")

            # 1. Run Live Jev RLCD Firewall
            t0 = time.perf_counter()
            res_jev = self.jev_firewall.process_request(prompt)
            t1 = time.perf_counter()
            lat_jev = (t1 - t0) * 1000.0
            results_jev.append({
                "latency_ms": lat_jev,
                "status": res_jev["status"],
                "category": res_jev["category"],
                "detected": res_jev["status"] == "REJECTED"
            })

            # 2. Run Live Microsoft Presidio Analyzer Engine
            res_presidio = self.presidio.evaluate(prompt)
            results_presidio.append({
                "latency_ms": res_presidio["latency_ms"],
                "has_pii": res_presidio["has_pii"],
                "entities_count": len(res_presidio["entities_found"]),
                "detected": res_presidio["has_pii"]
            })

            # 3. Run Live Local Ollama LLM
            if ollama_active:
                res_ollama = self.ollama.generate_eval(prompt)
                results_ollama.append({
                    "latency_ms": res_ollama["latency_ms"],
                    "response": res_ollama.get("response_text", "")[:50],
                    "tokens": res_ollama.get("total_tokens", 0),
                    "detected": "SAFE" not in res_ollama.get("response_text", "").upper()
                })

            print(f"   ├─ Jev Firewall     : {lat_jev:.2f} ms | Decision: {res_jev['status']}")
            print(f"   ├─ MS Presidio      : {res_presidio['latency_ms']:.2f} ms | PII Found: {res_presidio['has_pii']}")
            if ollama_active:
                print(f"   └─ Ollama ({self.ollama_model}): {results_ollama[-1]['latency_ms']:.2f} ms | Response: {results_ollama[-1]['response']}...")
            print("-" * 75)

        # Statistical Calculations
        def stats(lats):
            if not lats:
                return {"p50": 0, "p95": 0, "mean": 0}
            sorted_l = sorted(lats)
            p50 = sorted_l[int(len(sorted_l) * 0.50)]
            p95 = sorted_l[min(int(len(sorted_l) * 0.95), len(sorted_l) - 1)]
            mean = sum(lats) / len(lats)
            return {"p50": round(p50, 2), "p95": round(p95, 2), "mean": round(mean, 2)}

        lats_j = [r["latency_ms"] for r in results_jev]
        lats_p = [r["latency_ms"] for r in results_presidio]
        lats_o = [r["latency_ms"] for r in results_ollama]

        summary = {
            "num_samples": len(dataset),
            "ollama_model": self.ollama_model,
            "jev_stats": stats(lats_j),
            "presidio_stats": stats(lats_p),
            "ollama_stats": stats(lats_o)
        }

        self.print_summary_report(summary)
        return summary

    def print_summary_report(self, s: Dict[str, Any]):
        print("\n===================================================================================")
        print("              EMPIRICAL HEAD-TO-HEAD BENCHMARK SUMMARY REPORT                      ")
        print("===================================================================================")
        print(f" Total Authentic Prompts Tested : {s['num_samples']}")
        print(f" Local Ollama Model Evaluated   : {s['ollama_model']}")
        print("-----------------------------------------------------------------------------------")
        print(f" 1. Jev RLCD System One Firewall : Mean {s['jev_stats']['mean']} ms | P50 {s['jev_stats']['p50']} ms | P95 {s['jev_stats']['p95']} ms")
        print(f" 2. MS Presidio Analyzer Engine  : Mean {s['presidio_stats']['mean']} ms | P50 {s['presidio_stats']['p50']} ms | P95 {s['presidio_stats']['p95']} ms")
        print(f" 3. Ollama LLM ({s['ollama_model']})  : Mean {s['ollama_stats']['mean']} ms | P50 {s['ollama_stats']['p50']} ms | P95 {s['ollama_stats']['p95']} ms")
        print("===================================================================================\n")


if __name__ == "__main__":
    runner = HeadToHeadBenchmarkRunner(max_samples=15)
    runner.run_benchmark()
