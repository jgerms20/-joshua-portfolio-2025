#!/usr/bin/env python3
"""
Portfolio Update Script
-----------------------
Reads portfolio-memory.json and regenerates the Claude Code Builds section
in index.html between the <!-- CLAUDE-BUILDS-START --> and <!-- CLAUDE-BUILDS-END --> markers.

Usage:
    python scripts/update-portfolio.py

Run manually after adding a new project to portfolio-memory.json,
or let the weekly GitHub Actions workflow handle it automatically.
"""

import json
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
MEMORY_FILE = ROOT / "portfolio-memory.json"
HTML_FILE = ROOT / "index.html"
START_MARKER = "<!-- CLAUDE-BUILDS-START -->"
END_MARKER = "<!-- CLAUDE-BUILDS-END -->"

ICON_SVG = {
    "award": '<path d="M12 2a4 4 0 0 1 4 4v2h1a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3h1V6a4 4 0 0 1 4-4z"/><circle cx="12" cy="14" r="2"/>',
    "memory": '<path d="M12 2a4 4 0 0 1 4 4v2h1a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3h1V6a4 4 0 0 1 4-4z"/><circle cx="12" cy="14" r="2"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "star": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "default": '<circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>',
}

STATUS_COLORS = {
    "active": ("Active", "rgba(212,255,79,0.15)", "rgba(212,255,79,0.4)", "var(--neon)"),
    "in-progress": ("In Progress", "rgba(255,165,0,0.15)", "rgba(255,165,0,0.4)", "#ffa500"),
    "complete": ("Complete", "rgba(100,200,100,0.15)", "rgba(100,200,100,0.4)", "#64c864"),
    "archived": ("Archived", "rgba(150,150,150,0.15)", "rgba(150,150,150,0.4)", "#999"),
}


def build_tech_pills(tools):
    pills = []
    for tool in tools:
        pills.append(
            f'<span style="font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; '
            f'background: rgba(255,255,255,0.07); color: rgba(255,255,255,0.5); '
            f'letter-spacing: 0.03em;">{tool}</span>'
        )
    return '\n                        '.join(pills)


def build_status_badge(status):
    label, bg, border, color = STATUS_COLORS.get(status, STATUS_COLORS["active"])
    return (
        f'<span style="position: absolute; top: 16px; right: 16px; '
        f'background: {bg}; border: 1px solid {border}; color: {color}; '
        f'font-size: 11px; font-weight: 600; padding: 4px 10px; border-radius: 20px; '
        f'letter-spacing: 0.05em; text-transform: uppercase;">{label}</span>'
    )


def build_card(project, span):
    icon_path = ICON_SVG.get(project.get("icon", "default"), ICON_SVG["default"])
    gradient = project.get("gradient", "linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%)")
    status = project.get("status", "active")
    status_badge = build_status_badge(status)
    tech_pills = build_tech_pills(project.get("tools", []))
    url = project.get("url") or "#"
    tag = project.get("tag", "Project")
    name = project.get("name", "Untitled")
    desc = project.get("description", "")
    project_id = project.get("id", "")

    tag_str = (
        f'<span class="bento-tag">{tag}</span>'
    )

    if url and url != "#":
        wrapper_open = f'<a href="{url}" target="_blank" class="bento-card {span}" data-project="{project_id}">'
        wrapper_close = "</a>"
    else:
        wrapper_open = f'<div class="bento-card {span}" data-project="{project_id}">'
        wrapper_close = "</div>"

    cta_text = "View Project" if not url or url == "#" else ("View Portfolio" if "portfolio" in url else "View Project")

    return f"""
                {wrapper_open}
                    <div class="bento-media" style="background: {gradient}; aspect-ratio: 16/9; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="72" height="72" viewBox="0 0 24 24" fill="none" stroke="rgba(212,255,79,0.7)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" style="position: relative; z-index: 1;">{icon_path}</svg>
                        <div style="position: absolute; top: 0; right: 0; width: 180px; height: 180px; background: rgba(212,255,79,0.04); border-radius: 50%; transform: translate(40%, -40%);"></div>
                        {status_badge}
                    </div>
                    <div class="bento-body">
                        {tag_str}
                        <h3 class="bento-title">{name}</h3>
                        <p class="bento-desc">{desc}</p>
                        <div style="display: flex; gap: 6px; flex-wrap: wrap; margin: var(--space-sm) 0;">
                        {tech_pills}
                        </div>
                        <span class="bento-cta">{cta_text} <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
                    </div>
                {wrapper_close}"""


def build_grid_html(projects):
    claude_projects = [p for p in projects if p.get("category") == "claude-build"]
    if not claude_projects:
        return ""

    count = len(claude_projects)
    if count == 1:
        span = "span-12"
    elif count == 2:
        span = "span-6"
    elif count % 3 == 0:
        span = "span-4"
    else:
        span = "span-6"

    cards = "".join(build_card(p, span) for p in claude_projects)
    return f"""
            <div class="bento-grid reveal reveal-delay-1" style="margin-top: var(--space-2xl);" id="claude-builds-grid">{cards}

            </div>"""


def update_html(html_content, new_grid_html):
    pattern = re.compile(
        rf"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})",
        re.DOTALL,
    )
    replacement = rf"\g<1>{new_grid_html}\n            \g<3>"
    new_content, subs = pattern.subn(replacement, html_content)
    if subs == 0:
        print("ERROR: Could not find CLAUDE-BUILDS-START/END markers in index.html", file=sys.stderr)
        sys.exit(1)
    return new_content


def main():
    if not MEMORY_FILE.exists():
        print(f"ERROR: {MEMORY_FILE} not found", file=sys.stderr)
        sys.exit(1)

    with open(MEMORY_FILE) as f:
        memory = json.load(f)

    projects = memory.get("projects", [])
    claude_count = sum(1 for p in projects if p.get("category") == "claude-build")
    print(f"Found {len(projects)} total projects ({claude_count} Claude builds)")

    new_grid = build_grid_html(projects)

    with open(HTML_FILE) as f:
        html = f.read()

    updated = update_html(html, new_grid)

    # Update last_updated in memory file
    memory["last_updated"] = date.today().isoformat()
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    with open(HTML_FILE, "w") as f:
        f.write(updated)

    print(f"Updated {HTML_FILE} with {claude_count} Claude Code project cards")
    print(f"Updated last_updated in {MEMORY_FILE} to {memory['last_updated']}")


if __name__ == "__main__":
    main()
