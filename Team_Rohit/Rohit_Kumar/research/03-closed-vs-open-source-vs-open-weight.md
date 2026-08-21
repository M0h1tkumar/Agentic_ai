# Difference Between Closed, Open Source, and Open Weight Models

## Introduction

AI models are distributed in different ways depending on how much of their technology is made available to users.

The three commonly discussed categories are:

- Closed Models
- Open Source Models
- Open Weight Models

These terms are related but they do not mean the same thing.

---

## Comparison

| Feature | Closed Model | Open Source Model | Open Weight Model |
|----------|--------------|-------------------|-------------------|
| Source Code | Usually No | Yes | Sometimes |
| Model Weights | No | Yes | Yes |
| Training Data | Usually No | More information should be available | Usually No |
| Modification | Restricted | Yes | Usually Yes |
| Self Hosting | Usually No | Yes | Yes |
| Commercial Usage | Provider dependent | Depends on license | Depends on license |
| Transparency | Low | High | Medium |
| Vendor Dependency | High | Low | Lower |

> **Important:** Open Weight does not automatically mean Open Source.

According to the Open Source Initiative (OSI), an Open Source AI system must provide users with the freedoms to **use, study, modify, and share** the system, along with the information and components required to exercise those freedoms. :contentReference[oaicite:5]{index=5}

---

## Closed Models

### Definition

A closed model is an AI model whose internal model weights and important implementation details are not publicly available.

Users normally access these models through:

- Web applications
- APIs
- Enterprise platforms

### Examples

- GPT-5.5
- Claude
- Gemini

GPT-5.5 is an example of a proprietary model offered by OpenAI. :contentReference[oaicite:6]{index=6}

### Advantages

- High performance
- Professionally maintained
- Easy to use
- No need to manage model infrastructure
- Regular improvements from the provider

### Disadvantages

- Limited transparency
- Usually cannot inspect model weights
- Limited customization
- Vendor dependency
- API or subscription costs may apply

---

## Open Source Models

### Definition

An Open Source AI model provides users with the necessary freedoms to use, study, modify, and share the system.

The Open Source Initiative's definition is stricter than simply publishing model weights. It requires access to the preferred form needed to modify the AI system, including relevant data information and code. :contentReference[oaicite:7]{index=7}

### Examples

- OLMo
- OLMo 2
- OLMo 3

Ai2 describes OLMo as a fully open language model family and provides access to models, data, training code, evaluations, and other parts of the model development process. :contentReference[oaicite:8]{index=8}

### Advantages

- High transparency
- Can be studied and modified
- Strong research value
- Community participation
- Less vendor lock-in
- More control over deployment

### Disadvantages

- Requires technical knowledge
- Users may need significant computing resources
- Deployment and maintenance become the user's responsibility
- License compliance is still required

---

## Open Weight Models

### Definition

An open weight model provides its trained model weights to users.

This allows users to:

- Download the model
- Run it locally
- Fine-tune it
- Quantize it
- Deploy it on their own infrastructure

However, the source code, training data, training process, or other components may not be fully available.

Therefore:

> **Open Weight ≠ Open Source**

### Examples

- Llama
- Some Mistral models
- Gemma

For example, Meta's Llama 2 makes trained weights available, but its Community License contains additional conditions. Therefore, availability of the weights alone does not make it equivalent to an OSI-defined Open Source AI system. :contentReference[oaicite:9]{index=9}

Mistral also publishes models under different licenses, so the exact model and license should always be checked. :contentReference[oaicite:10]{index=10}

### Advantages

- Can run locally
- Fine-tuning is possible
- More control over deployment
- Lower dependency on hosted APIs
- Can reduce inference cost

### Disadvantages

- Training data may not be available
- Source code may not be fully available
- License restrictions may apply
- Requires suitable hardware for larger models

---

## Key Difference

The easiest way to understand the difference is:

```text
Closed Model
     |
     |-- Model weights unavailable
     |-- Source code unavailable
     |-- Provider controls the model
     |
     v
Open Weight Model
     |
     |-- Model weights available
     |-- Other components may remain closed
     |-- License may contain restrictions
     |
     v
Open Source AI
     |
     |-- Use
     |-- Study
     |-- Modify
     |-- Share
     |-- Required information/components available