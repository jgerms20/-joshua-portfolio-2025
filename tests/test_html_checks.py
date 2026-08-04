import base64
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from portfolio_quality.html_checks import check_page


ONE_PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class HtmlCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.page = self.root / "index.html"

    def check_html_fixture(self, html):
        self.page.write_text(html, encoding="utf-8")
        return check_page(self.root, self.page)

    def test_reports_blank_missing_and_inaccessible_media(self):
        html = """
        <html><body>
          <img src="" alt="Broken">
          <img src="photos/missing.jpg">
          <iframe src="https://example.com/player"></iframe>
          <div id="same"></div><div id="same"></div>
          <a href="#absent">Jump</a>
          <p>Video Coming Soon</p>
        </body></html>
        """

        findings = self.check_html_fixture(html)

        self.assertEqual(
            {finding.code for finding in findings},
            {
                "blank-source",
                "missing-local-file",
                "missing-alt",
                "missing-iframe-title",
                "duplicate-id",
                "missing-fragment",
                "placeholder-media",
            },
        )

    def test_accepts_existing_local_media_and_external_links(self):
        photo = self.root / "photos/working.png"
        photo.parent.mkdir(parents=True, exist_ok=True)
        photo.write_bytes(ONE_PIXEL_PNG)

        findings = self.check_html_fixture(
            '<img src="photos/working.png" alt="Portrait">'
            '<a href="https://example.com">Source</a>'
        )

        self.assertEqual(findings, [])

    def test_reports_an_image_that_cannot_be_decoded(self):
        photo = self.root / "photos/broken.jpg"
        photo.parent.mkdir(parents=True, exist_ok=True)
        photo.write_text("not an image", encoding="utf-8")

        findings = self.check_html_fixture(
            '<img src="photos/broken.jpg" alt="Broken image">'
        )

        self.assertEqual([finding.code for finding in findings], ["unreadable-image"])


if __name__ == "__main__":
    unittest.main()
