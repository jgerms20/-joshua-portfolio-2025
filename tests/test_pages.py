from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from portfolio_quality.model import Finding, HealthReport
from portfolio_quality.pages import discover_production_pages


class PageDiscoveryTests(unittest.TestCase):
    def test_discovers_only_production_pages_in_stable_order(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in [
                "index.html",
                "index-gemini-ultra.html",
                "work/work-alpha.html",
                "work/work-template.html",
                "podcasts/podcast-show.html",
                "media/media-books.html",
                "archives/old.html",
                "concepts/concept.html",
                "versions/milestones/v1/index.html",
            ]:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("<html></html>", encoding="utf-8")

            pages = discover_production_pages(root)

            self.assertEqual(
                [page.relative_to(root).as_posix() for page in pages],
                [
                    "index.html",
                    "media/media-books.html",
                    "podcasts/podcast-show.html",
                    "work/work-alpha.html",
                ],
            )

    def test_report_exits_nonzero_only_for_broken_findings(self):
        warning = Finding(
            "degraded",
            "external-rate-limit",
            "index.html",
            "https://example.com",
            "rate limited",
        )
        broken = Finding(
            "broken",
            "missing-local-file",
            "index.html",
            "photos/missing.jpg",
            "not found",
        )

        self.assertEqual(HealthReport([warning]).exit_code(), 0)
        self.assertEqual(HealthReport([warning, broken]).exit_code(), 1)
        self.assertEqual(
            HealthReport([warning, broken]).to_dict(),
            {
                "ok": False,
                "findings": [
                    {
                        "severity": "degraded",
                        "code": "external-rate-limit",
                        "page": "index.html",
                        "target": "https://example.com",
                        "message": "rate limited",
                    },
                    {
                        "severity": "broken",
                        "code": "missing-local-file",
                        "page": "index.html",
                        "target": "photos/missing.jpg",
                        "message": "not found",
                    },
                ],
            },
        )


if __name__ == "__main__":
    unittest.main()
