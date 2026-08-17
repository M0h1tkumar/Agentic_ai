# Closed Source vs. Open Source vs. Open Weight AI Models: Architecture, Licensing, Governance & Benchmarks

## Executive Summary

As Artificial Intelligence (AI) and Large Language Models (LLMs) advance, understanding model governance, licensing, reproducibility, and deployment security has become critical for developers, legal teams, and enterprise architects. 

AI models are categorized into three distinct paradigms based on how much of their Intellectual Property (IP)—including model parameters, source code, data curation scripts, and training datasets—is disclosed to the public:
1. **Closed Source (Proprietary / API-only)**
2. **Open Weight (Weights Public, Data/Code Withheld)**
3. **Open Source (Fully OSI-Compliant Open Code, Weights, & Datasets)**

This paper provides an authoritative comparative analysis of these paradigms, incorporates the **Open Source Initiative (OSI) Open Source AI Definition 1.0 (OSAID)**, details regulatory impacts under the **EU AI Act**, and analyzes performance benchmarks.

---

## 1. Defining the Three Paradigms & The OSI Standard

```
+-----------------------------------------------------------------------------------+
|                              AI MODEL CLASSIFICATION                              |
+----------------------+------------------------------------+-----------------------+
|  CLOSED SOURCE       |  OPEN WEIGHT                       |  TRUE OPEN SOURCE     |
|  (Proprietary API)   |  (Weights Available)               |  (OSAID 1.0 Standard) |
+----------------------+------------------------------------+-----------------------+
| * GPT-4o, o1         | * LLaMA 3.1 / 3.2 (Meta)           | * OLMo (Allen AI)     |
| * Claude 3.5 Sonnet  | * Mistral / Mixtral (Mistral AI)   | * BLOOM (BigScience)  |
| * Gemini 1.5 Pro     | * Gemma 2 (Google)                 | * Pythia (EleutherAI) |
+----------------------+------------------------------------+-----------------------+
| Access: Hosted API   | Access: Binary Weight Download     | Access: 100% Artifacts|
+----------------------+------------------------------------+-----------------------+
```

### A. Closed Source (Proprietary) Models
Closed-source models are developed by private commercial entities that keep internal model weights, training datasets, architectural specifications, and hyper-parameters secret. Access is granted exclusively via hosted APIs.

* **Examples:** OpenAI (GPT-4o, GPT-o1, o3-mini), Anthropic (Claude 3.5 Sonnet, Claude 3 Opus), Google (Gemini 1.5 Pro).
* **Key Characteristic:** Zero infrastructure management for users; data is transmitted to vendor servers, processed remotely, and returned via API responses.

---

### B. Open Weight Models
Open-weight models release trained binary parameters for public download, allowing users to execute models locally or host them on private cloud GPU instances. However, vendors typically **withhold** full training datasets, filtering pipelines, and exact data pre-processing code.

* **Examples:** Meta (LLaMA 3.1 8B/70B/405B), Mistral AI (Mistral 7B, Mixtral 8x22B), Google (Gemma 2 2B/9B/27B), DeepSeek (DeepSeek-V3 / R1 open weights).
* **Key Characteristic:** High degree of privacy and local customizability, but lacks complete scientific reproducibility. Often mislabeled as "open source" (a practice known as *openwashing*).

---

### C. True Open Source AI (OSI OSAID 1.0 Standard)
According to the **Open Source Initiative (OSI) Open Source AI Definition (OSAID 1.0)**, an AI system is only "Open Source" if it provides four fundamental freedoms (use, study, modify, share). This mandates public access to:
1. **Model Parameters / Weights:** Under OSI-approved permissive licenses (e.g., Apache 2.0, MIT).
2. **Complete Source Code:** Full code for inference, training, data processing, and tokenization.
3. **Data Information & Provenance:** Detailed information regarding training data composition, dataset provenance, filtering criteria, and cleaning scripts sufficient to allow a skilled team to build a substantially equivalent system.

* **Examples:** Allen Institute for AI's **OLMo**, BigScience's **BLOOM**, EleutherAI's **Pythia**.
* **Key Characteristic:** Full scientific auditability, 100% legal freedom, and unencumbered commercial modification rights.

---

## 2. Comparative Analysis Matrix

| Feature / Dimension | Closed Source Models | Open Weight Models | True Open Source Models (OSAID) |
| :--- | :--- | :--- | :--- |
| **Model Weights Access** | ❌ Hidden (API Only) | ✅ Public Binary Download | ✅ Public Binary Download |
| **Training Code Access** | ❌ Secret | ⚠️ Partial (Inference code) | ✅ 100% Full Source Code |
| **Dataset & Data Provenance**| ❌ Secret / Proprietary | ❌ Withheld / Technical Report | ✅ Disclosed Datasets & Scripts |
| **OSI License Compliance** | ❌ No (SaaS Terms of Service) | ❌ No (Custom restrictive licenses) | ✅ Yes (Apache 2.0 / MIT) |
| **Self-Hosting Capability** | ❌ No (Cloud API dependent) | ✅ Yes (100% Offline / Local) | ✅ Yes (100% Offline / Local) |
| **Data Privacy & Compliance**| ⚠️ Data sent to cloud vendor | ✅ Absolute Local Control | ✅ Absolute Local Control |
| **Legal & Regulatory (EU AI Act)**| Full SaaS Governance | Partial Obligations waived | High Exemption for R&D/Open AI |
| **Fine-Tuning Flexibility** | ⚠️ Restricted (API SFT) | ✅ Full (LoRA, QLoRA, DPO) | ✅ Full Pre-training & Fine-Tuning |

---

## 3. Legal, Regulatory & Governance Impact

> [!WARNING]
> **Regulatory Impact under the EU AI Act:**
> The **EU AI Act** grants specific compliance exemptions for Open Source AI models to foster research and innovation. However, models categorized merely as **Open Weight** with restrictive usage clauses (or models that exceed compute thresholds triggering *Systemic Risk* classification) remain subject to rigorous documentation, transparency, and risk management duties.

### The "Openwashing" Debate
The AI community draws a strict line between Open Weights and Open Source. Open-weight licenses (such as Meta's LLaMA License) contain commercial scale clauses (e.g., requiring explicit licenses if monthly active users exceed 700 million) or field-of-use restrictions. While these licenses benefit developers, they do not comply with the OSI definition of Open Source software.

---

## 4. Benchmark Performance & Intelligence Density

```
+-----------------------------------------------------------------------------------+
|                        BENCHMARK COMPOSITE INDEX COMPARISON                       |
+-----------------------------------------------------------------------------------+
| GPT-4o (Closed)            │ ██████████████████████████████ 88.6 (MMLU-Pro)       |
| Claude 3.5 Sonnet (Closed) │ ███████████████████████████████ 92.0 (SWE-bench)     |
| LLaMA 3.1 405B (Open Wt)   │ ██████████████████████████████ 88.6 (MMLU-Pro)       |
| DeepSeek R1 (Open Wt)      │ ███████████████████████████████ 90.8 (MATH-500)      |
| OLMo 7B (Open Source)      │ █████████████████████ 68.4 (MMLU Standard)           |
+-----------------------------------------------------------------------------------+
```

Recent benchmarks demonstrate that the capability gap between closed-source frontier models and open-weight models has virtually closed:
* **Reasoning & Math:** Open-weight models like **DeepSeek R1** and **LLaMA 3.1 405B** match or exceed GPT-4o on benchmarks like *MATH-500* and *HumanEval*.
* **Scaffolding Advantage in Closed APIs:** Closed-source vendors often augment their raw model weights with hidden system scaffolding (internal multi-step RAG, dynamic system prompts, tool-calling wrappers) which elevates perceived end-user performance beyond raw model inference.

---

## 5. Strategic Recommendation Framework

```
                          +-----------------------------------+
                          |     Enterprise Priority Check     |
                          +-----------------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                                                     |
 [ Maximum Privacy / Zero Vendor Lock-in ]                   [ Zero GPU Maintenance / Fast Launch ]
         |                                                                     |
         v                                                                     v
  OPEN WEIGHT / SOURCE                                                   CLOSED SOURCE
(LLaMA 3.1, DeepSeek, OLMo)                                         (GPT-4o, Claude 3.5)
```

1. **Adopt Closed Source APIs** when speed-to-market is the top priority, reasoning requirements are hyper-complex, and managing multi-GPU server infrastructure is undesirable.
2. **Adopt Open Weight Models** when operating under strict privacy frameworks (HIPAA, GDPR, SOC2), requiring low offline latency, or building custom domain-adapted models via fine-tuning.
3. **Adopt True Open Source (OSAID)** when conducting verifiable academic research, building unencumbered open-source products, or requiring 100% data and code transparency.
