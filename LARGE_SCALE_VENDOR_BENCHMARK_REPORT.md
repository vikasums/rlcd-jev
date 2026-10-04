# 🏛️ Large-Scale AI Firewall Benchmark & Industry Vendor Analysis Report
## *Empirical 2,000+ Prompt Dataset Evaluation & Enterprise Vendor Ecosystem Breakdown*

**Generated At**: 2026-10-04 10:12:06  
**Total Dataset Prompts Evaluated**: **`2000` prompts**  
**Execution Throughput**: **`3712.2 requests / sec`**  
**Execution Time**: **`0.54 seconds`**  

---

## 🎯 1. Dataset Breakdown & Composition

The evaluation benchmark was executed over a balanced multi-domain dataset suite containing **`2000` prompts** across 4 primary risk categories:

| Dataset Domain Category | Prompt Count | Description & Target Payload |
| :--- | :--- | :--- |
| **Compliance / PII & Data Privacy** | `500` | SSNs, Credit Cards, Emails, Auth Tokens, Database URLs |
| **Security / Prompt Injection & Jailbreaks** | `500` | System prompt overrides, DAN mode, encoded payloads |
| **Security / Toxicity & Malware** | `300` | Malware scripts, DDoS triggers, exploit keyloggers |
| **Routing / Safe Knowledge Queries** | `700` | Coding, FAQ, general knowledge, customer support queries |
| **TOTAL DATASET SIZE** | **`2000`** | **Comprehensive Multi-Domain AI Safety Suite** |

---

## ⚡ 2. Empirical Benchmark Performance Metrics

### Latency Percentiles (End-to-End Decision Gating)
* **Mean Latency**: **`0.262 ms`**
* **P50 (Median)**: **`0.24 ms`**
* **P90**: **`0.3 ms`**
* **P95**: **`0.33 ms`**
* **P99 (Max Tail)**: **`0.69 ms`**

### Classification Confusion Matrix & Calibration
* **Classification Accuracy**: **`80.35%`**
* **Precision**: **`100.0%`**
* **Recall / Sensitivity**: **`69.77%`**
* **F1-Score**: **`82.19%`**
* **Brier Calibration Score**: **`0.1828`** (0.00 = perfect probability calibration)

| Confusion Matrix Metric | Count | Explanation |
| :--- | :--- | :--- |
| **True Positives (TP)** | `907` | Security threat / PII leak correctly blocked |
| **True Negatives (TN)** | `700` | Safe user prompt correctly fast-passed |
| **False Positives (FP)** | `0` | Safe prompt incorrectly flagged |
| **False Negatives (FN)** | `393` | Security threat incorrectly passed |

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

## 💡 Key Architectural Insights

1. **Regex vs Classifiers vs LLMs vs System 1 RLCD**:
   * Pure Regex (e.g., Presidio / Datadog) is ultra-fast for static patterns (SSNs, emails), but fails on semantic prompt injections or contextual policy breaches.
   * Generative LLM Guardrails (e.g., NeMo / System Two evaluators) catch semantic nuances, but incur unacceptable latency bottlenecks (**1–3 seconds**) and high token spend.
   * **System One Jev RLCD** bridges the gap: It evaluates non-generative typed primitives (`Choice`, `Score`, `Noul`) in a **single parallel pass (<70ms API / <1ms local)** with mathematically calibrated probability scores.

2. **Defense in Depth Recommendation**:
   An enterprise production AI gateway should stack:
   * **Tier 1 (Fast Pattern Gating)**: Regex & Heuristics (`scan_pii`, `detect_prompt_injection`) < 0.05ms
   * **Tier 2 (System One Decision Engine)**: TypeSafe Jev RLCD Primitives (`Choice`, `Score`, `Noul`) < 1ms - 70ms
   * **Tier 3 (System Two LLM Synthesis)**: Frontier LLM (GPT-4 / Claude / Ollama) reserved strictly for ambiguous queries ($P < 0.90$).

---

## 🏛️ Verification & Audit Proof

To re-run this 2,000+ prompt large-scale benchmark on your machine:

```bash
python3 main.py --large-benchmark 2000
```
