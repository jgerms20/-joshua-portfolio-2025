# Add Episode — The Eclectic Polymath Podcast

Adds a new episode to the Eclectic Polymath podcast page.

## Usage
`/add-eclectic-episode EP006 "Episode Title" spotify_episode_id "One sentence description"`

Or run without args and you'll be prompted.

## Instructions

You are adding a new episode to `/home/user/-joshua-portfolio-2026/podcasts/podcast-eclectic-polymath.html`.

### Step 1: Gather info (if not provided)
Ask for:
- Episode number (e.g., 006)
- Spotify episode ID (the part after `/episode/` in the embed URL, e.g., `4GXJ0Jtdw03mdxAxikMbao`)
- To get the embed: in Spotify, click ··· → Share → Embed → copy the `src` URL and extract the ID

### Step 2: Read the current episodes section
Find the first `<!-- Episode 00X — LATEST -->` comment. The newest episode goes FIRST.

### Step 3: Update the previous "Latest" label
Change the old Episode 005's `episode-label-text` from `Latest Episode` back to `Episode 005`.

### Step 4: Insert the new episode card at the TOP

Use this exact structure:
```html
<!-- Episode 00X — LATEST -->
<div class="episode-item">
    <div class="episode-header">
        <div class="episode-number">0X</div>
        <span class="episode-label-text">Latest Episode</span>
    </div>
    <div class="episode-embed">
        <iframe data-testid="embed-iframe" style="border-radius:12px"
            src="https://open.spotify.com/embed/episode/[SPOTIFY_EPISODE_ID]?utm_source=generator"
            width="100%" height="352" frameBorder="0" allowfullscreen=""
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy"></iframe>
    </div>
</div>
```

### Step 5: Update the episode count badge
Find `<strong id="ep-count">` and increment the number by 1.

### Step 6: Commit and push
```
git add podcasts/podcast-eclectic-polymath.html
git commit -m "Add Eclectic Polymath EP[NUMBER]"
git push -u origin claude/[current-branch]
```

## How to get a Spotify episode embed ID
1. Open the episode in Spotify (desktop or web)
2. Click the **···** (more options) button
3. Click **Share** → **Copy Embed Code**
4. The embed src URL looks like: `https://open.spotify.com/embed/episode/[ID]?utm_source=generator`
5. The ID is the string between `/episode/` and `?`

## Current episode count: 5
- EP005: `4GXJ0Jtdw03mdxAxikMbao`
- EP004: `44spk33dHWs5X3ARwNLwBo`
- EP003: `1t1UH9eFAAppQxwgy31Yko`
- EP002: `5c802TfEsUMM2XjzzlgFtV`
- EP001: `5hlycC2HvZaI98HEyEoi98`
