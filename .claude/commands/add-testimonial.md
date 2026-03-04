# Add Testimonial — Add a Recommendation or Quote

Adds a new testimonial or professional quote to the portfolio.

## Usage
`/add-testimonial` then answer prompts.

## Instructions

### Step 1: Gather info
Ask for:
- **Name**: Full name of the person
- **Title**: Their title and company
- **Quote**: The exact quote text
- **Context**: When/how they worked with Joshua (optional, for the card)
- **LinkedIn URL** (optional): For the card link

### Step 2: Find the testimonials section
Search `index.html` for `id="testimonials"` or similar. If no testimonials section exists, create one after the contact section.

### New testimonial card format:
```html
<div class="testimonial-card reveal">
    <blockquote class="testimonial-quote">
        "[Quote text]"
    </blockquote>
    <div class="testimonial-attribution">
        <strong>[Name]</strong>
        <span>[Title, Company]</span>
    </div>
</div>
```

### If creating a new section:
Use the dark glass card style consistent with the portfolio's design system. Add a nav link to the header dropdown.

### Step 3: Commit
```bash
git add index.html
git commit -m "Add testimonial from [Name] — [Company]"
```
