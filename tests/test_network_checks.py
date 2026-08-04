from dataclasses import dataclass
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from portfolio_quality.network_checks import load_media_manifest, probe_manifest


@dataclass
class FakeResponse:
    status_code: int


class FakeFetch:
    def __init__(self, statuses):
        self.statuses = statuses
        self.urls = []

    def __call__(self, url, **_kwargs):
        self.urls.append(url)
        status = self.statuses[url]
        if isinstance(status, list):
            status = status.pop(0)
        return FakeResponse(status)


def media_entry(**overrides):
    entry = {
        "id": "hero",
        "page": "index.html",
        "kind": "image",
        "url": "https://cdn.example/hero.jpg",
        "fallback": "",
        "critical": True,
        "last_verified": "2026-08-04",
        "evidence_url": "",
    }
    entry.update(overrides)
    return entry


class NetworkCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_critical_404_without_fallback_is_broken(self):
        entry = media_entry()

        findings = probe_manifest(
            self.root,
            [entry],
            fetch=FakeFetch({entry["url"]: 404}),
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "broken")
        self.assertEqual(findings[0].code, "external-not-found")

    def test_not_found_with_working_fallback_is_degraded(self):
        fallback = self.root / "brand/sample/poster.jpg"
        fallback.parent.mkdir(parents=True)
        fallback.write_bytes(b"poster")
        entry = media_entry(fallback="brand/sample/poster.jpg")

        findings = probe_manifest(
            self.root,
            [entry],
            fetch=FakeFetch({entry["url"]: 404}),
        )

        self.assertEqual(findings[0].severity, "degraded")

    def test_rate_limit_is_unverifiable_even_with_fallback(self):
        fallback = self.root / "brand/sample/poster.jpg"
        fallback.parent.mkdir(parents=True)
        fallback.write_bytes(b"poster")
        entry = media_entry(
            id="video",
            page="work/work-sample.html",
            kind="youtube",
            url="https://www.youtube.com/watch?v=abc",
            fallback="brand/sample/poster.jpg",
        )
        endpoint = (
            "https://www.youtube.com/oembed?"
            "url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dabc&format=json"
        )
        fetch = FakeFetch({endpoint: 429})

        findings = probe_manifest(self.root, [entry], fetch=fetch)

        self.assertEqual(findings[0].severity, "unverifiable")
        self.assertEqual(fetch.urls, [endpoint])

    def test_award_evidence_forbidden_to_automated_client_is_unverifiable(self):
        entry = media_entry(
            id="award",
            page="work/work-gatorade.html",
            kind="award-evidence",
            url="https://clios.com/winners-gallery/details/220718",
        )

        findings = probe_manifest(
            self.root,
            [entry],
            fetch=FakeFetch({entry["url"]: 403}),
        )

        self.assertEqual(findings[0].severity, "unverifiable")
        self.assertEqual(findings[0].code, "external-access-denied")

    def test_successful_probe_returns_no_findings(self):
        entry = media_entry()

        findings = probe_manifest(
            self.root,
            [entry],
            fetch=FakeFetch({entry["url"]: 200}),
        )

        self.assertEqual(findings, [])

    def test_server_error_retries_once_before_succeeding(self):
        entry = media_entry()
        fetch = FakeFetch({entry["url"]: [503, 200]})

        findings = probe_manifest(self.root, [entry], fetch=fetch)

        self.assertEqual(findings, [])
        self.assertEqual(fetch.urls, [entry["url"], entry["url"]])

    def test_manifest_loader_rejects_duplicate_ids(self):
        manifest = self.root / "media.json"
        entry = media_entry()
        manifest.write_text(
            json.dumps({"version": 1, "entries": [entry, entry]}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "duplicate media id: hero"):
            load_media_manifest(manifest)

    def test_manifest_loader_rejects_missing_required_fields(self):
        manifest = self.root / "media.json"
        entry = media_entry()
        del entry["evidence_url"]
        manifest.write_text(
            json.dumps({"version": 1, "entries": [entry]}),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "media entry missing fields: evidence_url"):
            load_media_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
