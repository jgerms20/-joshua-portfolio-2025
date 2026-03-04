# Portfolio Audit — Find Everything Broken

Scans every page and reports all issues. Run before any major update.

## Instructions

You are auditing all HTML files in `/home/user/-joshua-portfolio-2026/`.

### Files to check
- `index.html`
- `work/work-*.html` (all 8 work pages)
- `podcasts/podcast-*.html` (all 3 podcast pages)

### What to check for

**1. Broken media**
- `<img>` tags where the `src` file doesn't exist locally
- `<iframe>` tags with placeholder YouTube IDs (contain "placeholder")
- `<video>` tags with missing src files
- `background-image` CSS referencing non-existent files

**2. Dead links**
- Internal `href="#section-id"` that don't exist
- Links to work/podcast pages that don't exist

**3. Content placeholders**
- Lorem ipsum text
- "[Coming Soon]", "[TBD]", "[TODO]" text
- Empty `alt=""` attributes on meaningful images

**4. JS errors**
- `getElementById` calls for elements that don't exist
- Obvious undefined variable references

**5. Consistency issues**
- Pages missing the standard back-to-portfolio navigation
- Inconsistent page titles
- Missing meta descriptions

### Output Format

Return a structured report:

```
## AUDIT REPORT — [date]

### 🔴 Critical (broken user experience)
- [file]:[line] — [issue]

### 🟡 Warnings (degraded experience)
- [file]:[line] — [issue]

### 🔵 Nice to Fix (polish)
- [file]:[line] — [issue]

### ✅ Clean
- [list of files with no issues]

TOTAL: [X] critical, [Y] warnings, [Z] polish items
```

### After the audit
Ask: "Fix all critical issues now?" and if yes, go fix them.
