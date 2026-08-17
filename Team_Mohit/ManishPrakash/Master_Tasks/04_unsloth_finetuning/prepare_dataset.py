#!/usr/bin/env python3
"""Dataset preparation and validation for instruction fine-tuning.

Written first, and deliberately so. Tool choice is the least important
decision in a fine-tune; dataset quality dominates everything. A thousand
clean, correctly formatted examples beat a hundred thousand noisy ones, and
most failed fine-tunes are failed datasets wearing a training script.

What this does:

  - reads instruction data from JSON, JSONL, or CSV
  - validates every record and explains each rejection
  - strips records that would teach the model the wrong thing: empty
    responses, duplicated prompts, refusals, truncation artifacts
  - renders to a chat template ready for Unsloth/TRL
  - splits train/validation deterministically
  - reports statistics that predict training problems before you pay for them

Usage:
    python3 prepare_dataset.py raw.jsonl -o data/
    python3 prepare_dataset.py raw.csv -o data/ --val-split 0.1
    python3 prepare_dataset.py raw.jsonl --stats-only
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# Field names accepted for each role, in priority order. Public instruction
# datasets are inconsistent about this and normalising once here is cheaper
# than special-casing it in every downstream script.
INSTRUCTION_KEYS = ("instruction", "question", "prompt", "input_text", "query")
INPUT_KEYS = ("input", "context", "passage")
OUTPUT_KEYS = ("output", "answer", "response", "completion", "target")

MIN_INSTRUCTION_CHARS = 8
MIN_OUTPUT_CHARS = 8
MAX_CHARS = 24_000

# Responses that teach the model to decline rather than to answer. A dataset
# scraped from a chat log is full of these and they are actively harmful:
# training on them produces a model that refuses.
REFUSAL_PATTERNS = re.compile(
    r"^\s*(as an ai|i'?m sorry,? (but )?i (can'?t|cannot)|i (can'?t|cannot) (help|assist)"
    r"|i do not have (access|the ability)|n/?a|none|unknown|todo)\b",
    re.IGNORECASE,
)

# Text that got cut off mid-generation. Training on truncated targets teaches
# the model to stop early.
TRUNCATION_PATTERNS = re.compile(r"(\.\.\.|…)\s*$|\b(etc\.?|and so on)\s*$", re.IGNORECASE)


@dataclass
class Example:
    """One validated training example."""

    instruction: str
    output: str
    context: str = ""

    @property
    def fingerprint(self) -> str:
        """Hash of the normalised prompt, used for deduplication.

        Prompt-only rather than prompt+response: two different answers to the
        same question is a contradiction in the training signal, not two
        useful examples.
        """
        key = " ".join((self.instruction + " " + self.context).lower().split())
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    def to_chat(self, system: str = "") -> dict[str, list[dict[str, str]]]:
        """Render to the messages format Unsloth and TRL expect."""
        user = self.instruction
        if self.context:
            user = f"{self.instruction}\n\n{self.context}"
        messages = [{"role": "system", "content": system}] if system else []
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": self.output})
        return {"messages": messages}


@dataclass
class Rejection:
    """A record that did not survive validation, and why."""

    index: int
    reason: str
    excerpt: str = ""


@dataclass
class Report:
    """Outcome of preparing a dataset."""

    accepted: list[Example] = field(default_factory=list)
    rejected: list[Rejection] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.accepted) + len(self.rejected)

    def reasons(self) -> Counter[str]:
        return Counter(r.reason for r in self.rejected)

    def statistics(self) -> dict[str, float | int]:
        """Length statistics, in characters.

        Character counts rather than tokens: a real token count needs the
        target model's tokeniser, which is a heavy dependency for a
        preprocessing step. Characters divided by roughly four is a close
        enough estimate to choose a sequence length.
        """
        if not self.accepted:
            return {}
        prompts = [len(e.instruction) + len(e.context) for e in self.accepted]
        outputs = [len(e.output) for e in self.accepted]
        combined = [p + o for p, o in zip(prompts, outputs)]
        return {
            "examples": len(self.accepted),
            "prompt_chars_mean": round(statistics.mean(prompts), 1),
            "prompt_chars_p95": _percentile(prompts, 95),
            "output_chars_mean": round(statistics.mean(outputs), 1),
            "output_chars_p95": _percentile(outputs, 95),
            "combined_chars_max": max(combined),
            "estimated_tokens_p95": _percentile(combined, 95) // 4,
        }

    def warnings(self) -> list[str]:
        """Problems that will surface during or after training."""
        out: list[str] = []
        stats = self.statistics()
        if not stats:
            return ["No examples survived validation."]

        count = int(stats["examples"])
        if count < 100:
            out.append(
                f"Only {count} examples. LoRA can work from a few hundred, but "
                "below ~100 expect the adapter to memorise rather than generalise."
            )
        if self.total and len(self.rejected) / self.total > 0.3:
            out.append(
                f"{len(self.rejected)}/{self.total} records rejected "
                f"({len(self.rejected) / self.total:.0%}). Inspect the source data "
                "before training; this rate usually means a format mismatch."
            )
        if stats["estimated_tokens_p95"] > 2048:
            out.append(
                f"95th-percentile length is ~{int(stats['estimated_tokens_p95'])} "
                "tokens. Set max_seq_length above that or long examples will be "
                "silently truncated mid-answer."
            )
        outputs = [len(e.output) for e in self.accepted]
        if outputs and statistics.mean(outputs) < 40:
            out.append(
                "Mean response length is very short. The model will learn to "
                "answer tersely, which may not be what you want."
            )
        return out


def _percentile(values: list[int], pct: int) -> int:
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * pct / 100))
    return ordered[index]


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def load_records(path: Path) -> list[dict]:
    """Read raw records from JSON, JSONL, or CSV."""
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8", errors="replace")

    if suffix == ".jsonl":
        records = []
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{number}: invalid JSON: {exc}") from exc
        return records

    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            for key in ("data", "examples", "records", "train"):
                if isinstance(data.get(key), list):
                    return data[key]
            raise ValueError(f"{path}: JSON object has no recognisable list field")
        if not isinstance(data, list):
            raise ValueError(f"{path}: expected a list of records")
        return data

    if suffix == ".csv":
        return list(csv.DictReader(text.splitlines()))

    raise ValueError(f"{path}: unsupported extension {suffix} (use .json, .jsonl, or .csv)")


def _first_present(record: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def validate(record: dict, index: int) -> tuple[Example | None, Rejection | None]:
    """Turn one raw record into an Example, or explain why it cannot be."""
    if not isinstance(record, dict):
        return None, Rejection(index, "not an object")

    instruction = _first_present(record, INSTRUCTION_KEYS)
    output = _first_present(record, OUTPUT_KEYS)
    context = _first_present(record, INPUT_KEYS)

    if not instruction:
        return None, Rejection(index, "missing instruction field")
    if not output:
        return None, Rejection(index, "missing or empty response", instruction[:60])
    # Refusals are checked before length. Placeholders like "N/A" are short
    # enough to trip the length rule first, and "response too short" sends a
    # reviewer looking for a formatting bug instead of the real problem,
    # which is that the source data is full of non-answers.
    if REFUSAL_PATTERNS.match(output):
        return None, Rejection(index, "response is a refusal or placeholder", output[:60])
    if len(instruction) < MIN_INSTRUCTION_CHARS:
        return None, Rejection(index, "instruction too short", instruction)
    if len(output) < MIN_OUTPUT_CHARS:
        return None, Rejection(index, "response too short", output)
    if len(instruction) + len(context) + len(output) > MAX_CHARS:
        return None, Rejection(index, "example exceeds length limit", instruction[:60])
    if TRUNCATION_PATTERNS.search(output):
        return None, Rejection(index, "response looks truncated", output[-60:])
    if instruction.strip() == output.strip():
        return None, Rejection(index, "response duplicates the instruction", instruction[:60])

    return Example(instruction=instruction, output=output, context=context), None


def prepare(records: list[dict]) -> Report:
    """Validate and deduplicate a list of raw records."""
    report = Report()
    seen: set[str] = set()

    for index, record in enumerate(records):
        example, rejection = validate(record, index)
        if rejection is not None:
            report.rejected.append(rejection)
            continue
        assert example is not None
        if example.fingerprint in seen:
            report.rejected.append(
                Rejection(index, "duplicate prompt", example.instruction[:60])
            )
            continue
        seen.add(example.fingerprint)
        report.accepted.append(example)

    return report


def split(examples: list[Example], val_fraction: float, seed: int = 42) -> tuple[list[Example], list[Example]]:
    """Deterministic train/validation split.

    Seeded so that two runs produce the same split. Without that, a
    validation score is not comparable between runs and the whole point of
    holding data out is lost.
    """
    if not 0 <= val_fraction < 1:
        raise ValueError("val_fraction must be in [0, 1)")
    shuffled = list(examples)
    random.Random(seed).shuffle(shuffled)
    cut = int(len(shuffled) * val_fraction)
    return shuffled[cut:], shuffled[:cut]


def write_jsonl(examples: list[Example], path: Path, system: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for example in examples:
            handle.write(json.dumps(example.to_chat(system), ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and format an instruction dataset for fine-tuning."
    )
    parser.add_argument("source", type=Path, help="raw dataset (.json, .jsonl, .csv)")
    parser.add_argument("-o", "--output", type=Path, default=Path("data"), help="output directory")
    parser.add_argument("--val-split", type=float, default=0.05, help="validation fraction (default 0.05)")
    parser.add_argument("--system", default="", help="system prompt to prepend to every example")
    parser.add_argument("--seed", type=int, default=42, help="split seed (default 42)")
    parser.add_argument("--stats-only", action="store_true", help="report without writing files")
    parser.add_argument("--show-rejections", type=int, default=5, help="how many rejections to print")
    args = parser.parse_args(argv)

    try:
        records = load_records(args.source)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    report = prepare(records)

    print(f"Source:   {args.source}  ({report.total} records)")
    print(f"Accepted: {len(report.accepted)}")
    print(f"Rejected: {len(report.rejected)}")

    if report.rejected:
        print("\nRejections by reason:")
        for reason, count in report.reasons().most_common():
            print(f"  {count:>5}  {reason}")
        if args.show_rejections:
            print(f"\nFirst {args.show_rejections} rejected records:")
            for rejection in report.rejected[: args.show_rejections]:
                excerpt = f"  > {rejection.excerpt}" if rejection.excerpt else ""
                print(f"  [{rejection.index}] {rejection.reason}{excerpt}")

    stats = report.statistics()
    if stats:
        print("\nStatistics:")
        for key, value in stats.items():
            print(f"  {key:<24} {value}")

    for warning in report.warnings():
        print(f"\nWarning: {warning}")

    if not report.accepted:
        print("\nNothing to write.", file=sys.stderr)
        return 1

    if args.stats_only:
        return 0

    train, validation = split(report.accepted, args.val_split, args.seed)
    write_jsonl(train, args.output / "train.jsonl", args.system)
    print(f"\nWrote {len(train)} examples to {args.output / 'train.jsonl'}")
    if validation:
        write_jsonl(validation, args.output / "validation.jsonl", args.system)
        print(f"Wrote {len(validation)} examples to {args.output / 'validation.jsonl'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
