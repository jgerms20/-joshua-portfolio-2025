# Portfolio Reliability Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the portfolio's date-touching automation with a tested quality system that discovers production pages, reports actionable local defects, models external media checks, and fails CI on critical breakage.

**Architecture:** A small Python package owns page discovery, finding/report types, static HTML checks, and network probes. A thin CLI composes those units for local, scheduled, and post-deployment runs. The existing Monday/Friday workflow runs tests and the CLI but never edits portfolio content merely to update a date.

**Tech Stack:** Python 3.11, standard-library `unittest`, Beautiful Soup 4, Requests, Pillow, JSON, GitHub Actions.

## Global Constraints

- Preserve the current site design; this phase changes no visitor-facing layout or copy.
- Production scope is `index.html`, `work/work-*.html` except `work-template.html`, `podcasts/podcast-*.html`, and `media/media-*.html`.
- Exclude `archives/`, `versions/`, `concepts/`, and `index-gemini-ultra.html` from production checks.
- Critical failures exit nonzero; warnings remain visible without rewriting content.
- Network checks use finite timeouts and classify `broken`, `degraded`, and `unverifiable` separately.
- No scheduled job commits a date-only change.
- No deployment, merge, or public publication occurs in this phase.

---

### Task 1: Production Page Registry and Finding Model

**Files:**
- Create: `portfolio_quality/__init__.py`
- Create: `portfolio_quality/model.py`
- Create: `portfolio_quality/pages.py`
- Create: `tests/test_pages.py`

**Interfaces:**
- Produces: `discover_production_pages(root: Path) -> list[Path]`
- Produces: `Finding(severity: str, code: str, page: str, target: str, message: str)`
- Produces: `HealthReport(findings: list[Finding])` with `has_critical`, `to_dict()`, and `exit_code()`.

- [ ] **Step 1: Write failing discovery and model tests**

```python
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
        warning = Finding("degraded", "external-rate-limit", "index.html", "https://example.com", "rate limited")
        broken = Finding("broken", "missing-local-file", "index.html", "photos/missing.jpg", "not found")

        self.assertEqual(HealthReport([warning]).exit_code(), 0)
        self.assertEqual(HealthReport([warning, broken]).exit_code(), 1)
```

- [ ] **Step 2: Run the tests and confirm the import failure**

Run: `python3 -m unittest tests.test_pages -v`

Expected: `ModuleNotFoundError: No module named 'portfolio_quality'`.

- [ ] **Step 3: Implement the minimal registry and data model**

```python
@dataclass(frozen=True, slots=True)
class Finding:
    severity: str
    code: str
    page: str
    target: str
    message: str


@dataclass(slots=True)
class HealthReport:
    findings: list[Finding]

    @property
    def has_critical(self) -> bool:
        return any(item.severity == "broken" for item in self.findings)

    def exit_code(self) -> int:
        return int(self.has_critical)

    def to_dict(self) -> dict[str, object]:
        return {"ok": not self.has_critical, "findings": [asdict(item) for item in self.findings]}
```

`discover_production_pages()` must build its result from the four explicit production globs and return resolved files sorted by repository-relative POSIX path.

- [ ] **Step 4: Run the focused test module**

Run: `python3 -m unittest tests.test_pages -v`

Expected: 2 tests pass.

- [ ] **Step 5: Commit the registry and model**

```bash
git add portfolio_quality/__init__.py portfolio_quality/model.py portfolio_quality/pages.py tests/test_pages.py
git commit -m "test: define production portfolio pages"
```

---

### Task 2: Static HTML Quality Checks

**Files:**
- Create: `portfolio_quality/html_checks.py`
- Create: `tests/test_html_checks.py`
- Create: `tests/fixtures/site/index.html`
- Modify: `requirements.txt`

**Interfaces:**
- Consumes: `Finding` from `portfolio_quality.model`
- Produces: `check_page(root: Path, page: Path) -> list[Finding]`
- Produces finding codes: `blank-source`, `placeholder-media`, `missing-local-file`, `unreadable-image`, `missing-alt`, `missing-iframe-title`, `duplicate-id`, and `missing-fragment`.

- [ ] **Step 1: Write failing tests for visitor-impacting defects**

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from portfolio_quality.html_checks import check_page


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
        Image.new("RGB", (2, 2), "white").save(photo)
        findings = self.check_html_fixture(
            '<img src="photos/working.png" alt="Portrait"><a href="https://example.com">Source</a>'
        )
        self.assertEqual(findings, [])

    def test_reports_an_image_that_cannot_be_decoded(self):
        photo = self.root / "photos/broken.jpg"
        photo.parent.mkdir(parents=True, exist_ok=True)
        photo.write_text("not an image", encoding="utf-8")
        findings = self.check_html_fixture('<img src="photos/broken.jpg" alt="Broken image">')
        self.assertEqual([finding.code for finding in findings], ["unreadable-image"])
```

- [ ] **Step 2: Run the tests and confirm `check_page` is missing**

Run: `python3 -m unittest tests.test_html_checks -v`

Expected: import failure for `portfolio_quality.html_checks`.

- [ ] **Step 3: Implement Beautiful Soup checks**

Use `BeautifulSoup(page.read_text(encoding="utf-8"), "lxml")`. Resolve local `src`, `poster`, and non-fragment `href` values against the page directory after removing query strings and fragments. Treat protocol-relative and `http`, `https`, `mailto`, `tel`, `data`, and `javascript` targets as non-local. Preserve filesystem case by checking the exact resolved path. For local `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, and `.avif` sources, call `PIL.Image.open(path).verify()` and report `unreadable-image` if Pillow cannot decode the file or reports zero width or height. Add `Pillow>=10.0.0` to `requirements.txt`.

Severity rules:

```python
BROKEN_CODES = {
    "blank-source",
    "missing-local-file",
    "unreadable-image",
    "duplicate-id",
    "missing-fragment",
    "placeholder-media",
}
DEGRADED_CODES = {"missing-alt", "missing-iframe-title"}
```

The literal phrases `Video Coming Soon`, `PLACEHOLDER`, and a media URL containing `placeholder` produce `placeholder-media` findings.

- [ ] **Step 4: Run focused tests**

Run: `python3 -m unittest tests.test_html_checks -v`

Expected: 3 tests pass.

- [ ] **Step 5: Run checks against the real production pages and save the baseline**

Run: `python3 -m unittest tests.test_pages tests.test_html_checks -v`

Expected: 5 tests pass. The real-site CLI does not exist yet, so no claim is made about current portfolio health.

- [ ] **Step 6: Commit static checks**

```bash
git add requirements.txt portfolio_quality/html_checks.py tests/test_html_checks.py tests/fixtures/site
git commit -m "feat: detect broken production markup"
```

---

### Task 3: Manifest-Driven External Media Probes

**Files:**
- Create: `data/media-manifest.json`
- Create: `portfolio_quality/network_checks.py`
- Create: `tests/fixtures/spotify-show.html`
- Create: `tests/test_network_checks.py`

**Interfaces:**
- Produces: `load_media_manifest(path: Path) -> list[dict[str, object]]`
- Produces: `probe_manifest(root: Path, entries: list[dict[str, object]], fetch: Callable[..., ResponseLike]) -> list[Finding]`
- Media entry fields: `id`, `page`, `kind`, `url`, `fallback`, `critical`, `last_verified`, and `evidence_url`.

- [ ] **Step 1: Write failing tests around status classification**

```python
from dataclasses import dataclass
from pathlib import Path
import unittest

from portfolio_quality.network_checks import probe_manifest


@dataclass
class FakeResponse:
    status_code: int


class FakeFetch:
    def __init__(self, statuses):
        self.statuses = statuses

    def __call__(self, url, **_kwargs):
        return FakeResponse(self.statuses[url])


class NetworkCheckTests(unittest.TestCase):
    def test_critical_404_without_fallback_is_broken(self):
        entries = [{
            "id": "hero",
            "page": "index.html",
            "kind": "image",
            "url": "https://cdn.example/missing.jpg",
            "fallback": "",
            "critical": True,
            "last_verified": "2026-08-04",
            "evidence_url": "",
        }]
        findings = probe_manifest(Path("."), entries, fetch=FakeFetch({entries[0]["url"]: 404}))
        self.assertEqual(findings[0].severity, "broken")

    def test_rate_limit_with_working_fallback_is_unverifiable(self):
        entries = [{
            "id": "video",
            "page": "work/work-sample.html",
            "kind": "youtube",
            "url": "https://www.youtube.com/watch?v=abc",
            "fallback": "brand/sample/poster.jpg",
            "critical": True,
            "last_verified": "2026-08-04",
            "evidence_url": "",
        }]
        endpoint = "https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3Dabc&format=json"
        findings = probe_manifest(Path("."), entries, fetch=FakeFetch({endpoint: 429}))
        self.assertEqual(findings[0].severity, "unverifiable")
```

- [ ] **Step 2: Run the tests and confirm the network module is missing**

Run: `python3 -m unittest tests.test_network_checks -v`

Expected: import failure for `portfolio_quality.network_checks`.

- [ ] **Step 3: Implement dependency-injected probes**

Generic URLs use GET with a 10-second timeout and at most one retry for timeouts and 5xx responses. YouTube entries convert their watch URL to the public oEmbed endpoint. Status rules are:

```python
if 200 <= status < 400:
    return None
if status in {408, 425, 429} or status >= 500:
    severity = "unverifiable"
elif fallback_resolves_locally:
    severity = "degraded"
else:
    severity = "broken"
```

The initial manifest contains the verified Spotify show URL and Clio evidence URL plus records for known broken media. Known broken records are allowed in the manifest; the CLI reports them until the media-repair phase supplies working URLs or fallbacks.

```json
{
  "version": 1,
  "entries": [
    {
      "id": "eclectic-polymath-spotify",
      "page": "podcasts/podcast-eclectic-polymath.html",
      "kind": "spotify",
      "url": "https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069",
      "fallback": "",
      "critical": true,
      "last_verified": "2026-08-04",
      "evidence_url": "https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069"
    },
    {
      "id": "gatorade-no-ordinary-athlete-clio",
      "page": "work/work-gatorade.html",
      "kind": "award-evidence",
      "url": "https://clios.com/winners-gallery/details/220718",
      "fallback": "",
      "critical": true,
      "last_verified": "2026-08-04",
      "evidence_url": "https://clios.com/winners-gallery/details/220718"
    },
    {
      "id": "directv-emmys-youtube",
      "page": "work/work-directv.html",
      "kind": "youtube",
      "url": "https://www.youtube.com/watch?v=gxJNsUCJ1qk",
      "fallback": "brand/directv/ooh-hijack/DIRECTV Emmy's OOH Hijack.MOV",
      "critical": true,
      "last_verified": "2026-08-04",
      "evidence_url": ""
    },
    {
      "id": "xfinity-campaign-youtube",
      "page": "work/work-xfinity.html",
      "kind": "youtube",
      "url": "https://www.youtube.com/watch?v=R4MkK-9fJ9M",
      "fallback": "",
      "critical": true,
      "last_verified": "2026-08-04",
      "evidence_url": ""
    }
  ]
}
```

- [ ] **Step 4: Run focused network tests without live internet**

Run: `python3 -m unittest tests.test_network_checks -v`

Expected: all fixture-driven tests pass with no network access.

- [ ] **Step 5: Commit the external probe layer**

```bash
git add data/media-manifest.json portfolio_quality/network_checks.py tests/fixtures/spotify-show.html tests/test_network_checks.py
git commit -m "feat: classify external portfolio media"
```

---

### Task 4: Health Check CLI and Machine-Readable Report

**Files:**
- Create: `scripts/check-site.py`
- Create: `tests/test_check_site_cli.py`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: page discovery, HTML checks, media manifest probes, and `HealthReport`.
- CLI: `python3 scripts/check-site.py --root PATH [--live] [--json-out PATH]`
- Exit code: `0` when no `broken` finding exists; `1` when at least one `broken` finding exists; `2` for invalid configuration or unreadable input.

- [ ] **Step 1: Write failing subprocess tests**

```python
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class CheckSiteCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        (self.site / "index.html").write_text('<img src="missing.jpg" alt="Missing">', encoding="utf-8")
        self.report = self.site / "report.json"

    def test_broken_fixture_writes_json_and_exits_one(self):
        result = subprocess.run(
            [sys.executable, "scripts/check-site.py", "--root", str(self.site), "--json-out", str(self.report)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(self.report.read_text())
        self.assertFalse(payload["ok"])
        self.assertGreater(payload["summary"]["broken"], 0)
```

- [ ] **Step 2: Run the CLI tests and confirm the script is absent**

Run: `python3 -m unittest tests.test_check_site_cli -v`

Expected: failure because `scripts/check-site.py` does not exist.

- [ ] **Step 3: Implement the thin CLI**

The CLI must add the repository root to `sys.path`, discover pages, collect static findings, optionally run manifest probes only with `--live`, print findings grouped by severity, and write JSON with this stable shape:

```json
{
  "ok": false,
  "checked_at": "2026-08-04T20:00:00Z",
  "pages_checked": 18,
  "summary": {"broken": 1, "degraded": 2, "unverifiable": 0},
  "findings": []
}
```

Add `reports/*.json` to `.gitignore` while retaining `reports/.gitkeep` if the directory is committed later.

- [ ] **Step 4: Run CLI tests**

Run: `python3 -m unittest tests.test_check_site_cli -v`

Expected: subprocess exit and JSON assertions pass.

- [ ] **Step 5: Run the CLI against the current portfolio baseline**

Run: `python3 scripts/check-site.py --root . --json-out reports/site-health.json || test $? -eq 1`

Expected: a JSON report is created. Existing production defects may produce exit 1; the command records that baseline without weakening severity rules.

- [ ] **Step 6: Commit the CLI**

```bash
git add .gitignore scripts/check-site.py tests/test_check_site_cli.py
git commit -m "feat: add portfolio health CLI"
```

---

### Task 5: Replace Date-Touching Automation

**Files:**
- Modify: `.github/workflows/weekly-update.yml`
- Create: `tests/test_workflow_contract.py`

**Interfaces:**
- Scheduled runs: Monday and Friday at `17:00 UTC`.
- Pull-request runs: tests and offline static checks.
- Scheduled/manual runs: tests, offline checks, then `--live` probes.
- Artifact: `site-health-report` containing `reports/site-health.json`.

- [ ] **Step 1: Write failing workflow contract tests**

```python
class WorkflowContractTests(unittest.TestCase):
    def test_workflow_runs_tests_and_never_commits_date_only_updates(self):
        workflow = (ROOT / ".github/workflows/weekly-update.yml").read_text()
        self.assertIn("python3 -m unittest discover -s tests -v", workflow)
        self.assertIn("python3 scripts/check-site.py --root .", workflow)
        self.assertIn("actions/upload-artifact@v4", workflow)
        self.assertNotIn("scripts/update-portfolio.py", workflow)
        self.assertNotIn("git commit", workflow)
        self.assertNotIn("git push", workflow)
```

- [ ] **Step 2: Run the contract test and confirm it fails on the old workflow**

Run: `python3 -m unittest tests.test_workflow_contract -v`

Expected: failure because the current workflow calls `scripts/update-portfolio.py` and commits changes.

- [ ] **Step 3: Rewrite the workflow as a checker**

Retain both cron expressions and `workflow_dispatch`. Add `pull_request` and `push` triggers for relevant Python, JSON, HTML, and workflow paths. Install `requirements.txt`, run the full unittest suite, run offline CLI checks on every trigger, run live checks only for `schedule` and `workflow_dispatch`, and upload the JSON report with `if: always()`.

Do not configure write permissions, Git identity, commit commands, or push commands.

- [ ] **Step 4: Run the workflow contract and full unit suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: all test modules pass.

- [ ] **Step 5: Validate workflow YAML and the current baseline report**

Run: `python3 -c 'import pathlib, yaml; yaml.safe_load(pathlib.Path(".github/workflows/weekly-update.yml").read_text())'`

Expected: exit 0. Add `PyYAML>=6.0` to `requirements.txt` so this validation command is reproducible locally and in CI.

Run: `python3 scripts/check-site.py --root . --json-out reports/site-health.json || test $? -eq 1`

Expected: report generation succeeds even if existing site defects correctly produce exit 1.

- [ ] **Step 6: Commit the workflow replacement**

```bash
git add .github/workflows/weekly-update.yml tests/test_workflow_contract.py requirements.txt
git commit -m "ci: replace portfolio date updates with health checks"
```

---

### Task 6: Phase Verification and Baseline Handoff

**Files:**
- Modify: `docs/superpowers/plans/2026-08-04-portfolio-reliability-foundation.md` (checkbox states only)

**Interfaces:**
- Produces a clean branch with a reproducible test suite and an explicit baseline defect report for Phase 2.

- [ ] **Step 1: Run the complete test suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: zero failures and zero errors.

- [ ] **Step 2: Run static health against the repository**

Run: `python3 scripts/check-site.py --root . --json-out reports/site-health.json || test $? -eq 1`

Expected: the report file parses as JSON; existing broken findings are enumerated with page, target, and code.

- [ ] **Step 3: Run a bounded live probe**

Run: `python3 scripts/check-site.py --root . --live --json-out reports/site-health-live.json || test $? -eq 1`

Expected: the command completes within configured timeouts and records external results without modifying portfolio content.

- [ ] **Step 4: Inspect repository scope**

Run: `git status --short && git diff origin/main...HEAD --stat && git log --oneline origin/main..HEAD`

Expected: only the committed spec, plan, reliability package, manifests, tests, CLI, ignore rule, requirements, and workflow are changed.

- [ ] **Step 5: Commit completed checklist state**

```bash
git add docs/superpowers/plans/2026-08-04-portfolio-reliability-foundation.md
git commit -m "docs: complete reliability foundation plan"
```
