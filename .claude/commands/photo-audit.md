# Photo Audit — Review Photography Section Quality

Reviews the photography grid for quality, diversity, organization, and missing images.

## Instructions

### Step 1: Inventory what's in the grid
Read `index.html` and find the photography section. Extract:
- All image paths referenced
- How many photos are in each category (if categorized)
- Any photos with empty or missing `alt` text

### Step 2: Check file existence
```bash
find "Images/Photos of Self" "Images/" -type f -name "*.jpg" -o -name "*.JPG" -o -name "*.png" | sort
```

Compare against what's referenced in HTML.

### Step 3: Flag issues
- Images in HTML that don't exist on disk
- Images on disk that aren't in the grid (potential additions)
- Very large file sizes (over 2MB) that should be compressed
- Missing alt text on photos

### Step 4: Suggest curation improvements
- Are all 4 categories represented? (Portrait, Street, Landscape, Abstract or similar)
- Is there a good mix of featured (large) and standard grid photos?
- Are the self-portraits current? (Check file dates)

### Step 5: Report
```
## PHOTO AUDIT — [date]

### Missing from disk (broken): [X]
### On disk but not shown: [X files, here are the best candidates to add]
### Alt text gaps: [X]
### Suggested grid improvements: [list]
```

Ask: "Want me to add the best missing photos now? Run /photo-add."
