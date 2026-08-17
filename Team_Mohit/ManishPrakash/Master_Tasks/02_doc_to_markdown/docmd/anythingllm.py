"""Minimal AnythingLLM REST client.

Only the four calls this pipeline needs. Written against `urllib` so the
package has no hard HTTP dependency; if `requests` is installed it is not
used, deliberately, to keep one code path.

Endpoints used:
    GET  /api/v1/auth                                  credential check
    GET  /api/v1/workspaces                            list workspaces
    POST /api/v1/document/raw-text                     upload markdown
    POST /api/v1/workspace/{slug}/update-embeddings    embed into a workspace
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_TIMEOUT = 60


class AnythingLLMError(RuntimeError):
    """Raised when the AnythingLLM API rejects a request or is unreachable."""


@dataclass
class UploadResult:
    """Outcome of uploading one document."""

    title: str
    location: str
    embedded: bool = False


class AnythingLLMClient:
    """Thin synchronous client.

    The API key is a static bearer token. It is read from configuration and
    never logged; `__repr__` is overridden so it cannot leak into a
    traceback or a debug print.
    """

    def __init__(self, base_url: str, api_key: str, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        if not base_url:
            raise AnythingLLMError("base_url is required")
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self.timeout = timeout

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"AnythingLLMClient(base_url={self.base_url!r}, api_key=<redacted>)"

    # -- transport ---------------------------------------------------------

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(url, data=data, method=method)
        request.add_header("Authorization", f"Bearer {self._api_key}")
        request.add_header("Accept", "application/json")
        if data is not None:
            request.add_header("Content-Type", "application/json")

        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:400]
            raise AnythingLLMError(
                f"{method} {path} returned HTTP {exc.code}: {detail}"
            ) from exc
        except URLError as exc:
            raise AnythingLLMError(
                f"cannot reach AnythingLLM at {self.base_url}: {exc.reason}"
            ) from exc

        if not body.strip():
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise AnythingLLMError(f"{method} {path} returned non-JSON body") from exc

    # -- API ---------------------------------------------------------------

    def verify(self) -> bool:
        """Check that the base URL and API key work. Cheap preflight."""
        self._request("GET", "/api/v1/auth")
        return True

    def workspaces(self) -> list[dict[str, Any]]:
        """List workspaces available to this key."""
        data = self._request("GET", "/api/v1/workspaces")
        return data.get("workspaces", []) if isinstance(data, dict) else []

    def workspace_exists(self, slug: str) -> bool:
        return any(w.get("slug") == slug for w in self.workspaces())

    def upload_markdown(self, title: str, body: str, *, source: str = "") -> UploadResult:
        """Upload markdown as a raw-text document.

        Raw text is used rather than file upload because the document has
        already been converted. Sending the original file would make
        AnythingLLM re-parse it with its own extractor, discarding the
        conversion and the provenance frontmatter attached to it.
        """
        payload = {
            "textContent": body,
            "metadata": {
                "title": title,
                "docSource": source or title,
                "description": f"Converted to markdown by docmd from {source or title}",
            },
        }
        data = self._request("POST", "/api/v1/document/raw-text", payload)
        location = _extract_location(data)
        if not location:
            raise AnythingLLMError(f"upload of {title!r} returned no document location")
        return UploadResult(title=title, location=location)

    def embed(self, workspace: str, locations: list[str]) -> None:
        """Attach uploaded documents to a workspace and embed them.

        Upload and embed are separate operations in AnythingLLM: a document
        can exist in storage without belonging to any workspace, in which
        case it is never retrieved. Forgetting this second call is the most
        common reason ingestion "works" but search finds nothing.
        """
        if not locations:
            return
        self._request(
            "POST",
            f"/api/v1/workspace/{workspace}/update-embeddings",
            {"adds": locations, "deletes": []},
        )


def _extract_location(payload: Any) -> str:
    """Pull the document location out of an upload response.

    The response shape has varied across AnythingLLM versions, so this
    checks the known variants rather than assuming one.
    """
    if not isinstance(payload, dict):
        return ""
    documents = payload.get("documents")
    if isinstance(documents, list) and documents:
        first = documents[0]
        if isinstance(first, dict):
            return first.get("location") or first.get("name") or ""
    document = payload.get("document")
    if isinstance(document, dict):
        return document.get("location") or document.get("name") or ""
    return payload.get("location", "") or ""
