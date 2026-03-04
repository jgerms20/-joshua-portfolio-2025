# GitHub Sync — Commit, Push, and Sync Status

Reviews current changes, commits with a smart message, pushes to the feature branch, and confirms sync status.

## Instructions

### Step 1: Check git status
```bash
git status
git diff --stat
```

### Step 2: Summarize what changed
Read the diff and write a concise, descriptive commit message that explains *why* these changes were made, not just what files changed.

Commit message format:
- First line: noun phrase, ≤72 chars (e.g. "Fix DIRECTV image paths and recover missing sections")
- Body (if multiple changes): bullet list of changes
- Always append the session URL on the last line

### Step 3: Stage and commit
Stage only intentionally changed files:
```bash
git add [specific files]
git commit -m "[message]

https://claude.ai/code/session_01JxuDta5VUQ5NeC5EexMG8G"
```

### Step 4: Push
```bash
git push -u origin claude/portfolio-continuous-memory-g1Fi3
```

### Step 5: Verify sync
```bash
git log --oneline -5
git status
```

Report back:
- How many commits ahead of origin
- Whether the push succeeded
- Direct link to compare on GitHub for opening a PR

### Step 6: Remind the user
> "Pushed to `claude/portfolio-continuous-memory-g1Fi3`. To go live: GitHub → yellow banner → Compare & pull request → Merge pull request. Live in ~2 minutes."

### If there's nothing to commit
Report that everything is already in sync — no action needed.
