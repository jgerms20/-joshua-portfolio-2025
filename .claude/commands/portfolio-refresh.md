# Portfolio Refresh — Auto 5 Improvements

Makes 5 meaningful improvements to the portfolio in a single session. No prompting needed.

## Instructions

You are Claude Code working on Joshua McKenzie German's portfolio at `/home/user/-joshua-portfolio-2026/`.

Autonomously identify and implement 5 improvements. Pick from this priority order:

**Priority A — Fix broken things**
- Placeholder iframes (replace with styled "coming soon" divs)
- Missing/broken images (fix paths or use appropriate fallback)
- Dead links (remove or replace)
- JS errors or console warnings

**Priority B — Content freshness**
- Stats in hero (8+ years, 50+ campaigns — update if stale)
- About section copy — does it reflect current role accurately?
- AI projects section — any new projects to add from portfolio-memory.json?
- Work section — any campaign results to update with better numbers?

**Priority C — Visual polish**
- Spacing inconsistencies
- Mobile layout issues
- Typography hierarchy problems
- Cards that look unfinished

**Priority D — Performance**
- Unused CSS classes
- Animation jank points
- Images missing alt text

## Rules
- Make exactly 5 improvements
- Each must be a real, visible change (not just a comment fix)
- After each change, briefly note what you did and why
- Commit all 5 together with a descriptive message
- Push to the current branch

## Output Format
After completing, summarize:
```
✓ 1. [What you changed] — [Why it matters]
✓ 2. [What you changed] — [Why it matters]
✓ 3. [What you changed] — [Why it matters]
✓ 4. [What you changed] — [Why it matters]
✓ 5. [What you changed] — [Why it matters]
```
