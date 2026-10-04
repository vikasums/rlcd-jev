"""
Downloader module to fetch thousands of authentic prompts directly from HuggingFace Datasets API.
Saves data into data/authentic_huggingface_dataset.json.
"""

import os
import json
import urllib.request
import urllib.error
import time
from typing import List, Dict, Any
from rlcd_jev.core.logger import logger
from rlcd_jev.benchmark.dataset_generator import generate_large_scale_dataset


def fetch_hf_rows(dataset_name: str, config: str = "default", split: str = "train", limit: int = 100, max_rows: int = 1000) -> List[Dict[str, Any]]:
    """Fetches rows from HuggingFace datasets server API."""
    rows = []
    offset = 0
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    logger.info(f"Downloading authentic prompts from HuggingFace [{dataset_name}] (target: {max_rows})...")

    while len(rows) < max_rows:
        url = f"https://datasets-server.huggingface.co/rows?dataset={dataset_name}&config={config}&split={split}&offset={offset}&limit={limit}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                fetched = data.get("rows", [])
                if not fetched:
                    break
                rows.extend(fetched)
                offset += len(fetched)
                time.sleep(0.1)
        except Exception as e:
            logger.warning(f"Error fetching {dataset_name} at offset {offset}: {e}")
            break

    logger.info(f"Successfully downloaded {len(rows)} authentic rows from HuggingFace [{dataset_name}]")
    return rows


def build_authentic_huggingface_dataset(target_size: int = 2500, output_path: str = "data/authentic_huggingface_dataset.json") -> List[Dict[str, Any]]:
    """
    Downloads and parses thousands of authentic prompts directly from HuggingFace APIs:
    1. deepset/prompt-injections (660+ prompts)
    2. xTRam1/safe-guard-prompt-injection (1,000+ prompts)
    3. Synthetic Enterprise PII, Toxicity & Routing Variations (800+ prompts)
    """
    os.makedirs(os.path.dirname(output_path) or "data", exist_ok=True)
    dataset = []

    # 1. Download deepset/prompt-injections
    raw_deepset = fetch_hf_rows("deepset/prompt-injections", limit=100, max_rows=700)
    for idx, item in enumerate(raw_deepset, 1):
        row = item.get("row", {})
        prompt_text = row.get("text", "").strip()
        label_num = row.get("label", 0)  # 1 = injection, 0 = safe
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

    # 2. Download xTRam1/safe-guard-prompt-injection
    raw_xtram = fetch_hf_rows("xTRam1/safe-guard-prompt-injection", limit=100, max_rows=1200)
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

    # 3. Add Synthetic Enterprise PII, Toxicity & Routing Variations to reach target_size
    synthetic_needed = max(100, target_size - len(dataset))
    synthetic_items = generate_large_scale_dataset(num_samples=synthetic_needed)
    dataset.extend(synthetic_items)

    # Save to local file data/authentic_huggingface_dataset.json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    logger.info(f"Saved {len(dataset)} authentic prompts into {output_path}")
    return dataset


if __name__ == "__main__":
    build_authentic_huggingface_dataset()
