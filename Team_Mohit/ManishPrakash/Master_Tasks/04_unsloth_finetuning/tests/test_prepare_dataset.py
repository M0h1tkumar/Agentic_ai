"""Tests for the dataset preparation tool."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import prepare_dataset as pd  # noqa: E402


def record(instruction="What is quantisation?", output="Reducing numeric precision to save memory.", **extra):
    return {"instruction": instruction, "output": output, **extra}


# --------------------------------------------------------------------------
# field normalisation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("key", ["instruction", "question", "prompt", "query"])
def test_instruction_aliases_are_accepted(key: str) -> None:
    example, rejection = pd.validate({key: "Explain LoRA briefly", "output": "Low-rank adaptation."}, 0)
    assert rejection is None
    assert example.instruction == "Explain LoRA briefly"


@pytest.mark.parametrize("key", ["output", "answer", "response", "completion"])
def test_output_aliases_are_accepted(key: str) -> None:
    example, rejection = pd.validate({"instruction": "Explain LoRA briefly", key: "Low-rank adaptation."}, 0)
    assert rejection is None
    assert example.output == "Low-rank adaptation."


def test_context_is_captured_separately() -> None:
    example, _ = pd.validate(record(context="Some background text here."), 0)
    assert example.context == "Some background text here."


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------

def test_missing_instruction_is_rejected() -> None:
    _, rejection = pd.validate({"output": "An answer that is long enough."}, 3)
    assert rejection.reason == "missing instruction field"
    assert rejection.index == 3


def test_empty_response_is_rejected() -> None:
    _, rejection = pd.validate({"instruction": "A valid question here?", "output": "   "}, 0)
    assert rejection.reason == "missing or empty response"


@pytest.mark.parametrize(
    "response",
    [
        "As an AI language model, I cannot help with that.",
        "I'm sorry, but I can't assist with this request.",
        "N/A",
        "unknown",
        "TODO",
    ],
)
def test_refusals_are_rejected(response: str) -> None:
    _, rejection = pd.validate(record(output=response), 0)
    assert rejection is not None
    assert "refusal" in rejection.reason or "too short" in rejection.reason


def test_truncated_response_is_rejected() -> None:
    _, rejection = pd.validate(record(output="The first three reasons are these..."), 0)
    assert rejection.reason == "response looks truncated"


def test_echoed_instruction_is_rejected() -> None:
    text = "This is the same on both sides."
    _, rejection = pd.validate({"instruction": text, "output": text}, 0)
    assert rejection.reason == "response duplicates the instruction"


def test_oversized_example_is_rejected() -> None:
    _, rejection = pd.validate(record(output="x" * (pd.MAX_CHARS + 1)), 0)
    assert rejection.reason == "example exceeds length limit"


def test_non_object_record_is_rejected() -> None:
    _, rejection = pd.validate(["not", "an", "object"], 0)
    assert rejection.reason == "not an object"


def test_valid_record_survives() -> None:
    example, rejection = pd.validate(record(), 0)
    assert rejection is None
    assert example.instruction and example.output


# --------------------------------------------------------------------------
# deduplication
# --------------------------------------------------------------------------

def test_duplicate_prompts_are_removed() -> None:
    report = pd.prepare([
        record(output="First answer, long enough."),
        record(output="A different answer entirely."),
    ])
    assert len(report.accepted) == 1
    assert report.rejected[0].reason == "duplicate prompt"


def test_fingerprint_ignores_case_and_whitespace() -> None:
    a = pd.Example("What  is LoRA?", "answer one here")
    b = pd.Example("what is lora?", "answer two here")
    assert a.fingerprint == b.fingerprint


def test_different_prompts_are_kept() -> None:
    report = pd.prepare([
        record(instruction="What is LoRA adaptation?"),
        record(instruction="What is QLoRA adaptation?"),
    ])
    assert len(report.accepted) == 2


# --------------------------------------------------------------------------
# chat rendering
# --------------------------------------------------------------------------

def test_to_chat_produces_user_and_assistant_turns() -> None:
    messages = pd.Example("A question here?", "An answer here.").to_chat()["messages"]
    assert [m["role"] for m in messages] == ["user", "assistant"]
    assert messages[1]["content"] == "An answer here."


def test_to_chat_includes_system_prompt_when_given() -> None:
    messages = pd.Example("Q here?", "A here.").to_chat(system="You are terse.")["messages"]
    assert messages[0] == {"role": "system", "content": "You are terse."}


def test_to_chat_appends_context_to_the_user_turn() -> None:
    messages = pd.Example("Q here?", "A here.", context="Background.").to_chat()["messages"]
    assert messages[0]["content"] == "Q here?\n\nBackground."


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def test_load_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "d.jsonl"
    path.write_text('{"instruction":"a","output":"b"}\n\n{"instruction":"c","output":"d"}\n')
    assert len(pd.load_records(path)) == 2


def test_load_jsonl_reports_bad_line_number(tmp_path: Path) -> None:
    path = tmp_path / "d.jsonl"
    path.write_text('{"a":1}\n{bad}\n')
    with pytest.raises(ValueError, match=r":2:"):
        pd.load_records(path)


def test_load_json_list(tmp_path: Path) -> None:
    path = tmp_path / "d.json"
    path.write_text(json.dumps([record(), record(instruction="Another question here?")]))
    assert len(pd.load_records(path)) == 2


def test_load_json_wrapped_in_object(tmp_path: Path) -> None:
    path = tmp_path / "d.json"
    path.write_text(json.dumps({"data": [record()]}))
    assert len(pd.load_records(path)) == 1


def test_load_csv(tmp_path: Path) -> None:
    path = tmp_path / "d.csv"
    path.write_text("question,answer\nWhat is GGUF?,A single-file model format.\n")
    records = pd.load_records(path)
    assert records[0]["question"] == "What is GGUF?"


def test_load_rejects_unknown_extension(tmp_path: Path) -> None:
    path = tmp_path / "d.parquet"
    path.write_text("x")
    with pytest.raises(ValueError, match="unsupported extension"):
        pd.load_records(path)


# --------------------------------------------------------------------------
# split
# --------------------------------------------------------------------------

def test_split_is_deterministic() -> None:
    examples = [pd.Example(f"Question number {i}?", f"Answer number {i}.") for i in range(100)]
    first = pd.split(examples, 0.2, seed=7)
    second = pd.split(examples, 0.2, seed=7)
    assert [e.instruction for e in first[0]] == [e.instruction for e in second[0]]


def test_split_sizes_and_disjointness() -> None:
    examples = [pd.Example(f"Question number {i}?", f"Answer number {i}.") for i in range(100)]
    train, validation = pd.split(examples, 0.2)
    assert len(train) == 80
    assert len(validation) == 20
    assert not {e.instruction for e in train} & {e.instruction for e in validation}


def test_split_zero_fraction_keeps_everything() -> None:
    examples = [pd.Example("Question here?", "Answer here.")]
    train, validation = pd.split(examples, 0.0)
    assert len(train) == 1 and validation == []


def test_split_rejects_invalid_fraction() -> None:
    with pytest.raises(ValueError):
        pd.split([], 1.5)


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------

def test_statistics_are_computed() -> None:
    report = pd.prepare([record(instruction=f"Question number {i} here?") for i in range(20)])
    stats = report.statistics()
    assert stats["examples"] == 20
    assert stats["estimated_tokens_p95"] > 0


def test_warning_on_small_dataset() -> None:
    report = pd.prepare([record(instruction=f"Question number {i} here?") for i in range(5)])
    assert any("Only 5 examples" in w for w in report.warnings())


def test_warning_on_high_rejection_rate() -> None:
    records = [record(instruction=f"Question number {i} here?") for i in range(3)]
    records += [{"output": "orphan response text"} for _ in range(7)]
    assert any("rejected" in w for w in pd.prepare(records).warnings())


def test_warning_on_long_examples() -> None:
    long_answer = "word " * 3000
    report = pd.prepare([
        record(instruction=f"Question number {i} here?", output=long_answer) for i in range(10)
    ])
    assert any("tokens" in w for w in report.warnings())


def test_empty_dataset_warns_clearly() -> None:
    assert pd.prepare([]).warnings() == ["No examples survived validation."]


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def test_cli_writes_train_and_validation(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "raw.jsonl"
    source.write_text(
        "\n".join(
            json.dumps(record(instruction=f"Question number {i} here?"))
            for i in range(50)
        )
    )
    out = tmp_path / "data"
    assert pd.main([str(source), "-o", str(out), "--val-split", "0.2"]) == 0

    train = (out / "train.jsonl").read_text().strip().splitlines()
    validation = (out / "validation.jsonl").read_text().strip().splitlines()
    assert len(train) == 40
    assert len(validation) == 10
    assert json.loads(train[0])["messages"][0]["role"] == "user"


def test_cli_stats_only_writes_nothing(tmp_path: Path) -> None:
    source = tmp_path / "raw.jsonl"
    source.write_text(json.dumps(record()))
    out = tmp_path / "data"
    assert pd.main([str(source), "-o", str(out), "--stats-only"]) == 0
    assert not out.exists()


def test_cli_reports_rejections(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "raw.jsonl"
    source.write_text(json.dumps({"instruction": "A question here?", "output": "N/A"}))
    pd.main([str(source), "--stats-only"])
    assert "refusal" in capsys.readouterr().out


def test_cli_exits_nonzero_when_nothing_survives(tmp_path: Path) -> None:
    source = tmp_path / "raw.jsonl"
    source.write_text(json.dumps({"nothing": "useful"}))
    assert pd.main([str(source), "-o", str(tmp_path / "d")]) == 1


def test_cli_reports_unreadable_source(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert pd.main([str(tmp_path / "missing.jsonl")]) == 2


def test_cli_applies_system_prompt(tmp_path: Path) -> None:
    source = tmp_path / "raw.jsonl"
    source.write_text(json.dumps(record()))
    out = tmp_path / "data"
    pd.main([str(source), "-o", str(out), "--system", "You are a finance assistant."])
    first = json.loads((out / "train.jsonl").read_text().splitlines()[0])
    assert first["messages"][0]["role"] == "system"
