#!/usr/bin/env python3
"""LoRA fine-tuning with Unsloth.

Runs on a single consumer GPU or a free Colab T4. Reads the chat-formatted
JSONL produced by `prepare_dataset.py`, trains a LoRA adapter, evaluates it
against held-out examples, and optionally exports to GGUF for Ollama.

    python3 train.py --data data/ --model unsloth/Qwen2.5-7B-Instruct-bnb-4bit
    python3 train.py --data data/ --export-gguf Q4_K_M

Requires a CUDA GPU. Install inside Colab or a GPU environment:

    pip install unsloth trl peft accelerate bitsandbytes datasets

This script is written to run in Colab; it is not runnable on a CPU-only
machine, and it will say so clearly rather than failing deep inside a
library call.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Defaults chosen for a 16 GB T4. Every one of them is a memory/quality
# trade-off, explained where it is used.
DEFAULTS = {
    "model": "unsloth/Qwen2.5-7B-Instruct-bnb-4bit",
    "max_seq_length": 2048,
    "lora_r": 16,
    "lora_alpha": 16,
    "lora_dropout": 0.0,
    "batch_size": 2,
    "grad_accum": 4,
    "epochs": 2,
    "learning_rate": 2e-4,
    "warmup_ratio": 0.03,
    "seed": 42,
}

# The modules LoRA adapts. Attention plus MLP projections is the standard
# choice: adapting attention alone trains fewer parameters but consistently
# underperforms on instruction following.
TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]


def check_environment() -> None:
    """Fail early and legibly if this cannot possibly work."""
    try:
        import torch
    except ImportError:
        sys.exit("torch is not installed. Run this in a GPU environment: pip install unsloth")

    if not torch.cuda.is_available():
        sys.exit(
            "No CUDA GPU detected. Unsloth requires one.\n"
            "Use Google Colab (Runtime > Change runtime type > T4 GPU) or a machine with an NVIDIA card."
        )

    name = torch.cuda.get_device_name(0)
    total = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"GPU: {name} ({total:.1f} GB)")
    if total < 14:
        print(
            "Warning: under 14 GB of VRAM. Reduce --max-seq-length or use a "
            "smaller base model if training runs out of memory."
        )


def load_datasets(data_dir: Path):
    """Load the JSONL written by prepare_dataset.py."""
    from datasets import load_dataset

    train_path = data_dir / "train.jsonl"
    if not train_path.exists():
        sys.exit(f"{train_path} not found. Run prepare_dataset.py first.")

    files = {"train": str(train_path)}
    val_path = data_dir / "validation.jsonl"
    if val_path.exists():
        files["validation"] = str(val_path)

    dataset = load_dataset("json", data_files=files)
    print(f"Loaded {len(dataset['train'])} training examples")
    if "validation" in dataset:
        print(f"Loaded {len(dataset['validation'])} validation examples")
    return dataset


def build_model(args):
    """Load a 4-bit base model and attach LoRA adapters."""
    from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.model,
        max_seq_length=args.max_seq_length,
        # 4-bit quantised base weights. This is the single change that makes
        # a 7B model trainable on a 16 GB card at all.
        load_in_4bit=True,
        dtype=None,  # let Unsloth pick bf16 or fp16 for the hardware
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=args.lora_r,
        target_modules=TARGET_MODULES,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        # Trades a little compute for a large memory saving; without it the
        # activations for a 2048-token sequence do not fit alongside the model.
        use_gradient_checkpointing="unsloth",
        random_state=args.seed,
    )

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable parameters: {trainable:,} of {total:,} ({100 * trainable / total:.2f}%)")
    return model, tokenizer


def format_dataset(dataset, tokenizer):
    """Apply the model's chat template to the messages field.

    Using the tokeniser's own template rather than a hand-written prompt
    format matters: a mismatch between training and inference formatting is
    the most common cause of a fine-tune that trains cleanly and then
    behaves badly when actually used.
    """
    def apply(batch):
        return {
            "text": [
                tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
                for messages in batch["messages"]
            ]
        }

    return dataset.map(apply, batched=True, remove_columns=["messages"])


def train(args) -> Path:
    from transformers import TrainingArguments
    from trl import SFTTrainer

    check_environment()
    dataset = load_datasets(args.data)
    model, tokenizer = build_model(args)
    dataset = format_dataset(dataset, tokenizer)

    output_dir = args.output / "checkpoints"
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset["train"],
        eval_dataset=dataset.get("validation"),
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
        packing=False,  # packing corrupts short instruction examples
        args=TrainingArguments(
            output_dir=str(output_dir),
            per_device_train_batch_size=args.batch_size,
            # Effective batch size is batch_size * grad_accum. Accumulating
            # gradients gives a larger effective batch without the memory
            # cost of actually holding one.
            gradient_accumulation_steps=args.grad_accum,
            num_train_epochs=args.epochs,
            learning_rate=args.learning_rate,
            warmup_ratio=args.warmup_ratio,
            lr_scheduler_type="cosine",
            optim="adamw_8bit",  # 8-bit optimiser states, another large saving
            weight_decay=0.01,
            logging_steps=10,
            eval_strategy="epoch" if "validation" in dataset else "no",
            save_strategy="epoch",
            save_total_limit=2,
            seed=args.seed,
            report_to="none",
        ),
    )

    print(f"\nEffective batch size: {args.batch_size * args.grad_accum}")
    stats = trainer.train()

    adapter_dir = args.output / "adapter"
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))

    metrics = {
        "train_runtime_seconds": round(stats.metrics.get("train_runtime", 0), 1),
        "train_loss": round(stats.metrics.get("train_loss", 0), 4),
        "epochs": args.epochs,
        "base_model": args.model,
        "lora_r": args.lora_r,
    }
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"\nAdapter saved to {adapter_dir}")
    print(f"Metrics: {metrics}")
    return adapter_dir


def sample_generation(model, tokenizer, prompt: str) -> str:
    """Generate one response, to eyeball the result before exporting."""
    from unsloth import FastLanguageModel

    FastLanguageModel.for_inference(model)
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt"
    ).to("cuda")
    outputs = model.generate(input_ids=inputs, max_new_tokens=256, temperature=0.7, do_sample=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def export_gguf(model, tokenizer, output: Path, quantisation: str) -> None:
    """Export a merged GGUF for Ollama or LM Studio.

    Closes the loop: train, quantise, and run locally without a separate
    conversion step. Q4_K_M is the default for the reasons set out in
    ../../GitHub_Tasks/06_model_formats_and_gguf.md.
    """
    target = output / "gguf"
    print(f"\nExporting GGUF ({quantisation}) to {target}")
    model.save_pretrained_gguf(str(target), tokenizer, quantization_method=quantisation.lower())
    print("Run it with Ollama:")
    print(f"  ollama create my-model -f {target}/Modelfile")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="LoRA fine-tune with Unsloth.")
    parser.add_argument("--data", type=Path, default=Path("data"), help="directory holding train.jsonl")
    parser.add_argument("--output", type=Path, default=Path("runs/latest"), help="output directory")
    parser.add_argument("--model", default=DEFAULTS["model"], help="base model")
    parser.add_argument("--max-seq-length", type=int, default=DEFAULTS["max_seq_length"])
    parser.add_argument("--lora-r", type=int, default=DEFAULTS["lora_r"])
    parser.add_argument("--lora-alpha", type=int, default=DEFAULTS["lora_alpha"])
    parser.add_argument("--lora-dropout", type=float, default=DEFAULTS["lora_dropout"])
    parser.add_argument("--batch-size", type=int, default=DEFAULTS["batch_size"])
    parser.add_argument("--grad-accum", type=int, default=DEFAULTS["grad_accum"])
    parser.add_argument("--epochs", type=int, default=DEFAULTS["epochs"])
    parser.add_argument("--learning-rate", type=float, default=DEFAULTS["learning_rate"])
    parser.add_argument("--warmup-ratio", type=float, default=DEFAULTS["warmup_ratio"])
    parser.add_argument("--seed", type=int, default=DEFAULTS["seed"])
    parser.add_argument("--export-gguf", metavar="QUANT", help="export GGUF, e.g. Q4_K_M")
    parser.add_argument("--test-prompt", help="generate one sample after training")
    args = parser.parse_args(argv)

    args.output.mkdir(parents=True, exist_ok=True)
    train(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
