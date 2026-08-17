"""docmd - convert documents to markdown and ingest them into AnythingLLM."""

from .config import Config, ConfigError
from .converters import ConversionError, select_engine
from .markdown import Document, normalise
from .pipeline import RunReport, run
from .triage import Action, Verdict, slugify, triage

__version__ = "1.0.0"

__all__ = [
    "Action",
    "Config",
    "ConfigError",
    "ConversionError",
    "Document",
    "RunReport",
    "Verdict",
    "normalise",
    "run",
    "select_engine",
    "slugify",
    "triage",
]
