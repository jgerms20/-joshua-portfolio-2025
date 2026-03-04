# Timeline Update — Update the Career Journey Timeline

Adds a new entry to the career/journey timeline section.

## Usage
`/timeline-update` then answer prompts.

## Instructions

### Step 1: Gather info
Ask for:
- **Year/date**: e.g., "2025" or "Spring 2025"
- **Title**: Role or milestone name, e.g., "Senior Connections Strategist"
- **Organization**: Company/agency/school name
- **Location**: City, State (for the state SVG map)
- **State**: Two-letter abbreviation (e.g., CA, NY, SC) — for the SVG map
- **City**: City name for the glowing star label
- **2-3 sentence description**: What you did and why it matters

### Step 2: Find the timeline
Look for `class="jtl-wrap"` or `id="journey"` in `index.html`.

### Step 3: Determine position
- New entries go at the top (most recent)
- Alternate left/right positioning — check the last entry's side

### Step 4: Create the timeline row
```html
<div class="jtl-row jtl-row-[left|right] reveal">
    [card div] [mid div with dot] [state SVG or empty div]
</div>
```

For the state SVG: add simplified SVG path for the specified state, with a pulsing city star. Use existing state SVGs in the file as templates.

### Step 5: Commit
```bash
git add index.html
git commit -m "Add [Year] [Role] at [Company] to journey timeline"
```
