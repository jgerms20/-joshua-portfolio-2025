# Ticker Update — Refresh the Skills Ticker

Updates the running skills ticker at the top of the portfolio with new skills, updated proficiency percentages, and current tools.

## Instructions

### Step 1: Find the ticker
Search `index.html` for `class="ticker-track"` or `ticker-content`. Read the current ticker items — they're typically structured as:
```html
<div class="ticker-item">
    <span class="ticker-skill">Skill Name</span>
    <span class="ticker-level">XX%</span>
</div>
```

Or as plain text items separated by `•` or `·` dividers.

### Step 2: Audit what's there
List every skill currently in the ticker. Flag:
- Skills that feel outdated or generic (remove or update)
- Missing skills that Joshua uses regularly now
- Percentage levels that seem off

### Step 3: Update the list
Fresh skill categories to cover:
- **Strategy**: Brand Strategy, Connections Planning, Media Strategy, Cultural Insight, Campaign Architecture, Audience Intelligence
- **AI/Tools**: Claude Code, Google AI Studio, Prompt Engineering, AI Workflow Design, Gemini, ChatGPT, Cursor
- **Craft**: Creative Brief Writing, Comms Planning, Media Math, Brand Positioning, Competitive Analysis
- **Production**: Google Workspace, Slack, Figma (light), GitHub, Notion
- **Soft skills** (framed as outputs): Cross-Functional Leadership, Client Presentation, Storytelling

### Step 4: Set meaningful percentages
Use these as honest anchors:
- 95%+ = This is what Joshua does for a living, daily
- 80-94% = Strong, practiced regularly
- 65-79% = Solid, used frequently on projects
- 50-64% = Growing, used selectively

### Step 5: Rewrite the ticker HTML
Keep ticker items to 16-24 total — enough for a full loop with variety. Each item should show the skill name + level. Keep the existing CSS classes and structure exactly — only update the content.

Format example (adapt to whatever format is currently in the ticker):
```html
<span>Brand Strategy · 97%</span>
<span class="ticker-divider">◆</span>
<span>Claude Code · 88%</span>
<span class="ticker-divider">◆</span>
```

### Step 6: Commit
```bash
git add index.html
git commit -m "Update skills ticker — [month year] refresh"
```

Report: how many skills were updated/added/removed.
