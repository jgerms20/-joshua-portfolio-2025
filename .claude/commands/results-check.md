# Results Check — Audit and Strengthen Campaign Metrics

Finds every campaign result claim in the portfolio and flags missing, vague, or unverified metrics.

## Instructions

### Step 1: Scan for metrics
Search all files for numbers and result claims:
```bash
grep -n "%" work/*.html index.html
grep -n "lift\|impressions\|recall\|reach\|awareness\|consideration\|revenue" work/*.html index.html
```

### Step 2: Evaluate each claim
For each metric found, assess:
- **Specific enough?** "47M impressions" ✓ vs "significant reach" ✗
- **Attributed properly?** Is it clear whose campaign and which period?
- **Missing results?** Campaigns with no metrics mentioned at all
- **Verifiable?** Can Joshua back this up if asked in an interview?

### Step 3: Flag gaps
List campaigns that have no results at all — these are weak spots a recruiter will notice.

### Step 4: Suggest improvements
For campaigns with missing metrics, suggest:
- What metrics are typically trackable for this type of campaign
- How to frame qualitative wins ("Led the first X", "Nominated for Y", "Featured in Z")
- Placeholder language if no data is available yet

### Output format:
```
## RESULTS CHECK — [date]

### ✅ Strong metrics
- [file]:[campaign] — [metric] — clear and specific

### 🟡 Vague claims
- [file]:[campaign] — [claim] — recommendation to sharpen

### 🔴 Missing results entirely
- [file]:[campaign] — no metrics found

### Suggested additions
[Specific copy improvements for weak spots]
```
