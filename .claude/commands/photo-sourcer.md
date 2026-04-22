# Photo Sourcer — Find and Add Campaign Assets

Searches for images and videos from campaigns Joshua has worked on, verifies they're from the right project, then integrates them into the relevant case study page.

## Usage
`/photo-sourcer [campaign name]`

Examples:
- `/photo-sourcer Xfinity The Greatest Gift`
- `/photo-sourcer DoorDash All The Ads`
- `/photo-sourcer BMW Zeus Hera`

## Instructions

### Step 1: Identify the campaign
From the argument, match to a known case study page in `work/`:
- Xfinity → `work/work-xfinity.html`
- DoorDash → `work/work-doordash.html`
- BMW → `work/work-bmw.html`
- Gatorade → `work/work-gatorade.html`
- Samuel Adams → `work/work-samadams.html`
- Sephora → `work/work-sephora.html`
- Levi's → `work/work-levis.html`
- DWB / Driving While Black → `work/work-dwb.html`
- MLB → `work/work-mlb.html`
- Califia → `work/work-califia.html`
- Preach → `work/work-preach.html`
- DIRECTV → `work/work-directv.html`

### Step 2: Search for campaign assets

Search the web for:
1. `"[Campaign Name]" site:goodbysilverstein.com` — Goodby Silverstein case studies
2. `"[Campaign Name]" site:wk.com` — W+K work pages
3. `"[Campaign Name]" site:tbwa.com` — TBWA/Chiat/Day work pages
4. `"[Campaign Name]" [brand] campaign behind the scenes`
5. `"[Campaign Name]" [brand] YouTube` — For video links
6. `"[Campaign Name]" press release OR ad week OR campaign brief`

### Step 3: Verify authenticity
Before using any asset:
- ✅ Confirm the image is from the EXACT campaign (not just a brand photoshoot)
- ✅ Check the year matches the known campaign year
- ✅ Prefer agency portfolio pages (GS&P, W+K, TBWA) as they're authoritative
- ✅ For video: prefer official YouTube links over third-party

**NEVER:**
- Use images from unverified sources
- Use stock photos and label them as campaign assets
- Use images from the wrong campaign year
- Add assets you cannot verify are from this specific campaign

### Step 4: Find official image URLs

For campaign imagery, look for:
1. **Agency portfolio pages** — Often have high-quality press images
2. **AdWeek / Campaign Brief / Shots** — Trade press coverage with stills
3. **YouTube** — Official campaign video embeds
4. **Getty/AP press releases** — Often released with campaigns

Extract direct image URLs (`.jpg`, `.png`, `.webp`) that can be used in `<img>` tags.

### Step 5: Add to the case study page

Read the current case study page. Find the best insertion point:
- After the campaign description section
- Before the Results section
- In a `.case-gallery` div

Add images using this pattern:
```html
<!-- Campaign stills gallery -->
<div class="case-gallery two-col" style="margin: 48px 0;">
    <img loading="lazy" 
         src="[IMAGE_URL]" 
         alt="[Campaign Name] — [brief description]"
         onerror="this.style.display='none'">
    <img loading="lazy" 
         src="[IMAGE_URL_2]" 
         alt="[Campaign Name] — [brief description 2]"
         onerror="this.style.display='none'">
</div>
```

For videos, use the poster+play pattern:
```html
<div class="case-video" style="position:relative; aspect-ratio:16/9; border-radius: 20px; overflow:hidden; background:#111; margin: 48px 0;">
    <iframe 
        width="100%" height="100%"
        src="https://www.youtube.com/embed/[VIDEO_ID]"
        title="[Campaign Name]"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen loading="lazy"
        style="border:none; width:100%; height:100%;">
    </iframe>
</div>
```

### Step 6: Also update the Brand Imagery folder reference

If you found a good hero image, note the URL and suggest updating the bento card in `index.html` to use it.

### Step 7: Report findings

After searching, report:
```
## Photo Sourcer Results: [Campaign Name]

### Found ✅
- [URL] — [description] — [source]
- [URL] — [description] — [source]

### Skipped ⏭️
- [URL] — [reason: wrong year / unverified / low quality]

### Integrated
- Added [N] images to [work page]
- Video embed: [yes/no]

### Could not find
- [What was missing and why]
```

### Step 8: Commit
```
git add work/work-[campaign].html
git commit -m "Add verified campaign assets to [Campaign] case study"
git push origin claude/[current-branch]
```

## How to Upload Your Own Photos

To add real photos you have (from your phone, hard drive, etc.) to the portfolio's photography section or a case study:

### Option A: Direct file upload via Claude Code
1. Tell Claude: "I want to upload a photo for [campaign/section]"
2. Claude will create a new file in the appropriate `Brand Imagery/[Brand]/` folder
3. You need to have the file accessible on your machine
4. Claude can then update the HTML to reference it

### Option B: Drag into Brand Imagery folder
1. Open the repo folder on your machine
2. Navigate to `Brand Imagery/[Brand name]/Supporting Images/`
3. Drop your photo files there (JPG, PNG, WebP recommended)
4. Run `/photo-add` or tell Claude the filename to add it to the portfolio

### Option C: Host externally and link
1. Upload your photos to any image host (Cloudinary, Imgur, your own S3 bucket)
2. Copy the direct image URL (must end in `.jpg`, `.png`, or `.webp`)
3. Tell Claude: "Add this image [URL] to the [campaign] case study"
4. Claude will integrate it with proper alt text and onerror fallbacks

### For Photography Section
The photography grid is in `index.html` under the Photography section.
Each photo uses this pattern:
```html
<div class="photo-item" onclick="openLightbox([index])">
    <img loading="lazy" src="[YOUR_PHOTO_PATH]" alt="[description]">
</div>
```
