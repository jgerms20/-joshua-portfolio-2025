# Add AI Project — AI Projects Grid

Adds a new project card to the AI Projects grid in index.html.

## Usage
`/add-ai-project` then answer the prompts, or provide all details upfront:
`/add-ai-project "Project Name" "tag" "description" "url" google|claude [status]`

## Instructions

You are adding a card to the `.ai-projects-grid` in `/home/user/-joshua-portfolio-2026/index.html`.

### Step 1: Gather info (if not provided)
- **Project name**: Display name
- **Tag**: Short category label (e.g., "Media Intelligence", "Productivity")
- **Description**: 1-2 sentences about what it does
- **URL**: Link to the app (or empty string if not yet deployed)
- **Platform**: `google` (Google AI Studio) or `claude` (Claude Code)
- **Status badge**: Optional — "In Progress", "Active", "Beta", "Live" (leave empty if none)

### Step 2: Choose a gradient
Pick a gradient that fits the project's vibe from this palette or invent one:
- Focus/calm: `linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)`
- Energy/action: `linear-gradient(135deg, #FFB700 0%, #FF8C00 100%)`
- Creative: `linear-gradient(135deg, #8A2BE2 0%, #4B0082 100%)`
- Nature/growth: `linear-gradient(135deg, #1DB954 0%, #191414 100%)`
- Warmth: `radial-gradient(circle at top right, #FF6B6B 0%, #FFA500 100%)`

### Step 3: Add the card
Insert the new `.ai-grid-item` at the appropriate position in the grid:
- Google AI Studio projects first (in order of creation)
- Claude Code projects at the end

Follow the exact same HTML structure as existing cards. Include the `ai-platform-badge` div.

### Step 4: Commit
```
git add index.html
git commit -m "Add AI project: [Project Name]"
git push -u origin claude/[current-branch]
```
