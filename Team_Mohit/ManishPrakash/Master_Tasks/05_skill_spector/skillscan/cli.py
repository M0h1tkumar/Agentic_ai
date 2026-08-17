"""Command-line interface for skillscan.

    skillscan samples/weather-lookup
    skillscan samples/* --format markdown --output audit.md
    skillscan skills/ --fail-on high
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .rules import RULES, Severity
from .report import render_json, render_markdown, render_text
from .scanner import scan_many

EXIT_CLEAN = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2

_THRESHOLDS = {
    "critical": Severity.CRITICAL,
    "high": Severity.HIGH,
    "medium": Severity.MEDIUM,
    "low": Severity.LOW,
    "never": None,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillscan",
        description=(
            "Static security scanner for agent skills. Audits SKILL.md files and "
            "accompanying scripts for execution, credential, exfiltration, "
            "persistence, obfuscation, and prompt-injection patterns."
        ),
    )
    parser.add_argument("paths", nargs="*", type=Path, help="skill directories or files")
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="output format (default: text)",
    )
    parser.add_argument("-o", "--output", type=Path, help="write the report to a file")
    parser.add_argument("-v", "--verbose", action="store_true", help="include low-severity findings")
    parser.add_argument(
        "--fail-on",
        choices=list(_THRESHOLDS),
        default="high",
        help="exit non-zero at this severity or above (default: high)",
    )
    parser.add_argument("--list-rules", action="store_true", help="print the rule set and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_rules:
        return _list_rules()

    if not args.paths:
        print("error: no paths given (use --list-rules to inspect the rule set)", file=sys.stderr)
        return EXIT_ERROR

    missing = [p for p in args.paths if not p.exists()]
    if missing:
        for path in missing:
            print(f"error: path does not exist: {path}", file=sys.stderr)
        return EXIT_ERROR

    results = scan_many(args.paths)

    if args.format == "json":
        text = (
            render_json(results[0])
            if len(results) == 1
            else "[\n" + ",\n".join(render_json(r) for r in results) + "\n]"
        )
    elif args.format == "markdown":
        text = render_markdown(results)
    else:
        text = "\n\n".join(render_text(r, verbose=args.verbose) for r in results)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"report written to {args.output}")
    else:
        print(text)

    threshold = _THRESHOLDS[args.fail_on]
    if threshold is None:
        return EXIT_CLEAN
    triggered = any(r.highest.rank >= threshold.rank for r in results)
    return EXIT_FINDINGS if triggered else EXIT_CLEAN


def _list_rules() -> int:
    print(f"{len(RULES)} rules\n")
    current = ""
    for rule in sorted(RULES, key=lambda r: (r.family.value, r.id)):
        if rule.family.value != current:
            current = rule.family.value
            print(f"\n{current.upper()}")
        scope = " (prose only)" if rule.prose_only else ""
        print(f"  {rule.id}  [{rule.severity.value:<8}] {rule.name}{scope}")
    return EXIT_CLEAN


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
