# Add Episode — Approachable AI Podcast

Adds a new episode to the Approachable AI podcast page.

## Usage
Run this command then provide the episode details when prompted. Or pass them directly:
`/add-episode EP005 "Episode Title Here" youtube_video_id "One sentence description"`

## Instructions

You are adding a new episode to `/home/user/-joshua-portfolio-2026/podcasts/podcast-approachable-ai.html`.

### Step 1: Gather info (if not provided)
Ask for:
- Episode number (e.g., 005)
- Episode title
- YouTube video ID (the part after `v=` in the URL)
- Brief description (1-2 sentences)

### Step 2: Read the current episodes section
Look for the pattern of existing episode cards in the HTML. The newest episode should go FIRST (top of the list).

### Step 3: Insert the new episode card
Follow the exact same HTML structure as existing episodes:
- YouTube embed iframe with `rel=0&modestbranding=1` params
- Episode number badge
- Title
- Description
- Make it match the existing card styling exactly

### Step 4: Update episode count
If there's a count displayed anywhere, update it.

### Step 5: Commit and push
```
git add podcasts/podcast-approachable-ai.html
git commit -m "Add episode [NUMBER]: [TITLE]"
git push -u origin claude/[current-branch]
```

### Notes
- Always insert new episodes at the TOP of the episode list
- Keep the YouTube embed format consistent: `https://www.youtube.com/embed/[ID]?rel=0&modestbranding=1`
- The description should be conversational, not a formal synopsis
