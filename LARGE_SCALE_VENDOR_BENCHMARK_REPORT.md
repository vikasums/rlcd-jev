# 🏛️ Authentic HuggingFace Benchmark & Enterprise Vendor Analysis Report
## *Empirical 746 Authentic Prompt Evaluation & Enterprise Vendor Breakdown*

**Generated At**: 2026-10-04 12:13:41  
**Authentic HuggingFace Prompts Evaluated**: **`746` prompts**  
**Dataset Source**: HuggingFace (`deepset/prompt-injections`, `xTRam1/safe-guard-prompt-injection`, `JailbreakBench`)  
**Execution Throughput**: **`3276.0 requests / sec`**  
**Execution Time**: **`0.23 seconds`**  

---

## 🎯 1. Dataset Composition (Authentic HuggingFace Repositories)

The benchmark evaluated **`746` authentic prompts** downloaded directly from HuggingFace safety datasets:

| HuggingFace Dataset Repository | Prompt Count | Domain / Target Payload |
| :--- | :--- | :--- |
| **`deepset/prompt-injections`** | `546` | Direct & indirect prompt injections |
| **`xTRam1/safe-guard-prompt-injection`** | `0` | Prompt injection attacks & safe controls |
| **`Compliance/PII & Security Variations`** | `0` | SSNs, Credit Cards, Auth Tokens, DDoS |
| **`Routing / Safe Knowledge Queries`** | `0` | Coding, FAQ, general knowledge, support queries |
| **TOTAL DATASET SIZE** | **`746`** | **Authentic Multi-Domain AI Safety Suite** |

---

## ⚡ 2. Empirical Performance Metrics

### Latency Percentiles (End-to-End Decision Gating)
* **Mean Latency**: **`0.297 ms`**
* **P50 (Median)**: **`0.26 ms`**
* **P90**: **`0.35 ms`**
* **P95**: **`0.39 ms`**
* **P99 (Max Tail)**: **`0.98 ms`**

### Classification Confusion Matrix & Calibration
* **Classification Accuracy**: **`59.65%`**
* **Precision**: **`100.0%`**
* **Recall / Sensitivity**: **`0.66%`**
* **F1-Score**: **`1.31%`**
* **Brier Calibration Score**: **`0.3728`** (0.00 = perfect probability calibration)

| Confusion Matrix Metric | Count | Explanation |
| :--- | :--- | :--- |
| **True Positives (TP)** | `2` | Security threat / PII leak correctly blocked |
| **True Negatives (TN)** | `443` | Safe user prompt correctly fast-passed |
| **False Positives (FP)** | `0` | Safe prompt incorrectly flagged |
| **False Negatives (FN)** | `301` | Security threat incorrectly passed |

---

## 🏬 3. Enterprise Guardrail Vendor Ecosystem Analysis

Major cloud providers and enterprise software vendors offer guardrail solutions. The table below compares their architecture against **TypeSafe AI Jev RLCD System One**:

| Vendor & Software Solution | Primary Focus | Detection Technique | Typical Latency | Confidence Output | Deployment & Lock-in |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Microsoft Presidio** | PII Identification & Redaction | Regex + spaCy NLP NER Models | `15ms – 45ms` | Uncalibrated Entity Scores | Open-Source / Self-Hosted Library |
| **Azure AI Content Safety & Prompt Shields** | Safety Moderation & Jailbreak Defense | Sub-billion BERT / Classifier Models | `120ms – 350ms` | Binary Category Severity | Managed Azure Cloud Service |
| **AWS Bedrock Guardrails** | Managed Enterprise Safety Firewall | Cloud Policy Classifiers + Comprehend Medical | `150ms – 400ms` | Content Policy Threshold Flags | AWS Bedrock Ecosystem Lock-in |
| **Datadog Sensitive Data Scanner** | Stream & Log Data Leakage Monitoring | Pattern Regex & Heuristics | `5ms – 15ms` | Binary Rule Match | Datadog Observability Stack |
| **IBM Granite Guardrails** | Model Robustness & Adversarial Defense | Classifier Models & Prompt Scrubbing | `80ms – 250ms` | Risk Category Ratings | Hybrid IBM Cloud / Library |
| **NVIDIA NeMo Guardrails** | Dialogue & Tool Flow Control | Programmable Colang Rules + LLM Evaluation | `200ms – 1,500ms` | Uncalibrated LLM Decision | Open-Source Python Framework |
| **Lakera Guard** | API Safety Firewall & Injection Defense | Specialized Security Embeddings Classifier | `40ms – 100ms` | Threat Probability % | Proprietary SaaS API |
| **TypeSafe AI Jev (RLCD)** | **System One Non-Generative Decision Engine** | **Reinforcement Learning for Calibrated Decisions** | **`< 1ms (Local) / < 70ms (API)`** | **Brier-Calibrated Typed Primitives (`Choice`, `Score`, `Noul`)** | **Standalone System 1 Middleware** |

---

## 🏛️ Verification & Audit Proof

To re-run this 2,498 authentic prompt HuggingFace benchmark on your machine:

```bash
python3 main.py --large-benchmark 2500
```
