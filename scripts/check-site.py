#!/usr/bin/env python3
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from portfolio_quality.html_checks import check_page
from portfolio_quality.model import HealthReport
from portfolio_quality.network_checks import load_media_manifest, probe_manifest
from portfolio_quality.pages import discover_production_pages


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Check production portfolio health")
    parser.add_argument("--root", type=Path, required=True, help="portfolio root")
    parser.add_argument("--live", action="store_true", help="probe external media")
    parser.add_argument("--json-out", type=Path, help="write a JSON report")
    return parser.parse_args(argv)


def build_payload(report: HealthReport, pages_checked: int) -> dict[str, object]:
    serialized = report.to_dict()
    counts = Counter(item.severity for item in report.findings)
    return {
        "ok": serialized["ok"],
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pages_checked": pages_checked,
        "summary": {
            "broken": counts["broken"],
            "degraded": counts["degraded"],
            "unverifiable": counts["unverifiable"],
        },
        "findings": serialized["findings"],
    }


def print_report(payload: dict[str, object]) -> None:
    summary = payload["summary"]
    print(
        "Portfolio health: "
        f"{summary['broken']} broken, "
        f"{summary['degraded']} degraded, "
        f"{summary['unverifiable']} unverifiable"
    )
    for finding in payload["findings"]:
        print(
            f"[{finding['severity']}] {finding['page']} "
            f"{finding['code']}: {finding['target']} — {finding['message']}"
        )


def main(argv=None) -> int:
    args = parse_args(argv)
    root = args.root
    if not root.is_dir():
        print(f"error: portfolio root is not a directory: {root}", file=sys.stderr)
        return 2

    try:
        pages = discover_production_pages(root)
        findings = [finding for page in pages for finding in check_page(root, page)]
        manifest = root / "data/media-manifest.json"
        if args.live and manifest.is_file():
            findings.extend(probe_manifest(root, load_media_manifest(manifest)))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    report = HealthReport(findings)
    payload = build_payload(report, len(pages))
    print_report(payload)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return report.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
