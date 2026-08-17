"""Command-line interface.

    docmd convert  --input docs --output out
    docmd ingest   --input docs --output out --workspace research
    docmd check
    docmd workspaces
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .anythingllm import AnythingLLMClient, AnythingLLMError
from .config import Config, ConfigError
from .converters import ConversionError, ENGINES
from .pipeline import RunReport, report_as_json, run

EXIT_OK = 0
EXIT_FAILURES = 1
EXIT_CONFIG = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docmd",
        description="Convert documents to markdown and ingest them into AnythingLLM.",
    )
    parser.add_argument("--version", action="version", version="docmd 1.0.0")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("-i", "--input", type=Path, help="input file or directory")
        p.add_argument("-o", "--output", type=Path, help="output directory for markdown")
        p.add_argument(
            "-e", "--engine",
            choices=["auto", *(c.name for c in ENGINES)],
            help="conversion engine (default: auto)",
        )
        p.add_argument("--no-recursive", action="store_true", help="do not descend into subdirectories")
        p.add_argument("--overwrite", action="store_true", help="reconvert files even if unchanged")
        p.add_argument("--json", action="store_true", help="emit a JSON report instead of text")

    convert = sub.add_parser("convert", help="convert documents to markdown locally")
    add_common(convert)
    convert.add_argument("--dry-run", action="store_true", help="show what would be converted")

    ingest = sub.add_parser("ingest", help="convert, then upload and embed into AnythingLLM")
    add_common(ingest)
    ingest.add_argument("-w", "--workspace", help="AnythingLLM workspace slug")

    sub.add_parser("check", help="verify AnythingLLM connectivity and credentials")
    sub.add_parser("workspaces", help="list AnythingLLM workspaces")
    sub.add_parser("engines", help="show which conversion engines are installed")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "engines":
        return _cmd_engines()

    try:
        config = _config_from_args(args)
    except ConfigError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return EXIT_CONFIG

    try:
        if args.command == "check":
            return _cmd_check(config)
        if args.command == "workspaces":
            return _cmd_workspaces(config)
        if args.command in {"convert", "ingest"}:
            return _cmd_run(config, args)
    except (AnythingLLMError, ConversionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FAILURES
    except ConfigError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return EXIT_CONFIG
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        return EXIT_FAILURES

    return EXIT_OK  # pragma: no cover - argparse requires a subcommand


def _config_from_args(args: argparse.Namespace) -> Config:
    overrides: dict[str, object] = {}
    if getattr(args, "input", None) is not None:
        overrides["input_dir"] = args.input
    if getattr(args, "output", None) is not None:
        overrides["output_dir"] = args.output
    if getattr(args, "engine", None) is not None:
        overrides["engine"] = args.engine
    if getattr(args, "workspace", None) is not None:
        overrides["workspace"] = args.workspace
    if getattr(args, "no_recursive", False):
        overrides["recursive"] = False
    if getattr(args, "overwrite", False):
        overrides["overwrite"] = True
    return Config.from_env(**overrides)


def _cmd_engines() -> int:
    print("Conversion engines:")
    for cls in ENGINES:
        engine = cls()
        state = "available" if engine.available() else "not installed"
        print(f"  {engine.name:<12} {state}")
    return EXIT_OK


def _cmd_check(config: Config) -> int:
    config.require_upload()
    client = AnythingLLMClient(config.base_url, config.api_key)
    client.verify()
    print(f"connected to {config.base_url}")
    if client.workspace_exists(config.workspace):
        print(f"workspace '{config.workspace}' found")
        return EXIT_OK
    print(f"workspace '{config.workspace}' not found", file=sys.stderr)
    return EXIT_FAILURES


def _cmd_workspaces(config: Config) -> int:
    if not config.base_url or not config.api_key:
        raise ConfigError("ANYTHINGLLM_BASE_URL and ANYTHINGLLM_API_KEY are required")
    client = AnythingLLMClient(config.base_url, config.api_key)
    workspaces = client.workspaces()
    if not workspaces:
        print("no workspaces found")
        return EXIT_OK
    for workspace in workspaces:
        name = workspace.get("name", "")
        slug = workspace.get("slug", "")
        print(f"  {slug:<24} {name}")
    return EXIT_OK


def _cmd_run(config: Config, args: argparse.Namespace) -> int:
    if not config.input_dir.exists():
        raise ConfigError(f"input path does not exist: {config.input_dir}")

    report = run(
        config,
        upload=(args.command == "ingest"),
        dry_run=getattr(args, "dry_run", False),
    )

    if args.json:
        print(report_as_json(report))
    else:
        _print_report(report)

    return EXIT_FAILURES if report.failures else EXIT_OK


def _print_report(report: RunReport) -> None:
    for entry in report.results:
        if entry.status == "converted":
            print(f"  ok       {entry.source} -> {entry.output} ({entry.words} words)")
        elif entry.status == "unchanged":
            print(f"  cached   {entry.source}")
        elif entry.status == "skipped":
            print(f"  skip     {entry.source}  ({entry.detail})")
        elif entry.status == "empty":
            print(f"  empty    {entry.source}  ({entry.detail})")
        else:
            print(f"  FAILED   {entry.source}  ({entry.detail})", file=sys.stderr)
    print()
    print(report.summary())


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
