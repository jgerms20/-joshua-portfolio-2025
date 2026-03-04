# Add Award — Add a Recognition or Nomination

Adds an award, nomination, or recognition to the portfolio.

## Usage
`/add-award` then answer prompts.

## Instructions

### Step 1: Gather info
Ask for:
- **Award name**: e.g., "Effie Award", "4A's Jay Chiat Award"
- **Category**: e.g., "Best Multi-Platform Campaign"
- **Level**: Won / Finalist / Shortlisted / Nominated
- **Campaign**: Which campaign it was for
- **Year**: e.g., "2025"
- **Organization**: e.g., "Effie Worldwide"

### Step 2: Find the awards display
Look for an awards, recognition, or credentials section in `index.html`. If one exists, add to it. If not, check if there's a timeline or about section where it should go.

### Award badge format:
```html
<div class="award-item">
    <span class="award-level award-[won|finalist|shortlisted]">[Level]</span>
    <div class="award-details">
        <strong>[Award Name]</strong>
        <span>[Category] — [Campaign] ([Year])</span>
    </div>
</div>
```

### Step 3: Also check the relevant work page
If the award is for a specific campaign, add a badge to that campaign's `work/work-[brand].html` page as well.

### Step 4: Commit
```bash
git add index.html work/work-[brand].html
git commit -m "Add [Award Name] recognition for [Campaign]"
```
