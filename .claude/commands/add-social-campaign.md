# Add Social Campaign — Add a Social Media or Content Work Sample

Adds a social media or content strategy campaign to the portfolio.

## Usage
`/add-social-campaign` then answer prompts.

## Instructions

### Step 1: Gather info
Ask for:
- **Brand/Client**: e.g., "Daily Gamecock", "Freelance client"
- **Platform(s)**: Instagram, TikTok, Twitter/X, LinkedIn, etc.
- **Campaign type**: Organic content, paid social, influencer, community management
- **Your role**: Content creator, strategist, community manager, etc.
- **Results**: Follower growth, engagement rate, reach, impressions, conversions
- **Time period**: e.g., "2023-2024"
- **Agency**: If applicable
- **2-3 sentence description**: What you did and why it mattered
- **Assets**: Any images, screenshots, or video paths available in `Brand Imagery/`

### Step 2: Decide placement
Social/content work can go:
1. As a new bento card in the Work section of `index.html`
2. As its own `work/work-[brand].html` case study (if there's enough depth)
3. Added to an existing brand's case study page

Ask the user which they prefer if unclear.

### Step 3: Create the content
Follow the same pattern as existing bento cards in the work grid.

### Step 4: Commit
```bash
git add index.html [work/work-brand.html if created]
git commit -m "Add [Brand] social campaign: [Campaign Type]"
```
