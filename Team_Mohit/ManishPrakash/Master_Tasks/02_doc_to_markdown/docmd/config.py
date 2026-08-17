"""Configuration, loaded from the environment with sane defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Extensions we are willing to attempt. Anything else is skipped by triage.
SUPPORTED_EXTENSIONS: frozenset[str] = frozenset({
    ".pdf",
    ".docx", ".doc",
    ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv",
    ".html", ".htm",
    ".txt", ".md", ".rst",
    ".epub",
    ".json", ".xml",
})

# Extensions that are already markdown-ish and need no conversion engine.
PASSTHROUGH_EXTENSIONS: frozenset[str] = frozenset({".md", ".txt", ".rst"})


class ConfigError(ValueError):
    """Raised when configuration is missing or self-contradictory."""


@dataclass(frozen=True)
class Config:
    """Runtime configuration for a pipeline run.

    Every field has a default so that `Config()` is valid for local
    conversion. Only the AnythingLLM fields are required for upload, and
    they are validated lazily by `require_upload()` rather than at
    construction, so that `docmd convert` works with no credentials at all.
    """

    input_dir: Path = Path("input")
    output_dir: Path = Path("output")

    # Conversion engine: "auto" tries markitdown, then docling, then the
    # built-in plain-text fallback.
    engine: str = "auto"

    # AnythingLLM
    base_url: str = ""
    api_key: str = ""
    workspace: str = ""

    # Behaviour
    recursive: bool = True
    overwrite: bool = False
    max_bytes: int = 50 * 1024 * 1024
    skip_extensions: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def from_env(cls, **overrides: object) -> "Config":
        """Build a Config from environment variables, then apply overrides.

        Overrides whose value is None are ignored, so a CLI can pass its
        parsed arguments straight through without stripping unset flags.
        """
        env = os.environ
        base = cls(
            input_dir=Path(env.get("DOCMD_INPUT_DIR", "input")),
            output_dir=Path(env.get("DOCMD_OUTPUT_DIR", "output")),
            engine=env.get("DOCMD_ENGINE", "auto"),
            base_url=env.get("ANYTHINGLLM_BASE_URL", "").rstrip("/"),
            api_key=env.get("ANYTHINGLLM_API_KEY", ""),
            workspace=env.get("ANYTHINGLLM_WORKSPACE", ""),
            recursive=_env_bool(env, "DOCMD_RECURSIVE", True),
            overwrite=_env_bool(env, "DOCMD_OVERWRITE", False),
            max_bytes=int(env.get("DOCMD_MAX_BYTES", 50 * 1024 * 1024)),
        )
        clean = {k: v for k, v in overrides.items() if v is not None}
        return base.replace(**clean) if clean else base

    def replace(self, **changes: object) -> "Config":
        """Return a copy with the given fields changed."""
        from dataclasses import replace as _replace

        return _replace(self, **changes)  # type: ignore[arg-type]

    def require_upload(self) -> None:
        """Validate the fields needed to talk to AnythingLLM.

        Called only on the upload path so that offline conversion never
        demands credentials.
        """
        missing = [
            name
            for name, value in (
                ("ANYTHINGLLM_BASE_URL", self.base_url),
                ("ANYTHINGLLM_API_KEY", self.api_key),
                ("ANYTHINGLLM_WORKSPACE", self.workspace),
            )
            if not value
        ]
        if missing:
            raise ConfigError(
                "Upload requires these settings: " + ", ".join(missing)
            )


def _env_bool(env: object, key: str, default: bool) -> bool:
    raw = env.get(key)  # type: ignore[attr-defined]
    if raw is None:
        return default
    return str(raw).strip().lower() in {"1", "true", "yes", "on"}
