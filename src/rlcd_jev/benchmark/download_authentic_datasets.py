"""
Downloader module to fetch 100% authentic datasets directly from HuggingFace APIs:
1. JailbreakBench/JBB-Behaviors (Harmful & Benign splits)
2. deepset/prompt-injections
3. xTRam1/safe-guard-prompt-injection
Retries on network timeouts. Zero simulation fallback.
"""

import os
import json
import urllib.request
import urllib.error
import time
from typing import List, Dict, Any
from rlcd_jev.core.logger import logger


def fetch_hf_rows(dataset_name: str, config: str = "default", split: str = "train", limit: int = 100, max_rows: int = 1000) -> List[Dict[str, Any]]:
    """Fetches rows directly from HuggingFace datasets server API with network retries."""
    rows = []
    offset = 0
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    logger.info(f"Downloading authentic prompts from HuggingFace [{dataset_name} | {config} | {split}] (target: {max_rows})...")

    while len(rows) < max_rows:
        url = f"https://datasets-server.huggingface.co/rows?dataset={dataset_name}&config={config}&split={split}&offset={offset}&limit={limit}"
        success = False
        
        for attempt in range(1, 4):  # Up to 3 network retries
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30.0) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    fetched = data.get("rows", [])
                    if not fetched:
                        success = True
                        break
                    rows.extend(fetched)
                    offset += len(fetched)
                    success = True
                    time.sleep(0.1)
                    break
            except Exception as e:
                logger.warning(f"Network retry {attempt}/3 for {dataset_name} at offset {offset}: {e}")
                time.sleep(1.0 * attempt)

        if not success:
            logger.error(f"Stopping download for {dataset_name} at offset {offset} due to network timeout.")
            break

    logger.info(f"Successfully downloaded {len(rows)} authentic rows from HuggingFace [{dataset_name} | {config} | {split}]")
    return rows


def build_authentic_huggingface_dataset(output_path: str = "data/authentic_huggingface_dataset.json") -> List[Dict[str, Any]]:
    """
    Downloads and compiles 100% authentic dataset records:
    - JailbreakBench/JBB-Behaviors (harmful & benign)
    - deepset/prompt-injections
    - xTRam1/safe-guard-prompt-injection
    Zero simulation.
    """
    os.makedirs(os.path.dirname(output_path) or "data", exist_ok=True)
    dataset = []

    # 1. Download JailbreakBench harmful behaviors
    raw_jbb_harmful = fetch_hf_rows("JailbreakBench/JBB-Behaviors", config="behaviors", split="harmful", limit=100, max_rows=100)
    for idx, item in enumerate(raw_jbb_harmful, 1):
        row = item.get("row", {})
        prompt_text = row.get("Goal", "").strip() or row.get("Behavior", "").strip()
        if prompt_text:
            dataset.append({
                "id": f"hf-jbb-harmful-{idx}",
                "domain": "Security/JailbreakBench",
                "dataset_source": "HuggingFace: JailbreakBench/JBB-Behaviors (harmful split)",
                "paper_citation": "Chao et al. (2024). JailbreakBench: An Open Robustness Benchmark for LLMs. arXiv:2404.01318",
                "prompt": prompt_text,
                "ground_truth": "TOXIC_CONTENT"
            })

    # 2. Download JailbreakBench benign behaviors
    raw_jbb_benign = fetch_hf_rows("JailbreakBench/JBB-Behaviors", config="behaviors", split="benign", limit=100, max_rows=100)
    for idx, item in enumerate(raw_jbb_benign, 1):
        row = item.get("row", {})
        prompt_text = row.get("Goal", "").strip() or row.get("Behavior", "").strip()
        if prompt_text:
            dataset.append({
                "id": f"hf-jbb-benign-{idx}",
                "domain": "Routing/JailbreakBenchBenign",
                "dataset_source": "HuggingFace: JailbreakBench/JBB-Behaviors (benign split)",
                "paper_citation": "Chao et al. (2024). JailbreakBench: An Open Robustness Benchmark for LLMs. arXiv:2404.01318",
                "prompt": prompt_text,
                "ground_truth": "SAFE"
            })

    # 3. Download deepset/prompt-injections
    raw_deepset = fetch_hf_rows("deepset/prompt-injections", config="default", split="train", limit=100, max_rows=700)
    for idx, item in enumerate(raw_deepset, 1):
        row = item.get("row", {})
        prompt_text = row.get("text", "").strip()
        label_num = row.get("label", 0)
        ground_truth = "PROMPT_INJECTION" if label_num == 1 else "SAFE"
        if prompt_text:
            dataset.append({
                "id": f"hf-deepset-{idx}",
                "domain": "Security/DeepsetPromptInjections",
                "dataset_source": "HuggingFace: deepset/prompt-injections",
                "paper_citation": "Deepset AI (2023). Deepset Prompt Injections Dataset. HuggingFace: deepset/prompt-injections",
                "prompt": prompt_text,
                "ground_truth": ground_truth
            })

    # 4. Download xTRam1/safe-guard-prompt-injection
    raw_xtram = fetch_hf_rows("xTRam1/safe-guard-prompt-injection", config="default", split="train", limit=100, max_rows=1000)
    for idx, item in enumerate(raw_xtram, 1):
        row = item.get("row", {})
        prompt_text = row.get("prompt", "").strip() or row.get("text", "").strip()
        label_str = str(row.get("label", "0")).lower()
        ground_truth = "PROMPT_INJECTION" if ("1" in label_str or "injection" in label_str) else "SAFE"
        if prompt_text:
            dataset.append({
                "id": f"hf-xtram1-{idx}",
                "domain": "Security/SafeGuardInjection",
                "dataset_source": "HuggingFace: xTRam1/safe-guard-prompt-injection",
                "paper_citation": "xTRam1 (2023). Safe Guard Prompt Injection Dataset. HuggingFace: xTRam1/safe-guard-prompt-injection",
                "prompt": prompt_text,
                "ground_truth": ground_truth
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    logger.info(f"Saved {len(dataset)} 100% authentic HuggingFace prompts into {output_path}")
    return dataset


if __name__ == "__main__":
    build_authentic_huggingface_dataset()
