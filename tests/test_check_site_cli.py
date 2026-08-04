import base64
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
ONE_PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class CheckSiteCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        self.report = self.site / "report.json"

    def run_cli(self, root=None):
        return subprocess.run(
            [
                sys.executable,
                "scripts/check-site.py",
                "--root",
                str(root or self.site),
                "--json-out",
                str(self.report),
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_broken_fixture_writes_json_and_exits_one(self):
        (self.site / "index.html").write_text(
            '<img src="missing.jpg" alt="Missing">', encoding="utf-8"
        )

        result = self.run_cli()

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["pages_checked"], 1)
        self.assertEqual(payload["summary"]["broken"], 1)
        self.assertEqual(payload["findings"][0]["code"], "missing-local-file")

    def test_clean_fixture_exits_zero(self):
        photo = self.site / "photo.png"
        photo.write_bytes(ONE_PIXEL_PNG)
        (self.site / "index.html").write_text(
            '<img src="photo.png" alt="Portrait">', encoding="utf-8"
        )

        result = self.run_cli()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertTrue(payload["ok"])
        self.assertEqual(
            payload["summary"],
            {"broken": 0, "degraded": 0, "unverifiable": 0},
        )

    def test_missing_root_exits_two_without_writing_report(self):
        result = self.run_cli(self.site / "missing")

        self.assertEqual(result.returncode, 2)
        self.assertIn("portfolio root is not a directory", result.stderr)
        self.assertFalse(self.report.exists())


if __name__ == "__main__":
    unittest.main()
