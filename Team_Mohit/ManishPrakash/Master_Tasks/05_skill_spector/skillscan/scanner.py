"""Static scanner for agent skills.

Walks a skill directory, reads every text file, and applies the rule set
line by line. Findings are correlated afterwards, because the interesting
signal in a malicious skill is rarely one line: it is a decode next to an
exec, or an environment sweep next to a POST.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from .rules import Family, Rule, Severity, rules_for

# Files worth reading. Anything else is recorded but not scanned.
TEXT_SUFFIXES = frozenset({
    ".md", ".txt", ".py", ".js", ".ts", ".mjs", ".cjs", ".sh", ".bash", ".zsh",
    ".fish", ".rb", ".pl", ".ps1", ".yaml", ".yml", ".json", ".toml", ".cfg",
    ".ini", ".env", ".rs", ".go", ".php", ".lua", "",
})

PROSE_SUFFIXES = frozenset({".md", ".txt", ".rst"})

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_LINE_LENGTH = 4000

# Combinations that are far more serious together than apart. Each entry maps
# a pair of families to the reason the pairing matters.
CORRELATIONS: tuple[tuple[Family, Family, str], str] = (  # type: ignore[assignment]
    (
        (Family.OBFUSCATION, Family.EXECUTION),
        "Encoded content is decoded and then executed. This is the standard "
        "shape of a hidden payload, and the encoding exists to defeat exactly "
        "the review you are doing now.",
    ),
    (
        (Family.CREDENTIALS, Family.EXFILTRATION),
        "The skill reads credentials and separately sends data to a remote "
        "host. Treat as credential theft until the code proves otherwise.",
    ),
    (
        (Family.CREDENTIALS, Family.NETWORK),
        "Credential access combined with network capability. Confirm the "
        "secrets never reach the request body.",
    ),
    (
        (Family.INJECTION, Family.EXECUTION),
        "Prompt-injection text alongside execution primitives: the description "
        "manipulates the agent, and the code gives it something to do.",
    ),
    (
        (Family.PERSISTENCE, Family.EXFILTRATION),
        "Persistence plus outbound network access is the shape of a durable "
        "implant rather than a one-off task.",
    ),
)


@dataclass(frozen=True)
class Finding:
    """One rule match at one location."""

    rule: Rule
    path: Path
    line_number: int
    line: str

    @property
    def excerpt(self) -> str:
        text = self.line.strip()
        return text if len(text) <= 160 else text[:157] + "..."


@dataclass
class Correlation:
    """Two families of finding that are more serious in combination."""

    families: tuple[Family, Family]
    explanation: str


@dataclass
class ScanResult:
    """Everything the scanner learned about one skill."""

    root: Path
    name: str = ""
    findings: list[Finding] = field(default_factory=list)
    correlations: list[Correlation] = field(default_factory=list)
    files_scanned: int = 0
    files_skipped: list[tuple[Path, str]] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def by_severity(self, severity: Severity) -> list[Finding]:
        return [f for f in self.findings if f.rule.severity is severity]

    def counts(self) -> Counter[str]:
        return Counter(f.rule.severity.value for f in self.findings)

    @property
    def highest(self) -> Severity:
        if not self.findings:
            return Severity.INFO
        return max((f.rule.severity for f in self.findings), key=lambda s: s.rank)

    @property
    def risk_score(self) -> int:
        """A 0-100 score for ranking skills against each other.

        Weighted by severity, with diminishing returns so that fifty medium
        findings never outrank one reverse shell. Correlations add a fixed
        premium because a pairing is qualitatively worse than its parts.
        """
        weights = {
            Severity.CRITICAL: 40,
            Severity.HIGH: 15,
            Severity.MEDIUM: 5,
            Severity.LOW: 1,
            Severity.INFO: 0,
        }
        counts = Counter(f.rule.severity for f in self.findings)
        total = 0.0
        for severity, weight in weights.items():
            n = counts.get(severity, 0)
            if n:
                # log growth: the second finding of a kind adds less than the first
                total += weight * (1 + math.log(n, 2))
        total += 10 * len(self.correlations)
        return min(100, int(round(total)))

    @property
    def verdict(self) -> str:
        """A short recommendation for a human reviewer."""
        if self.correlations or self.by_severity(Severity.CRITICAL):
            return "DO NOT INSTALL without line-by-line review"
        if self.by_severity(Severity.HIGH):
            return "REVIEW REQUIRED before installing"
        if self.by_severity(Severity.MEDIUM):
            return "REVIEW RECOMMENDED"
        return "NO BLOCKING FINDINGS"


def scan(root: Path) -> ScanResult:
    """Scan a skill directory or a single skill file."""
    result = ScanResult(root=root, name=root.stem if root.is_file() else root.name)

    if not root.exists():
        result.errors.append(f"path does not exist: {root}")
        return result

    paths = [root] if root.is_file() else sorted(p for p in root.rglob("*") if p.is_file())

    for path in paths:
        if any(part in {".git", "node_modules", "__pycache__", ".venv"} for part in path.parts):
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            result.files_skipped.append((path, f"binary or unhandled type {path.suffix}"))
            continue

        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                result.files_skipped.append((path, "larger than 2 MB"))
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            result.files_skipped.append((path, f"unreadable: {exc}"))
            continue

        result.files_scanned += 1
        result.findings.extend(_scan_text(path, text))

        if path.name.upper() in {"SKILL.MD", "AGENTS.MD", "SOUL.MD"}:
            result.metadata.update(parse_frontmatter(text))

    result.findings.sort(
        key=lambda f: (-f.rule.severity.rank, str(f.path), f.line_number)
    )
    result.correlations = correlate(result.findings)
    return result


_FENCE = re.compile(r"^\s*(```|~~~)")


def _scan_text(path: Path, text: str) -> list[Finding]:
    """Apply the rule set line by line.

    In a markdown file, prose and code are scanned with different rule sets.
    Code rules against narrative text produce constant false positives - a
    sentence containing the word "fetch" is not a network call - and prose
    rules against source code fire on ordinary comments. Splitting on fenced
    code blocks is what makes the report worth reading.
    """
    is_prose_file = path.suffix.lower() in PROSE_SUFFIXES
    code_rules = rules_for(False)
    prose_rules = tuple(r for r in rules_for(True) if r.prose_only)
    findings: list[Finding] = []
    in_fence = False

    # Narrative lines are collected into paragraphs and scanned separately.
    # An injection payload wrapped across two lines - "...ignore all previous\n
    # instructions..." - matches nothing when each line is tested alone, and
    # hard-wrapped markdown makes that the common case rather than the edge.
    paragraph: list[tuple[int, str]] = []

    for number, raw_line in enumerate(text.splitlines(), start=1):
        # A minified bundle on one line would otherwise dominate the report.
        line = raw_line[:MAX_LINE_LENGTH]

        if is_prose_file and _FENCE.match(line):
            in_fence = not in_fence
            findings.extend(_scan_paragraph(path, paragraph, prose_rules))
            paragraph = []
            continue

        if is_prose_file and not in_fence:
            if line.strip():
                paragraph.append((number, line))
            else:
                findings.extend(_scan_paragraph(path, paragraph, prose_rules))
                paragraph = []
            continue

        for rule in code_rules:
            if rule.search(line):
                findings.append(Finding(rule, path, number, line))

    findings.extend(_scan_paragraph(path, paragraph, prose_rules))
    return findings


def _scan_paragraph(
    path: Path, paragraph: list[tuple[int, str]], rules: tuple
) -> list[Finding]:
    """Run prose rules against a whole paragraph, joined into one string."""
    if not paragraph:
        return []
    joined = " ".join(line.strip() for _, line in paragraph)
    first_line = paragraph[0][0]
    return [
        Finding(rule, path, first_line, joined)
        for rule in rules
        if rule.search(joined)
    ]


def correlate(findings: list[Finding]) -> list[Correlation]:
    """Flag family pairings that are worse together than apart."""
    present = {f.rule.family for f in findings}
    return [
        Correlation(families=pair, explanation=explanation)
        for pair, explanation in CORRELATIONS
        if pair[0] in present and pair[1] in present
    ]


_FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract simple `key: value` YAML frontmatter.

    Deliberately not a YAML parser. A skill file is untrusted input, and
    pulling in a full YAML loader to read a manifest is a larger attack
    surface than the four fields we actually want.
    """
    match = _FRONTMATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith(" "):
            continue
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def scan_many(roots: list[Path]) -> list[ScanResult]:
    """Scan several skills, highest risk first."""
    results = [scan(root) for root in roots]
    results.sort(key=lambda r: -r.risk_score)
    return results
