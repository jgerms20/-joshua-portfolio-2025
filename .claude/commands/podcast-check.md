# Podcast Check — Verify and Update All Podcast Content

Audits all podcast pages, checks for new episodes to add, and ensures consistency.

## Instructions

### Step 1: Inventory current episodes
Read all podcast HTML files:
```bash
ls podcasts/podcast-*.html
```

For each file, extract:
- Episode list (EP numbers and titles)
- YouTube embed IDs
- Episode descriptions

### Step 2: Check for missing or placeholder episodes
- Flag any `iframe` with `placeholder` in the src
- Check if any episodes are listed without YouTube IDs
- Identify the latest episode number to know if any are missing

### Step 3: Verify YouTube links are live
For each YouTube embed ID found, check:
```bash
curl -s "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=[ID]&format=json" | python3 -c "import sys,json; d=json.load(sys.stdin); print('✅', d['title'])"
```
Flag any that return errors.

### Step 4: Check episode consistency
- Are episode descriptions consistent in tone and length?
- Do all episodes have timestamps or show notes?
- Is the episode count in the nav/header accurate?

### Step 5: Report
```
## PODCAST CHECK — [date]

### Episodes verified: [X]
### Broken embeds: [list]
### Missing episodes: [list]
### Inconsistencies: [list]
```

Ask: "Is there a new episode to add? Run /add-episode."
