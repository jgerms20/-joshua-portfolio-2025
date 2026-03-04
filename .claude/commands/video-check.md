# Video Check — Find and Fix Broken YouTube Embeds

Checks every YouTube iframe across all pages, verifies they actually load, finds working replacements for broken ones.

## Instructions

You are checking ALL YouTube embeds in `/home/user/-joshua-portfolio-2026/`.

### Step 1: Find all YouTube iframes
Search all HTML files for `youtube.com/embed/` and collect every video ID. Also flag:
- Any iframe with "placeholder" in the src
- Any iframe where the video ID is not an 11-character alphanumeric string

### Step 2: Verify each video ID
For each real video ID, try to fetch the YouTube oEmbed endpoint to confirm it exists:
```bash
curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK:', d.get('title','?'))" 2>/dev/null || echo "BROKEN"
```

### Step 3: For broken/placeholder videos, find the real one
For each broken video, you know the campaign context (brand, campaign name, etc). Use WebSearch to find the real YouTube URL:
- Search: "[Brand] [Campaign Name] official youtube"
- Or look for the video on the brand's official YouTube channel
- Must be the ACTUAL campaign video, not just any related video

Verify the replacement video actually exists before swapping it in.

### Step 4: Replace in HTML
For each broken iframe, replace the `src` with the working YouTube embed URL. Keep all other iframe attributes the same.

For videos you cannot find (genuinely unavailable), replace the iframe with the styled placeholder:
```html
<div class="video-placeholder">
    <svg>...</svg>
    <span>Video Coming Soon</span>
</div>
```

### Step 5: Report and commit
```
## Video Check Report

✓ Working: [list of working videos with titles]
🔧 Fixed: [list of videos that were broken → replaced with real URL]
📋 Placeholder: [list of videos with no findable replacement]
```

Commit all fixes:
```bash
git add work/*.html podcasts/*.html
git commit -m "Fix broken YouTube embeds across portfolio"
git push -u origin claude/[current-branch]
```
