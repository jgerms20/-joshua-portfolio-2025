from pathlib import Path
import unittest

from portfolio_quality.html_checks import check_page
from portfolio_quality.pages import discover_production_pages


ROOT = Path(__file__).resolve().parents[1]


class ProductionHealthTests(unittest.TestCase):
    def test_production_pages_have_no_static_findings(self):
        findings = [
            finding
            for page in discover_production_pages(ROOT)
            for finding in check_page(ROOT, page)
        ]

        self.assertEqual(
            [
                (item.severity, item.page, item.code, item.target)
                for item in findings
            ],
            [],
        )


if __name__ == "__main__":
    unittest.main()
