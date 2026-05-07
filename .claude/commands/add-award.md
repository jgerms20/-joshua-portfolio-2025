# Add Award — Add a Recognition or Nomination

Adds a verified award pill to a work card on the portfolio.

## Usage
`/add-award` — then provide details, or pass inline: `/add-award Levi's x Beyoncé | Clio Gold | Integrated Campaign | 2025`

## Step 1: Gather info (ask if not provided)
- **Campaign**: Which work card? (e.g., "Levi's x Beyoncé", "DoorDash")
- **Award name**: e.g., "Clio Award", "Cannes Lions", "D&AD"
- **Level**: Grand Prix / Grand / Gold / Silver / Bronze / Yellow Pencil / Merit / Shortlist / Nomination
- **Category**: e.g., "Integrated Campaign", "Casting"
- **Year**: e.g., "2025"

## Step 2: Choose the right pill class

| Level | Class | Color |
|-------|-------|-------|
| Grand Prix, Grand Clio | `award-grand` | Neon green |
| Gold, Yellow Pencil | `award-gold` | Gold |
| Multiple wins (e.g. "8× Lions") | `award-multi` | Orange |
| Silver, Bronze, Merit, Special | `award-merit` | Lavender |
| Shortlist, Nomination, Finalist | `award-shortlist` | Muted white |

## Step 3: Choose the right emoji

| Award show | Emoji |
|------------|-------|
| Cannes Lions | 🦁 |
| Clio Awards | 🏆 |
| D&AD | ✏️ |
| The One Club / One Show | 🔵 |
| Effie | 📊 |
| Shorty Awards | 🏅 |
| Other / Generic | ⭐ |

## Step 4: Add the pill to index.html

Find the matching bento card and add inside the `.award-pills` div (create it if missing):

```html
<div class="award-pills">
    <span class="award-pill award-grand">🏆 Clio Grand — 2025</span>
</div>
```

Place it **between** the `.bento-desc` paragraph and the `.bento-cta` span.

## Step 5: Also update the work page

Open `work/work-[brand].html` and add the same pill near the campaign header or result stats.

## Step 6: Commit and push

```bash
git add index.html work/work-[brand].html
git commit -m "Add [Award] recognition to [Campaign] card"
git push -u origin claude/test-memory-access-2Fh1b
```

## Current awards on each card

| Campaign | Awards |
|----------|--------|
| Levi's x Beyoncé REIIMAGINE | *(none yet — add when confirmed)* |
| DoorDash: All The Ads | 🏆 Cannes Titanium Grand Prix, ✏️ D&AD Yellow Pencil, 🦁 8× Cannes Lions |
| Driving While Black | 🏆 Clio Grand, 🏅 Shorty Award Winner, ⭐ D&AD Shortlisted |
| Samuel Adams: Brighter Boston | ⭐ Clio Shortlist |
| Xfinity: The Greatest Gift | 🎖️ The One Club Merit |
| Gatorade Campaigns | *(none yet)* |
