# Link Check — Find All Broken Links

Tests every external and internal link across the entire portfolio.

## Instructions

### Step 1: Collect all links
From all HTML files in `/home/user/-joshua-portfolio-2026/`, extract:
- External `href` links (http/https)
- Internal page links (`href="work/..."`, `href="podcasts/..."`)
- Internal anchor links (`href="#section-id"`)

### Step 2: Check internal page links
For each `href="work/[page].html"` or `href="podcasts/[page].html"`, verify the file exists:
```bash
test -f /home/user/-joshua-portfolio-2026/[path] && echo "OK" || echo "MISSING"
```

### Step 3: Check internal anchor links
For each `href="#section-id"`, verify that `id="section-id"` exists somewhere in `index.html`.

### Step 4: Check external links
Use curl with a 10-second timeout to check each unique external URL:
```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 10 --location "[URL]"
```
- 200, 301, 302 = OK
- 404, 410 = broken
- 403, 401 = possibly restricted (flag but don't remove)
- Timeout = flag for manual review

Check these in parallel batches of 5.

### Step 5: Report
```
## LINK CHECK REPORT — [date]

### 🔴 Broken (fix immediately)
- [file]:[line] href="[url]" → [status code]

### 🟡 Restricted/Timeout (verify manually)
- [file]:[line] href="[url]" → [status]

### ✅ Working ([N] links checked)
Total external: [N]
Total internal: [N]
Broken: [N]
```

### Step 6: Fix broken links
- Remove or replace broken external links
- Fix broken internal page references
- Fix broken anchor links (update the href or add the missing id)

Commit fixes:
```bash
git commit -m "Fix [N] broken links found in link check"
```
