# Add Case Study — New Work Page

Creates a new campaign case study page from scratch.

## Usage
`/add-case-study` then answer the prompts.

## Instructions

### Step 1: Gather info
Ask for:
- **Brand**: e.g., "Nike"
- **Campaign name**: e.g., "Just Do It Relaunch"
- **Your role**: e.g., "Connections Strategist"
- **Agency**: e.g., "TBWA\Chiat\Day"
- **Year**: e.g., "2025"
- **Tag line** (optional): The campaign's main theme in 5-7 words
- **Key results** (3-5 metrics): e.g., "47M impressions, +22% brand lift, #1 recall"
- **Hero image path** (optional): Path to image in `Brand Imagery/`
- **2-3 sentence description**: What the campaign was about

### Step 2: Copy the template
Read `work/work-template.html` as your base.

### Step 3: Create the new page
Save as `work/work-[brand-lowercase].html` filling in all details.

### Step 4: Add to main navigation
In `index.html`, find the Work dropdown nav and add:
```html
<a href="work/work-[brand].html">[Brand] — [Campaign]</a>
```

### Step 5: Add a bento card to the work section
Find the work bento grid and add a new card with the brand's imagery and metrics.

### Step 6: Commit
```
git add work/work-[brand].html index.html
git commit -m "Add [Brand] case study: [Campaign Name]"
git push -u origin claude/[current-branch]
```
