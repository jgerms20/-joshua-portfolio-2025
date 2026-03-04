# Deploy — Commit, Push, Done

Commits all current changes and pushes to the feature branch.

## Instructions

You are deploying changes for the Joshua McKenzie German portfolio.

### Step 1: Check what's changed
```bash
git status
git diff --stat
```

### Step 2: Review the changes
Briefly read what's different. Make sure nothing looks accidental.

### Step 3: Stage and commit
Stage only the files that were intentionally changed:
```bash
git add [specific files]
git commit -m "[descriptive message]

https://claude.ai/code/session_01JxuDta5VUQ5NeC5EexMG8G"
```

Commit message format:
- Start with what changed (noun phrase): "Fix Gatorade hero image", "Add EP005 to Approachable AI"
- If multiple changes: short summary + bullet list in body
- Always append the session URL

### Step 4: Push
```bash
git push -u origin claude/portfolio-continuous-memory-g1Fi3
```

### Step 5: Remind
Tell the user:
> "Pushed to `claude/portfolio-continuous-memory-g1Fi3`. Go to GitHub and merge to `main` to deploy: yellow banner → Compare & pull request → Merge pull request. Live in ~2 minutes."

### If there's nothing to commit
Report that everything is clean and nothing needs deploying.
