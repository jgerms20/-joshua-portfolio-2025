# Photo Add — Add New Photos to Photography Grid

Adds newly dropped photos to the photography section in index.html.

## Usage
`/photo-add` — scans for new images and adds them to the grid.

Or specify a folder: `/photo-add "Images/Photography/new-batch/"`

## Instructions

### Step 1: Find new photos
Check for image files in:
- `Images/Photography/new-uploads/` (if it exists)
- Any folder the user specifies
- Or ask: "Which folder has your new photos?"

List files found.

### Step 2: Categorize each photo
For each image, ask (or infer from filename/folder):
- Category: `landscape`, `portrait`, `fashion`, `events`, `travel`
- Caption (optional)

If inferring — landscape photos are usually wide/horizontal, portraits have people, etc.

### Step 3: Generate HTML cards
For each photo, create a `.photo-item` card following the exact same structure as existing cards in the photography section. Include:
- `data-category="[category]"`
- `src` pointing to the image path
- `alt` text
- Lazy loading: `loading="lazy"`

### Step 4: Insert cards
Add new cards to the photography grid. New photos go at the TOP of the grid (most recent first).

### Step 5: Move files to permanent location
Move files from the upload folder to `Images/Photography/[category]/`

### Step 6: Commit
```bash
git add Images/Photography/ index.html
git commit -m "Add [N] new photos to photography grid"
git push -u origin claude/[current-branch]
```

### Photography System Setup
To make this really smooth, create this folder structure and drop photos there:
```
Images/Photography/
  ├── new-uploads/    ← drop new photos HERE
  ├── landscape/
  ├── portraits/
  ├── fashion/
  ├── events/
  └── travel/
```
Then run `/photo-add` and I'll handle the rest.
