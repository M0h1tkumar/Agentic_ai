# Anil Pradhan - Agentic AI Learning Workspace

Welcome to my personal progress tracker and repository for the **Agentic AI Course**. This folder tracks all research documentation, practical setups, and hands-on tool implementations as part of **Team Ritu** (`Team_Ritu`).

---

## 📌 Status Summary

| Category | Total Tasks | Completed | Status |
| :--- | :---: | :---: | :---: |
| 📄 **GitHub Research Papers** | 8 | 8 | 🟢 **100% Completed** |
| 🛠️ **Practical / Hands-On Tasks** | 8 | 5 | 🟢 **62.5% Completed** |

---

## 📄 1. GitHub Research Papers (`Tasks_Github/`)

All 8 research papers have been thoroughly researched, written, and saved under the [`Tasks_Github/`](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/) directory:

1. ✅ **[Task 1: Chatbot vs. AI Agent](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/1-chatbot_Vs_Aiagents.md)**
   - *Topics:* Evolution, architectural differences, reactive vs. proactive execution, decision loops, and real-world use cases.
2. ✅ **[Task 2: Privacy Policies of Major LLM Providers](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/2-privacy_policies_of_llms.md)**
   - *Topics:* Data retention, telemetry, opt-out policies, and enterprise security across OpenAI, Google Gemini, and Anthropic Claude.
3. ✅ **[Task 3: Closed Source vs. Open Source vs. Open Weight Models](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/3-closed_open_source_open_weight_models.md)**
   - *Topics:* OSI Open Source AI Definition (**OSAID 1.0**), EU AI Act regulatory impact, "Openwashing" debate, and intelligence index benchmarks.
4. ✅ **[Task 4: Top 3 Tools for Model Training & Fine-Tuning](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/4-model_training_and_tuning_tools.md)**
   - *Topics:* **Unsloth** (Triton CUDA kernels & 30-90% VRAM cuts), **Hugging Face TRL/AutoTrain**, **LLaMA-Factory**, and QLoRA NF4 mathematical breakdown.
5. ✅ **[Task 5: LLM vs. SLM Comparative Analysis](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/5-llm_vs_slm.md)**
   - *Topics:* Parameter scaling boundaries (>70B vs <14B SLMs), synthetic data curation (Phi-3.5/Phi-4), knowledge distillation, VRAM tables, and edge NPU execution.
6. ✅ **[Task 6: Model File Formats & Deep-Dive into GGUF](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/6-model_formats_and_gguf.md)**
   - *Topics:* PyTorch (`.pt` pickle security), SafeTensors, ONNX, and GGUF v3. Explains K-quants vs. I-quants (`IQ3_M`), Importance Matrix (`imatrix`), and hybrid CPU+GPU layer offloading.
7. ✅ **[Task 7: API vs. MCP (Model Context Protocol) & Drawbacks](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/7-api_vs_mcp_and_drawbacks.md)**
   - *Topics:* Architectural comparison between traditional REST APIs and MCP (JSON-RPC 2.0 Host-Client-Server), and detailed drawbacks of APIs in AI (N+1 glue code explosion, context window bloat, static vs dynamic discovery, lack of HITL safety guardrails).
8. ✅ **[Task 8: Comparative Analysis of MCP Transports: STDIO vs. Streamable HTTP](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/Tasks_Github/8-stdio_vs_streamable_http_mcp_transports.md)**
   - *Topics:* Deep architectural analysis of STDIO (local IPC, stdout framing fragility, memory scaling) vs. Streamable HTTP (stateless core, header-based routing, OAuth 2.1), performance benchmarks (latency, cold-start, concurrency), and enterprise hybrid topologies.

---

## 🛠️ 2. Practical & Hands-On Setup Progress

Below is the roadmap and real-time completion status for all hands-on environment setups:

### Task 1: AnythingLLM Setup
- [x] Multi-user enablement
- [x] Browser search integration
- [x] Nvidia API connection / OpenRouter setup
- [x] Vector Database connection (Qdrant / LanceDB)
- [x] Relational Database connection (MySQL / PostgreSQL)
- [x] Full trial run & validation
> **Status:** ✅ **Completed**

---

### Task 2: Markdown (`.md`) File Conversion
- [x] MarkItDown / Docling installation & setup
- [x] Python script for converting `.pdf`, `.docx`, etc. to clean `.md`
- [x] Connect automated Markdown pipeline to AnythingLLM
> **Status:** ✅ **Completed**

---

### Task 3: Local LLM Execution Runtimes
- [x] LM Studio setup & GGUF model loading
- [x] Jan Desktop local inference test
- [x] OpenHands autonomous coding agent environment configuration
> **Status:** ✅ **Completed**

---

### Task 4: Model Fine-Tuning with Unsloth (SupportSense Project)
- [x] Dataset selection & formatting: **BANKING77** dataset (1,000 train / 300 test examples)
- [x] Base model selection & quantization: **Qwen2.5-7B-Instruct** with **Unsloth** & **QLoRA** (4-bit quantization)
- [x] Parameter Efficiency: 40.37M trainable parameters (0.53% of 7.65B total parameters)
- [x] Model fine-tuning run: Google Colab Tesla T4 GPU (~12 min, 2 epochs)
- [x] Evaluation Accuracy: **91.67% test accuracy** (275 / 300 test examples correctly classified)
- [x] Project Architecture: [`SupportSense-FineTuning/`](file:///c:/Users/ANIL/Desktop/Agentic_ai/Team_Ritu/Anil_Pradhan/SupportSense-FineTuning/) (`dataset/`, `evaluation/`, `model/`, `notebooks/`, `outputs/`, `requirements.txt`, `.gitignore`)
> **Status:** ✅ **Completed**

---

### Task 5: Skill Inspector & Security Auditing
- [ ] OpenClaw / ClawHub / Hermes integration
- [ ] Download AI agent skills
- [ ] Vulnerability and safety inspection on downloaded skills
> **Status:** ⏳ **Pending**

---

### Task 6: Sandbox Setup & Virtual Machine Isolation
- [ ] Setup Virtual Machine / Sandbox container
- [ ] Migrate Agentic AI experimental scripts into VM environment for safety
> **Status:** ⏳ **Pending**

---

### Task 7: Multica & Advanced MCP Integration
- [x] Compulsory installation of Multica (through Docker)
- [x] Create workspace for team *(implemented by team leaders)*
- [x] Connect Multica workspace with Slack
- [x] Experiment with OpenCode (best for runtime execution)
- [x] Experiment with Microsoft Recorder skills
- [x] *(Advanced Task)* Connect AnythingLLM's RAG database to Multica/OpenClaw by exposing it as an MCP server (enables Multica agents to retrieve and use documents stored in AnythingLLM during execution)
> **Status:** ✅ **Completed**

---

### Task 8: Multica Agent Deployment Exercises
- [ ] **Exercise #1: Explainer_Agent**
  - [ ] Objective: Multica agent answering questions about people, places, topics, and events using live Wikipedia lookups (`@cyanheads/wikipedia-mcp-server`)
  - [ ] Skill definition & task assignment to `Explainer_Agent`: Summarize Mahatma Gandhi, list existing Wikipedia sections, and share "Legacy" section content
- [ ] **Exercise #2: Custom Agent Deployment in Multica Instance**
  - [ ] `Currency_Converter_Agent`: Convert 500 USD to INR & show today's rate for EUR to INR
  - [ ] `World_Clock_Agent`: Time right now in Tokyo, London, and New York
  - [ ] `Definition_Agent`: Define 'ubiquitous' and provide an example sentence
  - [ ] `HackerNews_Digest_Agent`: Retrieve top 5 Hacker News stories with scores
  - [ ] `GitHub_Repo_Agent`: Open issues count and 3 most recently updated issues for `anthropics/claude-code`
  - [ ] `Create a Squad including the other agents so that the Orchestrator Agent can coordinate their tasks`
> **Status:** ⏳ **In Progress / Pending**

---

## 📂 Repository Directory Structure

```
Team_Ritu/Anil_Pradhan/
├── README.md                                  # Workspace overview & task tracker
├── SupportSense-FineTuning/                   # Task 4: SupportSense LLM Fine-Tuning Project
│   ├── dataset/                               # BANKING77 dataset documentation
│   ├── evaluation/                            # 91.67% evaluation accuracy specs
│   ├── model/                                 # Qwen2.5-7B base model & LoRA adapter specs
│   ├── notebooks/                             # SupportSense_FineTuning.ipynb
│   ├── outputs/                               # LoRA adapter checkpoint docs
│   ├── requirements.txt                       # Project dependencies
│   ├── .gitignore                             # Ignore rules for models & .venv
│   └── README.md                              # SupportSense project README
└── Tasks_Github/                              # Research Papers & Documentation
    ├── 1-chatbot_Vs_Aiagents.md               # Task 1 Paper
    ├── 2-privacy_policies_of_llms.md          # Task 2 Paper
    ├── 3-closed_open_source_open_weight_models.md # Task 3 Paper
    ├── 4-model_training_and_tuning_tools.md   # Task 4 Paper
    ├── 5-llm_vs_slm.md                        # Task 5 Paper
    ├── 6-model_formats_and_gguf.md            # Task 6 Paper
    ├── 7-api_vs_mcp_and_drawbacks.md          # Task 7 Paper
    └── 8-stdio_vs_streamable_http_mcp_transports.md # Task 8 Paper
```

---

## 👤 Author Information
* **Name:** Anil Pradhan
* **Team:** Team Ritu (`Team_Ritu`)
* **Branch:** `anil-pradhan`
