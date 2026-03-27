# Dark Mode Toggle — Add Light/Dark Mode Support

Adds a light mode version of the portfolio with a toggle, respecting system preference.

## Instructions

### Step 1: Audit current color usage
Read `index.html` — identify all CSS custom properties (variables) in `:root`. The portfolio currently uses:
- `--bg: #0a0a0a` (near-black background)
- `--surface: #111111`
- `--neon: #d4ff4f` (lime green accent)
- `--text-primary: #f5f5f5`
- `--text-muted: #8a8a8a`

### Step 2: Define light mode values
Create a `[data-theme="light"]` block with light equivalents:
```css
[data-theme="light"] {
    --bg: #f8f8f4;
    --surface: #ffffff;
    --neon: #6b8f00;  /* darker lime for light bg contrast */
    --text-primary: #0a0a0a;
    --text-muted: #555555;
    --glass: rgba(0,0,0,0.04);
    --glass-border: rgba(0,0,0,0.08);
}
```

### Step 3: Add system preference detection
```css
@media (prefers-color-scheme: light) {
    :root { /* light values here too */ }
}
```

### Step 4: Add toggle button to nav
A sun/moon icon toggle in the header — small, accessible, saves preference to `localStorage`.

```js
const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
});
```

### Step 5: Test and commit
Verify the toggle works, key sections look good in light mode. Commit:
```bash
git add index.html
git commit -m "Add light/dark mode toggle with system preference detection"
```
