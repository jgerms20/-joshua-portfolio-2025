# Media Diet Update — Refresh What You're Reading and Watching

Updates the Media Diet / Reading Stack section with new content.

## Usage
`/media-diet-update` then answer prompts.

## Instructions

### Step 1: Find the media diet section
Look for `id="media-diet"` or similar in `index.html`.

### Step 2: Gather new content
Ask for (can provide multiple):
- **Books**: Title, author, status (reading/finished/recommending)
- **Podcasts**: Show name, why it's on the list
- **Newsletters**: Newsletter name, author
- **Videos/Films**: What and why
- **Tools**: Apps or tools recently added to workflow

### Step 3: Add new items
New media item format:
```html
<a href="[URL or #]" class="media-consumption-item" target="_blank" rel="noopener">
    <div class="media-consumption-content">
        <span class="media-type">[Book|Podcast|Newsletter|Tool]</span>
        <h4>[Title]</h4>
        <p>[Author or source] — [One-line reason it's worth your time]</p>
    </div>
</a>
```

### Step 4: Archive old items
If the section is full, move older items to an archived state or remove the least relevant. Keep the list feeling current — 8-12 items max.

### Step 5: Update the "Last updated" date
Find any date stamp in the media diet section and update it to today.

### Step 6: Commit
```bash
git add index.html
git commit -m "Update media diet — [month year]"
```
