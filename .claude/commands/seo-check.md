# SEO Check — Portfolio Discoverability Audit

Ensures every page is properly optimized for search and social sharing.

## Instructions

### Step 1: Check each HTML file
For each of `index.html`, `work/work-*.html`, `podcasts/podcast-*.html`, verify:

**Title tags**
- Present and unique per page
- Under 60 characters
- Includes the page subject + Joshua's name

**Meta descriptions**
- Present on every page
- 120-160 characters
- Describes the page content with a hook (not generic)

**OG/Twitter cards**
- `og:title`, `og:description`, `og:image` present
- `twitter:card`, `twitter:title`, `twitter:description` present
- OG image exists and is the right dimensions (1200×630)

**Heading hierarchy**
- One `<h1>` per page
- `<h2>` for main sections, `<h3>` for sub-items
- No skipped levels

**Alt text on meaningful images**
- All non-decorative images have descriptive alt text
- Alt text describes what's in the image, not filename

### Step 2: Fix all issues found
Apply fixes directly to files.

### Step 3: Generate a shareable OG image prompt
If OG images are missing, output a Midjourney/DALL-E prompt for creating a proper 1200×630 portfolio card image.

### Step 4: Commit
```bash
git add .
git commit -m "SEO improvements: meta descriptions, OG tags, heading hierarchy"
```
