"""skillscan - static security scanner for agent skills."""

from .report import render_json, render_markdown, render_text
from .rules import RULES, Family, Rule, Severity
from .scanner import Finding, ScanResult, parse_frontmatter, scan, scan_many

__version__ = "1.0.0"

__all__ = [
    "RULES",
    "Family",
    "Finding",
    "Rule",
    "ScanResult",
    "Severity",
    "parse_frontmatter",
    "render_json",
    "render_markdown",
    "render_text",
    "scan",
    "scan_many",
]
