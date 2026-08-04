#!/usr/bin/env python3
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from portfolio_quality.photography import load_photography_manifest, render_darkroom


START = "<!-- PHOTOGRAPHY:START -->"
END = "<!-- PHOTOGRAPHY:END -->"
LEGACY_END = "    <!-- =====================================================\n         07 — THE COLLECTION (dark)"


def replace_darkroom(page: str, rendered: str) -> str:
    block = f"{START}\n    {rendered}\n    {END}\n\n"
    if START in page and END in page:
        before, remainder = page.split(START, 1)
        _, after = remainder.split(END, 1)
        return before + block + after.lstrip("\n")

    legacy_start = page.index('    <section id="photography" class="chapter chapter-dark">')
    legacy_end = page.index(LEGACY_END, legacy_start)
    return page[:legacy_start] + "    " + block + page[legacy_end:]


def main() -> int:
    manifest = load_photography_manifest(ROOT / "data/photography.json")
    index_path = ROOT / "index.html"
    original = index_path.read_text(encoding="utf-8")
    rendered = render_darkroom(manifest)
    updated = replace_darkroom(original, rendered)
    if updated != original:
        index_path.write_text(updated, encoding="utf-8")
        print(f"Rendered {len(manifest)} published photographs into index.html")
    else:
        print("Photography markup is already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
