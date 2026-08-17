# Model

This directory contains information about the fine-tuned model.

The model was fine-tuned using:

- Base Model: Qwen2.5-7B-Instruct
- Dataset: BANKING77
- Method: LoRA / QLoRA
- Training: Unsloth
- GPU: Google Colab Tesla T4
- Epochs: 2
- Evaluation Accuracy: 91.67%

The trained LoRA adapter is currently stored in Google Drive.

## Adapter

The fine-tuned LoRA adapter was trained in Google Colab
and saved separately from the base Qwen model.

The local machine does not currently contain the 7B base model
or adapter weights.

They will be connected during the inference setup.
