import json
from pathlib import Path
from typing import Callable, Protocol
from urllib.parse import urlencode

import requests

from portfolio_quality.model import Finding


REQUIRED_MEDIA_FIELDS = {
    "id",
    "page",
    "kind",
    "url",
    "fallback",
    "critical",
    "last_verified",
    "evidence_url",
}


class ResponseLike(Protocol):
    status_code: int


Fetch = Callable[..., ResponseLike]


def load_media_manifest(path: Path) -> list[dict[str, object]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("version") != 1 or not isinstance(payload.get("entries"), list):
        raise ValueError("media manifest must contain version 1 and an entries list")

    entries = payload["entries"]
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("media entry must be an object")
        missing = REQUIRED_MEDIA_FIELDS.difference(entry)
        if missing:
            raise ValueError(f"media entry missing fields: {', '.join(sorted(missing))}")
        identifier = str(entry["id"])
        if identifier in seen:
            raise ValueError(f"duplicate media id: {identifier}")
        seen.add(identifier)
    return entries


def _probe_url(entry: dict[str, object]) -> str:
    url = str(entry["url"])
    if entry["kind"] == "youtube":
        return "https://www.youtube.com/oembed?" + urlencode(
            {"url": url, "format": "json"}
        )
    return url


def _fetch_status(url: str, fetch: Fetch) -> int | None:
    for attempt in range(2):
        try:
            response = fetch(url, timeout=10, allow_redirects=True)
        except requests.RequestException:
            if attempt == 0:
                continue
            return None
        if response.status_code >= 500 and attempt == 0:
            continue
        return response.status_code
    return None


def _fallback_exists(root: Path, entry: dict[str, object]) -> bool:
    fallback = str(entry.get("fallback", "")).strip()
    return bool(fallback and (root / fallback).is_file())


def _status_code(status: int | None) -> str:
    if status is None:
        return "external-request-failed"
    if status == 404:
        return "external-not-found"
    if status == 429:
        return "external-rate-limit"
    if status >= 500:
        return "external-server-error"
    return "external-http-error"


def probe_manifest(
    root: Path,
    entries: list[dict[str, object]],
    fetch: Fetch = requests.get,
) -> list[Finding]:
    root = Path(root)
    findings: list[Finding] = []
    for entry in entries:
        target = _probe_url(entry)
        status = _fetch_status(target, fetch)
        if status is not None and 200 <= status < 400:
            continue

        if status is None or status in {408, 425, 429} or status >= 500:
            severity = "unverifiable"
        elif _fallback_exists(root, entry) or not bool(entry["critical"]):
            severity = "degraded"
        else:
            severity = "broken"

        findings.append(
            Finding(
                severity=severity,
                code=_status_code(status),
                page=str(entry["page"]),
                target=str(entry["url"]),
                message=(
                    "request failed after one retry"
                    if status is None
                    else f"external source returned HTTP {status}"
                ),
            )
        )
    return findings
