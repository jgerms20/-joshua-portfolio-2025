# Perf Check — Performance and Load Speed Audit

Identifies performance bottlenecks and makes quick fixes for faster page loads.

## Instructions

### Step 1: Scan for performance issues

**Image optimization**
```bash
find . -name "*.jpg" -o -name "*.png" -o -name "*.tiff" | grep -v node_modules
```
Flag:
- TIFF files (should be JPG/WebP)
- Images over 1MB that lack `loading="lazy"`
- Images without `width`/`height` attributes (causes layout shift)

**JavaScript**
- Look for `setInterval`, `requestAnimationFrame` loops that run indefinitely
- Large inline `<script>` blocks that block rendering
- Missing `defer` or `async` on script tags

**CSS**
- `backdrop-filter: blur()` on many elements (GPU pressure)
- `will-change` used without `transform: translateZ(0)` companion
- Animations running without `prefers-reduced-motion` guard

**Fonts**
- How many Google Fonts are loaded? (Each font family = extra request)
- Are fonts using `font-display: swap`?

**Resource hints**
- `<link rel="preload">` on hero images?
- `<link rel="preconnect">` to Google Fonts, CDNs?

### Step 2: Apply quick wins
Fix in `index.html`:
- Add `loading="lazy"` to below-fold images
- Add `font-display: swap` to font imports
- Add `preconnect` resource hints
- Add `prefers-reduced-motion` guards to any unguarded animations

### Step 3: Report
```
## PERF CHECK — [date]

### Fixed automatically
[List of changes made]

### Needs manual attention
[Large files, TIFF conversions, etc. — flag for Joshua to handle]

### Estimated improvement
[Rough assessment of impact]
```
