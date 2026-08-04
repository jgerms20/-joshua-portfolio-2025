#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from portfolio_quality.photography import import_photography_inbox


def main() -> int:
    imported = import_photography_inbox(ROOT)
    if not imported:
        print("No new supported photographs found in photos/inbox")
        return 0

    print(f"Imported {len(imported)} draft photograph(s):")
    for entry in imported:
        print(f"- {entry['src']} -> draft id {entry['id']}")
    print("Add alt text and a chapter in data/photography.json, then set published to true.")
    print("Run scripts/render-photography.py after the edit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
