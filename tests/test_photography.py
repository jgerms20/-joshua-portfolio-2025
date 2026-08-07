import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from portfolio_quality.photography import import_photography_inbox, load_photography_manifest, render_darkroom


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/photography.json"


class PhotographyManifestTests(unittest.TestCase):
    def test_manifest_has_valid_unique_published_photos(self):
        photos = load_photography_manifest(MANIFEST)
        ids = [photo["id"] for photo in photos]
        sources = [photo["src"] for photo in photos]

        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(sources), len(set(sources)))
        self.assertTrue(all(photo["chapter"] in {"people", "places", "gatherings"} for photo in photos))
        self.assertTrue(all(photo["alt"].strip() for photo in photos))
        self.assertTrue(all((ROOT / photo["src"]).is_file() for photo in photos))

    def test_selected_sequence_is_contiguous_and_curated(self):
        photos = load_photography_manifest(MANIFEST)
        selected = sorted(
            (photo for photo in photos if photo.get("sequence") is not None),
            key=lambda photo: photo["sequence"],
        )

        self.assertGreaterEqual(len(selected), 18)
        self.assertLessEqual(len(selected), 24)
        self.assertEqual(
            [photo["sequence"] for photo in selected],
            list(range(1, len(selected) + 1)),
        )
        self.assertEqual(selected[0]["layout"], "hero")

    def test_renderer_outputs_story_and_three_accessible_chapters(self):
        markup = render_darkroom(load_photography_manifest(MANIFEST))

        self.assertIn('class="photo-sequence rv"', markup)
        self.assertIn('data-chapter="people"', markup)
        self.assertIn('data-chapter="places"', markup)
        self.assertIn('data-chapter="gatherings"', markup)
        self.assertIn('aria-pressed="true"', markup)
        self.assertIn("Selected sequence", markup)
        self.assertNotIn("photo-masonry", markup)

    def test_homepage_contains_rendered_darkroom_markers(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")

        self.assertIn("<!-- PHOTOGRAPHY:START -->", page)
        self.assertIn("<!-- PHOTOGRAPHY:END -->", page)
        self.assertIn('class="photo-sequence rv"', page)

    def test_inbox_import_creates_an_unpublished_metadata_stripped_webp_once(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            inbox = root / "photos/inbox"
            inbox.mkdir(parents=True)
            manifest_path = root / "data/photography.json"
            manifest_path.parent.mkdir(parents=True)
            manifest_path.write_text('{"version": 1, "entries": []}', encoding="utf-8")
            source = inbox / "New Portrait.JPG"
            image = Image.new("RGB", (32, 48), "red")
            image.save(source, exif=b"Exif\x00\x00test-metadata")

            first = import_photography_inbox(root)
            second = import_photography_inbox(root)

            self.assertEqual(len(first), 1)
            self.assertEqual(second, [])
            generated = root / first[0]["src"]
            self.assertTrue(generated.is_file())
            with Image.open(generated) as imported:
                self.assertEqual(imported.format, "WEBP")
                self.assertEqual(dict(imported.getexif()), {})
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["entries"]), 1)
            self.assertFalse(payload["entries"][0]["published"])
            self.assertEqual(payload["entries"][0]["chapter"], "unassigned")
            self.assertEqual(payload["entries"][0]["alt"], "")


if __name__ == "__main__":
    unittest.main()
