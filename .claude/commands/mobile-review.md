# Mobile Review — Responsive Layout Audit

Reviews all pages for mobile issues and fixes them.

## Instructions

Audit `/home/user/-joshua-portfolio-2026/` for mobile responsiveness problems.

### What to look for

**Hardcoded widths (common culprits)**
```bash
grep -n "width: [0-9]\+px" index.html work/*.html podcasts/*.html
```
Flag any `width: Xpx` over 320px that doesn't have a responsive override.

**Overflow issues**
- Elements with `white-space: nowrap` on text that might overflow on small screens
- Horizontal scroll triggers: wide tables, fixed-width elements in flex containers

**Font sizes**
- Any font below 12px on mobile (search `font-size: [0-9]px` or small `clamp()` values)
- Touch targets smaller than 44×44px (buttons, links)

**Media query gaps**
- Check breakpoints: are there rules at 1100px, 768px, 560px?
- The current grid breakpoints: 1100px (3→2 cols), 560px (2→1 col)
- Are navigation items manageable on 375px width?

**Images**
- `<img>` without `max-width: 100%` or similar constraint
- High-resolution images loaded on mobile (no srcset)

**The header**
- On 375px wide: does "Joshua McKenzie German" + "AI-Enhanced Creative Strategist" fit?
- Does the nav collapse properly on mobile?

### Testing simulation
For each issue found, describe what it would look like on:
- iPhone SE (375×667)
- iPhone 14 Pro (393×852)
- iPad (768×1024)

### Report format
```
## MOBILE REVIEW — [date]

### 🔴 Broken on Mobile
- [file]:[line] — [description] — [fix]

### 🟡 Suboptimal
- [file]:[line] — [description] — [recommendation]

### ✅ Responsive
- [elements that are properly responsive]
```

### Fix what you can
Auto-fix obvious issues: add `max-width: 100%`, fix touch target sizes, update font sizes.
Flag complex layout issues for manual review.

Commit:
```bash
git commit -m "Mobile responsiveness fixes from mobile-review audit"
```
