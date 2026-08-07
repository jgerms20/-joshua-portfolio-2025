# Portfolio Media Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Clear the reliability foundation's current production failures by fixing deferred-image markup, iframe labels, DIRECTV and Xfinity video playback, and verified Gatorade award evidence without redesigning any page.

**Architecture:** Production-page integration tests turn the current health report into a regression gate. Existing page components are edited in place. Owned video is converted to browser-compatible MP4, external video records use verified canonical URLs and fallbacks, and award copy links to official evidence.

**Tech Stack:** Static HTML/CSS, Python 3.11 `unittest`, FFmpeg, YouTube/iSpot embeds, JSON media manifest.

## Global Constraints

- Preserve the current site design, typography, page order, and navigation.
- Do not add unsupported campaign results, awards, or credits.
- Every iframe has a descriptive title and every deferred image omits a blank `src` attribute.
- A dead player is replaced by owned media or an honest, working external fallback.
- The Gatorade Clio Bronze links to `https://clios.com/winners-gallery/details/220718`.
- No deployment, merge, or public publication occurs in this phase.

---

### Task 1: Production Static-Health Regression Gate

**Files:**
- Create: `tests/test_production_health.py`

**Interfaces:**
- Consumes: `discover_production_pages()` and `check_page()`.
- Produces: one integration test that fails with the exact production findings until the page repairs are complete.

- [x] **Step 1: Write the failing integration test**

```python
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
            [(item.severity, item.page, item.code, item.target) for item in findings],
            [],
        )
```

- [x] **Step 2: Run the test and verify the current five findings**

Run: `../.venv-portfolio-quality/bin/python -m unittest tests.test_production_health -v`

Expected: FAIL listing two broken findings and three degraded iframe-title findings.

- [x] **Step 3: Commit the failing regression gate with the subsequent page fixes in Task 2**

No test-only commit is made because `main` currently contains known visitor-facing defects. The test remains red until Task 2's minimal repairs are applied.

---

### Task 2: Deferred Image, Iframe Labels, and DIRECTV Fallback

**Files:**
- Modify: `index.html`
- Modify: `media/media-podcasts.html`
- Modify: `podcasts/podcast-dominate.html`
- Modify: `podcasts/podcast-eclectic-polymath.html`
- Modify: `work/work-directv.html`
- Create: `brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4`
- Modify: `data/media-manifest.json`
- Test: `tests/test_production_health.py`

**Interfaces:**
- The lightbox image has no `src` until existing JavaScript assigns it.
- Spotify iframe titles are `Spotify playlist: Joshua German's rotation`, `Spotify show: Dominate The Decade`, and `Spotify show: The Eclectic Polymath Podcast`.
- DIRECTV's broken Emmys iframe uses the owned MP4 with native controls and a fallback link.
- The separate "Nothing On Your Roof 2.0" placeholder becomes an honest campaign still rather than reusing unrelated footage.

- [x] **Step 1: Convert the owned DIRECTV MOV without re-encoding**

Run:

```bash
ffmpeg -y -i "brand/directv/ooh-hijack/DIRECTV Emmy's OOH Hijack.MOV" \
  -map 0:v:0 -map 0:a:0 -c copy -movflags +faststart \
  brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4
```

Expected: FFprobe reports H.264 video, AAC audio, 720×1280 dimensions, and a duration near 56.4 seconds.

- [x] **Step 2: Apply the minimal HTML repairs**

Remove `src=""` from `#lightboxImg`. Add the three exact iframe titles. Replace the broken DIRECTV Emmys iframe with:

```html
<video controls playsinline preload="metadata" aria-label="DIRECTV Emmys OOH Hijack campaign video">
    <source src="../brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4" type="video/mp4">
    <a href="../brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4">Watch the DIRECTV campaign video</a>
</video>
```

Add `.film-frame video` to the existing absolute-fill rule used by `.film-frame iframe`.
Replace the unrelated "Video Coming Soon" block with a local DIRECTV campaign still and a caption that identifies it as a still.

- [x] **Step 3: Update the DIRECTV manifest record**

Change `directv-emmys-youtube` to `directv-emmys-owned-video`, set `kind` to `local-video`, set `url` and `fallback` to `brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4`, and retain the page and verification date.

- [x] **Step 4: Run the production regression test**

Run: `../.venv-portfolio-quality/bin/python -m unittest tests.test_production_health -v`

Expected: PASS with no static findings.

- [x] **Step 5: Verify the generated media file**

Run: `ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,codec_type,width,height -of json brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4`

Expected: exit 0 with one H.264 video stream and one AAC audio stream.

- [x] **Step 6: Commit the static repairs**

```bash
git add index.html media/media-podcasts.html podcasts/podcast-dominate.html podcasts/podcast-eclectic-polymath.html work/work-directv.html brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4 data/media-manifest.json tests/test_production_health.py
git commit -m "fix: repair production media fallbacks"
```

---

### Task 3: Xfinity Video and Verified Awards

**Files:**
- Modify: `work/work-xfinity.html`
- Modify: `work/work-gatorade.html`
- Modify: `data/media-manifest.json`
- Modify: `tests/test_production_health.py`
- Create: `tests/test_verified_content.py`

**Interfaces:**
- Xfinity uses the campaign-specific iSpot embed at `https://www.ispot.tv/share/tBI3`; the caption and page design remain unchanged.
- Gatorade displays `2026 Clio Awards · Bronze` with a direct official-source link.

- [x] **Step 1: Write failing content-evidence tests**

```python
class VerifiedContentTests(unittest.TestCase):
    def test_xfinity_uses_replacement_video(self):
        page = (ROOT / "work/work-xfinity.html").read_text(encoding="utf-8")
        self.assertIn("https://www.ispot.tv/share/tBI3", page)
        self.assertNotIn("R4MkK-9fJ9M", page)

    def test_gatorade_clio_bronze_links_official_evidence(self):
        page = (ROOT / "work/work-gatorade.html").read_text(encoding="utf-8")
        self.assertIn("2026 Clio Awards", page)
        self.assertIn("Bronze", page)
        self.assertIn("https://clios.com/winners-gallery/details/220718", page)
```

- [x] **Step 2: Run the tests and confirm both fail**

Run: `../.venv-portfolio-quality/bin/python -m unittest tests.test_verified_content -v`

Expected: two assertion failures because the replacement ID and Clio copy are absent.

- [x] **Step 3: Apply the minimal page and manifest changes**

Replace only the Xfinity iframe source and add a direct fallback link beneath its existing caption. Add the Gatorade award chip beside the Stranger Things campaign evidence, linking the official Clio record with `target="_blank"` and `rel="noopener noreferrer"`. Update the manifest Xfinity URL to the iSpot campaign page and retain the Clio evidence entry.

- [x] **Step 4: Run focused and full tests**

Run: `../.venv-portfolio-quality/bin/python -m unittest tests.test_verified_content tests.test_production_health -v`

Run: `../.venv-portfolio-quality/bin/python -m unittest discover -s tests -v`

Expected: zero failures and zero errors.

- [x] **Step 5: Run static and live health checks**

Run: `../.venv-portfolio-quality/bin/python scripts/check-site.py --root . --json-out reports/site-health.json`

Expected: exit 0 with no static findings.

Run: `../.venv-portfolio-quality/bin/python scripts/check-site.py --root . --live --json-out reports/site-health-live.json || test $? -eq 1`

Expected: any remaining nonzero result names an external source rather than blank markup, placeholder media, or a missing fallback.

- [x] **Step 6: Commit verified content repairs**

```bash
git add work/work-xfinity.html work/work-gatorade.html data/media-manifest.json tests/test_verified_content.py
git commit -m "fix: restore campaign video and award evidence"
```

---

### Task 4: Phase Verification

**Files:**
- Modify: `docs/superpowers/plans/2026-08-04-portfolio-media-repair.md` (checkbox states only)

- [x] **Step 1: Run the complete suite and health CLI**

Run: `../.venv-portfolio-quality/bin/python -m unittest discover -s tests -v`

Run: `../.venv-portfolio-quality/bin/python scripts/check-site.py --root . --json-out reports/site-health.json`

Expected: tests and static health both exit 0.

- [x] **Step 2: Inspect branch scope and media metadata**

Run: `git status --short && git diff origin/main...HEAD --stat && ffprobe -v error brand/directv/ooh-hijack/directv-emmys-ooh-hijack.mp4`

Expected: the worktree is clean and FFprobe exits 0.

- [x] **Step 3: Commit the completed checklist**

```bash
git add docs/superpowers/plans/2026-08-04-portfolio-media-repair.md
git commit -m "docs: complete portfolio media repair plan"
```
