"""Rendering scan results as text, JSON, or a markdown report."""

from __future__ import annotations

import json
from collections import defaultdict

from .rules import Severity
from .scanner import ScanResult

SEVERITY_ORDER = (
    Severity.CRITICAL,
    Severity.HIGH,
    Severity.MEDIUM,
    Severity.LOW,
    Severity.INFO,
)


def render_text(result: ScanResult, *, verbose: bool = False) -> str:
    """Terminal report. Grouped by severity so the worst is read first."""
    out: list[str] = []
    out.append(f"Skill:    {result.name}")
    out.append(f"Path:     {result.root}")
    if result.metadata.get("description"):
        out.append(f"Declared: {result.metadata['description'][:100]}")
    out.append(f"Files:    {result.files_scanned} scanned, {len(result.files_skipped)} skipped")
    out.append(f"Risk:     {result.risk_score}/100")
    out.append(f"Verdict:  {result.verdict}")

    for error in result.errors:
        out.append(f"Error:    {error}")

    if not result.findings:
        out.append("")
        out.append("No rule matched. Note that a clean static scan is not proof of")
        out.append("safety; it means these patterns were absent.")
        return "\n".join(out)

    counts = result.counts()
    summary = "  ".join(
        f"{sev.value}={counts.get(sev.value, 0)}"
        for sev in SEVERITY_ORDER
        if counts.get(sev.value)
    )
    out.append(f"Findings: {len(result.findings)}  ({summary})")

    grouped: dict[Severity, list] = defaultdict(list)
    for finding in result.findings:
        grouped[finding.rule.severity].append(finding)

    for severity in SEVERITY_ORDER:
        items = grouped.get(severity)
        if not items:
            continue
        if severity is Severity.LOW and not verbose:
            out.append("")
            out.append(f"[{severity.value}] {len(items)} finding(s), use --verbose to list")
            continue

        out.append("")
        out.append(f"[{severity.value.upper()}]")
        for finding in items:
            rule = finding.rule
            location = f"{finding.path}:{finding.line_number}"
            out.append(f"  {rule.id}  {rule.name}")
            out.append(f"      {location}")
            out.append(f"      > {finding.excerpt}")
            out.append(f"      Why: {rule.rationale}")

    if result.correlations:
        out.append("")
        out.append("[CORRELATED PATTERNS]")
        for correlation in result.correlations:
            pair = " + ".join(f.value for f in correlation.families)
            out.append(f"  {pair}")
            out.append(f"      {correlation.explanation}")

    return "\n".join(out)


def render_json(result: ScanResult) -> str:
    """Machine-readable output for CI."""
    payload = {
        "skill": result.name,
        "path": str(result.root),
        "risk_score": result.risk_score,
        "verdict": result.verdict,
        "highest_severity": result.highest.value,
        "files_scanned": result.files_scanned,
        "metadata": result.metadata,
        "counts": dict(result.counts()),
        "findings": [
            {
                "rule_id": f.rule.id,
                "rule": f.rule.name,
                "family": f.rule.family.value,
                "severity": f.rule.severity.value,
                "file": str(f.path),
                "line": f.line_number,
                "excerpt": f.excerpt,
                "rationale": f.rule.rationale,
            }
            for f in result.findings
        ],
        "correlations": [
            {
                "families": [fam.value for fam in c.families],
                "explanation": c.explanation,
            }
            for c in result.correlations
        ],
        "errors": result.errors,
    }
    return json.dumps(payload, indent=2)


def render_markdown(results: list[ScanResult]) -> str:
    """A committable audit report for one or more skills."""
    out: list[str] = ["# Skill security audit", ""]

    out.append("| Skill | Risk | Highest | Findings | Verdict |")
    out.append("|---|---|---|---|---|")
    for result in results:
        out.append(
            f"| {result.name} | {result.risk_score}/100 | {result.highest.value} "
            f"| {len(result.findings)} | {result.verdict} |"
        )
    out.append("")

    for result in results:
        out.append(f"## {result.name}")
        out.append("")
        out.append(f"- Path: `{result.root}`")
        out.append(f"- Files scanned: {result.files_scanned}")
        out.append(f"- Risk score: {result.risk_score}/100")
        out.append(f"- Verdict: **{result.verdict}**")
        out.append("")

        if not result.findings:
            out.append("No rule matched.")
            out.append("")
            continue

        out.append("| Severity | Rule | Location | Excerpt |")
        out.append("|---|---|---|---|")
        for finding in result.findings:
            excerpt = finding.excerpt.replace("|", "\\|").replace("`", "'")
            out.append(
                f"| {finding.rule.severity.value} | {finding.rule.id} "
                f"{finding.rule.name} | `{finding.path.name}:{finding.line_number}` "
                f"| `{excerpt[:80]}` |"
            )
        out.append("")

        if result.correlations:
            out.append("### Correlated patterns")
            out.append("")
            for correlation in result.correlations:
                pair = " + ".join(f.value for f in correlation.families)
                out.append(f"- **{pair}** — {correlation.explanation}")
            out.append("")

    out.append("---")
    out.append("")
    out.append(
        "Static analysis only. A clean result means these patterns were absent, "
        "not that the skill is safe. Obfuscated or novel techniques will not "
        "match a regex, and behaviour that only appears at runtime is invisible "
        "to this tool."
    )
    return "\n".join(out)
