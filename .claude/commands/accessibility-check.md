# Accessibility Check — WCAG Audit

Audits all pages for accessibility issues and fixes what it can automatically.

## Instructions

Check `/home/user/-joshua-portfolio-2026/` for these WCAG 2.1 issues:

### Automated checks (grep-based)

**Images**
- `<img>` missing `alt` attribute entirely
- `<img alt="">` on non-decorative images (images with meaningful content)
- Background images used for content (no alt available)

**Color contrast** (flag for manual review)
- Text colors `var(--text-muted)` and `var(--text-tertiary)` against dark backgrounds
- Note: `rgba(255,255,255,0.35)` = ~3.5:1 ratio, borderline AA

**Interactive elements**
- `<button>` without `aria-label` or visible text
- `<a>` with only SVG icon content and no aria-label
- Links opening in new tab without `aria-label` warning users

**Forms**
- `<input>` without associated `<label>`

**Headings**
- Skipped heading levels (h1 → h3 with no h2)
- Multiple h1 tags on one page

**Focus management**
- Elements with `tabindex` greater than 0
- Interactive elements that might not be keyboard-reachable

**ARIA**
- `aria-label` on non-interactive elements
- `role` attributes used incorrectly

### Output format
```
## ACCESSIBILITY REPORT — [date]

### 🔴 WCAG Failures (must fix)
- [file]:[line] — [issue] — [fix]

### 🟡 Warnings (should fix)
- [file]:[line] — [issue] — [fix]

### 🔵 Recommendations
- [suggestion]

SCORE: [X]/100 estimated
```

### Auto-fix what you can
- Add missing `alt=""` to decorative images
- Add `aria-label` to icon-only buttons and links
- Add `target="_blank"` warning: `aria-label="...(opens in new tab)"`
- Fix heading hierarchy issues

Commit fixes separately from the report.
