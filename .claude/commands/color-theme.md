# Color Theme — Try a New Color Palette

Swaps the portfolio accent color (currently neon lime `#d4ff4f`) for a new palette — preview and optionally commit.

## Usage
`/color-theme [color]` — e.g. `/color-theme electric-blue` or `/color-theme warm-gold`

## Instructions

### Step 1: Parse the desired color
If color specified, match to a palette:

| Input | Accent | Glow |
|-------|--------|------|
| `electric-blue` | `#4f9fff` | `rgba(79,159,255,0.2)` |
| `warm-gold` | `#ffcc4f` | `rgba(255,204,79,0.2)` |
| `hot-pink` | `#ff4fa8` | `rgba(255,79,168,0.2)` |
| `cyber-orange` | `#ff6b4f` | `rgba(255,107,79,0.2)` |
| `arctic-teal` | `#4fffda` | `rgba(79,255,218,0.2)` |
| `lavender` | `#b44fff` | `rgba(180,79,255,0.2)` |

If no color specified, show the options and ask.

### Step 2: Apply the theme
In `index.html`, find `:root` and update:
```css
--neon: [new-accent];
--neon-glow: [new-glow];
```

Also update anywhere `#d4ff4f` or `#D4FF4F` is hardcoded (not using the variable).

### Step 3: Preview
Tell the user: "Open index.html in browser to preview the [color] theme."

### Step 4: Confirm or revert
Ask: "Keep this color? If not, run `/color-theme neon-lime` to revert to original."

### To revert to original:
`--neon: #d4ff4f; --neon-glow: rgba(212,255,79,0.2);`

### Step 5: Commit if keeping
```bash
git add index.html
git commit -m "Switch accent color to [color-name]"
```
