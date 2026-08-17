# 🧠 SupportSense

### Fine-Tuning Qwen2.5-7B for Banking Customer Intent Classification

SupportSense is an end-to-end LLM fine-tuning project that adapts **Qwen2.5-7B-Instruct** to classify banking customer-support queries into predefined intents using **BANKING77**, **Unsloth**, and **LoRA/QLoRA**.

---

## 🎯 Objective

The goal is to teach an open-source LLM to convert natural-language banking queries into a specific support intent.

Example:

**Input**
> I am still waiting on my card.

**Output**
```text
card_arrival
```

Instead of generating a general conversational response, the fine-tuned model learns to return the relevant intent.

---

## 🏗️ Training Pipeline

```text
BANKING77 Dataset
        ↓
Data Preparation
        ↓
Chat / Instruction Format
        ↓
Qwen2.5-7B-Instruct
        ↓
4-bit Quantization
        ↓
LoRA / QLoRA
        ↓
Supervised Fine-Tuning
        ↓
Unseen Test Evaluation
        ↓
91.67% Accuracy
```

---

## 🤖 Model

- **Base Model:** Qwen2.5-7B-Instruct
- **Fine-Tuning Method:** LoRA / QLoRA
- **Framework:** Unsloth
- **Hardware:** Google Colab Tesla T4

---

## 📊 Training Configuration

| Configuration | Value |
|---|---|
| Training examples | 1,000 |
| Test examples | 300 |
| Epochs | 2 |
| Total parameters | 7.65B |
| Trainable parameters | 40.37M |
| Trainable percentage | 0.53% |
| Effective batch size | 8 |

---

## 📈 Results

The fine-tuned model achieved:
- **91.67% Accuracy**
- Correct predictions: 275 / 300
- Incorrect predictions: 25 / 300

The model was evaluated on unseen test examples.

---

## 🔍 Error Analysis

The main model weaknesses were semantic overlaps between closely related intents.

Examples:
```text
card_arrival
       ↕
card_delivery_estimate
```
and:
```text
exchange_rate
       ↕
card_payment_wrong_exchange_rate
```

This analysis helped identify areas for future dataset improvement.

---

## 🧪 Base Model vs Fine-Tuned Model

### Before Fine-Tuning
The base Qwen model behaved as a general conversational assistant.

### After Fine-Tuning
**User:**
> I am still waiting on my card. What should I do?

**Model:**
```text
card_arrival
```

The fine-tuning successfully shifted the model toward the desired intent-classification behavior.

---

## 📂 Project Structure

```text
SupportSense-FineTuning/
│
├── notebooks/
│   └── SupportSense_FineTuning.ipynb
│
├── dataset/
│   └── README.md
│
├── evaluation/
│   └── README.md
│
├── model/
│   └── README.md
│
├── outputs/
│   └── README.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🚀 Run in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1gnxySfuJ-Qsq8TwKf5uIAKoYR_WZ7lPn?usp=sharing)


The complete training workflow is available in:
[`notebooks/SupportSense_FineTuning.ipynb`](notebooks/SupportSense_FineTuning.ipynb)

The notebook can be opened and executed using Google Colab.
Training was performed on a free Tesla T4 Google Colab environment.

---

## 🧠 What I Learned

- Dataset preparation for LLM fine-tuning
- Conversational training formats
- Qwen chat templates
- 4-bit quantization
- LoRA / QLoRA
- Parameter-efficient fine-tuning
- Supervised Fine-Tuning (SFT)
- Training and validation loss analysis
- Model inference
- Unseen-test evaluation
- Error analysis
- Saving and reloading LoRA adapters

---

## 📌 Project Status

- Fine-tuning: ✅ Complete
- Evaluation: ✅ Complete
- Error Analysis: ✅ Complete
- Adapter Save/Reload: ✅ Verified
- Documentation: 🚧 In Progress
