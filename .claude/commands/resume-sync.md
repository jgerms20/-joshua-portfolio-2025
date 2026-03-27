# Resume Sync — Keep Portfolio and Resume Aligned

Audits the portfolio against Joshua's resume and flags gaps, inconsistencies, or things to add.

## Instructions

### Step 1: Read the portfolio
Scan `index.html` — specifically the about section, timeline, work section, and AI projects — to extract:
- All job titles and companies mentioned
- Date ranges on the timeline
- Campaign credits and role descriptions

### Step 2: Ask for the resume
Ask: "Can you paste your current resume text here, or share the path to your resume file?"

Read it in, or ask the user to paste key sections.

### Step 3: Compare and flag

**In portfolio but not resume:**
- Projects, campaigns, or roles that portfolio shows but resume doesn't mention
- AI builds or side projects that could strengthen the resume

**In resume but not portfolio:**
- Job roles or companies not reflected in portfolio timeline
- Campaigns on resume with no corresponding case study
- Skills, certifications, or education that could add credibility to portfolio

**Inconsistencies:**
- Date ranges that differ between portfolio and resume
- Title differences (same role called different things)
- Results claims that differ

### Step 4: Output
```
## RESUME SYNC — [date]

### In portfolio, missing from resume
[List with suggestions on how to add]

### In resume, missing from portfolio
[List with suggestions on what to build out]

### Inconsistencies
[List with recommended resolution]

### Alignment score: [X/10]
```

Ask: "Want me to draft resume bullet updates for any of these?"
