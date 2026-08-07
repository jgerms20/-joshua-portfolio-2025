# Portfolio Editorial, Media, and Photography Overhaul

**Date:** August 4, 2026
**Status:** Approved design awaiting written-spec review
**Repository:** `jgerms20/-joshua-portfolio-2026`
**Implementation branch:** `codex/portfolio-editorial-media-overhaul`

## Objective

Make Joshua's existing portfolio more trustworthy, current, and distinctly human without redesigning the site.

The visual system, navigation, typography, page structure, and case-study identity remain intact. The only substantial visual change is the Photography/Darkroom section, which will combine a story-led sequence with chapter-based browsing. Everywhere else, changes are surgical: rewrite weak copy, repair or replace broken media, correct project credits, verify awards, improve the Eclectic Polymath page, and install scheduled checks that fail when the production site is materially broken.

## Design Decision

The approved photography direction is **Story-led Darkroom with Project Chapters**:

- Preserve the current black Darkroom palette and its separation from the paper-like main site.
- Lead with one curated sequence of the strongest 18–24 photographs.
- Use large opening frames, asymmetric pairs, pauses, and generous negative space.
- Follow the sequence with a browsable archive organized into **People**, **Places**, and **Gatherings**.
- Draw on João Falcão's editorial spacing and image sequencing and Náthalyn Araújo's confidence in full-frame images, without copying either portfolio's layout or visual identity.
- Keep the rest of Joshua's portfolio visually recognizable.

## Scope

### 1. Photography and the Darkroom

The Photography section receives the only structural visual redesign.

#### Selected sequence

The opening sequence will use 18–24 existing photographs chosen after a contact-sheet review. The sequence will mix portrait, fashion, landscape, travel, and event work instead of acting as another category grid. It will use:

- one large opening photograph;
- alternating full-width images, asymmetric pairs, and deliberate blank space;
- minimal labels limited to sequence position, location or year when known, and accessible alternative text;
- native aspect ratios whenever practical rather than uniform crops;
- responsive images and lazy loading after the opening frame;
- reduced-motion behavior and keyboard-accessible image viewing.

#### Project chapters

The archive below the selected sequence will map current folders into three visitor-facing chapters:

- **People:** `photos/portraits/` and `photos/fashion/`
- **Places:** `photos/landscape/` and `photos/travel/`
- **Gatherings:** `photos/events/`

Self-portraits remain available for About-page use and are not automatically added to the public Darkroom archive. Chapter controls must work with keyboard input, expose an active state to assistive technology, and degrade to a readable grouped archive if JavaScript fails.

#### Photo source of truth

Create `data/photography.json` as the public manifest. Each entry contains:

- stable ID;
- source and generated image paths;
- alt text;
- chapter;
- optional location and year;
- selected-sequence order or `null`;
- archive order;
- publication state: `draft` or `published`;
- image dimensions and checksum.

The page is generated from the manifest between explicit HTML markers. Published images render into `index.html`; draft images never render publicly.

#### Photo drop workflow

Create `photos/inbox/` as Joshua's local drop location. The folder contains instructions but ignores dropped image binaries in Git. `scripts/photo-pipeline.py` will:

1. scan inbox files without deleting or moving originals;
2. reject unsupported or unreadable formats with a clear report;
3. detect exact duplicates by checksum;
4. normalize orientation;
5. remove embedded metadata from generated public copies;
6. produce a display image and thumbnail in a controlled output folder;
7. append new entries to the manifest as `draft`;
8. require an explicit manifest change to `published` before rendering.

This workflow makes adding photographs repeatable without turning the static portfolio into an unauthenticated upload service.

### 2. Full-site editorial pass

Rewrite visitor-facing copy across the production site, including:

- homepage hero, About, section introductions, contact copy, labels, and footer;
- every campaign case study;
- podcast overview and individual podcast pages;
- AI/project cards and tool credits;
- Culture and media-diet pages;
- empty states, calls to action, image captions, and other microcopy.

Archived, milestone, concept, and experimental HTML files are excluded from the editorial pass and from production health checks.

The editorial standard applies the high-level craft principles Joshua identified in Stephen King's *On Writing* without imitating King's voice:

- prefer active voice;
- choose concrete nouns and precise verbs;
- remove filler, inflated claims, repeated ideas, and unnecessary adverbs;
- put evidence before adjectives;
- vary sentence length for natural rhythm;
- keep paragraphs short enough to scan;
- state Joshua's role, decision, and outcome plainly;
- preserve personality, humor, and uncertainty where honest.

The Beyoncé/Levi's case study is the internal benchmark for proportion and clarity. The Gatorade case study will be cut substantially, and jargon-heavy pages such as Xfinity will be rewritten from evidence rather than polished abstractions. The About section will remove its repeated opening idea and tell one clean arc: South Carolina and journalism, strategy and culture, AI building, Los Angeles, photography, and audio work.

No claim, result, award, client relationship, or personal biography detail may be invented to make copy stronger. Unsupported material is removed or marked for Joshua's confirmation.

### 3. Campaign media and awards

Create `data/media-manifest.json` as the inventory for production-facing images, videos, external embeds, awards, and source links. Records include the owning page, asset type, local or external URL, public fallback, last verified date, status, and evidence URL when the record supports an award or result.

Known failures to resolve include:

- broken Letterboxd and Spotify artwork;
- missing DIRECTV and Xfinity YouTube videos;
- missing Sephora YouTube thumbnails;
- fragile or hotlink-blocked Goodreads, Gatorade, and Sam Adams assets;
- blank image sources and "Video Coming Soon" placeholders.

Critical campaign images and owned video files should be served locally when the repository already contains a usable asset and Joshua has the right to display it. External video embeds must use a verified public ID, include a descriptive iframe title, and provide a poster and direct-link fallback. If no valid public video can be verified, the page will show honest still imagery and concise context rather than a dead player or invented replacement.

Awards require an official award-gallery, agency, brand, or trade-source URL. The initial award update includes Gatorade's **2026 Clio Bronze** for *No Ordinary Athlete* in Branded Entertainment & Content, Partnerships/Co-Creation, verified on the official Clio winners gallery. Automated checks may flag stale or changed source pages, but they may not publish new awards without human review.

### 4. AI project attribution

Rename the current "Claude Code Builds" concept to **AI Builds** while retaining per-project tool credits.

Correct these verified credits:

- Gen Alpha Intelligence Lab — Codex
- Dreamcatcher — Codex
- Meme Library — Codex

Other tool labels remain unchanged unless repository or project evidence supports a correction. The update script must render projects by their actual category and tool fields instead of forcing every project into a Claude-specific section.

### 5. Eclectic Polymath and podcast freshness

Improve `podcasts/podcast-eclectic-polymath.html` within its existing dark-and-gold visual identity.

The page will include:

- working square show artwork;
- a shorter, specific show introduction;
- an accessible Spotify show embed with a non-empty title;
- a clearly labeled latest-episodes area supplied by the live platform embed rather than hand-entered cards;
- direct listening links;
- a compact topic map showing the show's range;
- no hard-coded episode total or "always current" claim.

Spotify currently identifies the show as `3dlagzJ0jiWLTB9mF3y069`. The platform page exposed episode #105 during the August 4, 2026 verification, while the portfolio was publishing stale counts. The portfolio will use the live Spotify embed as the visitor-facing episode source.

The scheduled checker will verify that:

- the Spotify show page and embed return successfully;
- the show title and at least one episode marker are present;
- the latest observed episode marker is not lower than the stored marker;
- the artwork resolves;
- the portfolio page contains the correct show ID and no static episode-count claim.

If Spotify changes its public markup, the checker fails with a source-format error rather than reporting false freshness. A failed freshness check does not remove the working embed or overwrite public copy.

The same source registry will cover the other podcast pages. Shows with no reliable episode feed keep a working platform embed and direct link; they do not make automated freshness claims.

### 6. Scheduled health checks

Replace the current date-touching workflow with checks that measure real production behavior.

#### Pull-request and push checks

Run against production HTML only:

- referenced local files exist with correct case;
- image files decode and have nonzero dimensions;
- no blank, placeholder, or "coming soon" media sources remain;
- internal links resolve;
- production HTML parses without duplicate IDs or critical structural errors;
- images have alt text and iframes have titles;
- photography manifest entries resolve and only `published` entries render;
- AI labels match the project manifest;
- tests for parsers, renderers, and health-check classifications pass.

Critical failures exit nonzero and block the workflow.

#### Scheduled checks

Run Monday and Friday against both repository files and `https://joshuamgerman.com/`:

- production pages return successful responses;
- local images render from the deployed URL;
- YouTube videos pass the public oEmbed check or their configured fallback resolves;
- Spotify show and embed checks pass;
- external links used as primary calls to action remain reachable;
- award evidence links remain reachable;
- the deployed homepage contains the expected release marker.

Network checks use timeouts, bounded retries, and a distinction between `broken`, `degraded`, and `unverifiable`. A single rate limit does not rewrite content. Broken production-critical assets fail the job; degraded or unverifiable third-party services produce a warning with the exact page and fallback status.

The workflow writes a readable GitHub Actions summary and a machine-readable JSON artifact. It does not commit a new date when content did not change.

#### Post-deployment smoke check

After GitHub Pages reports a successful deployment, run a bounded smoke check against the public alias. Verify the homepage, each campaign page, each podcast page, the Darkroom assets, and the expected release marker. A green deploy job without a successful public smoke check is not considered a verified release.

### 7. Accessibility and resilience

All retained and changed pages must preserve the existing theme behavior and visible theme control. Targeted fixes include:

- meaningful alt text for editorial images;
- empty alt text only for genuinely decorative assets;
- descriptive iframe titles;
- keyboard-operable chapter filters and image viewer;
- visible focus states;
- reduced-motion handling;
- no content that requires hover;
- fallback links for third-party players;
- readable layouts at 360px, 768px, and desktop widths.

### 8. Testing strategy

New behavior will be developed test-first.

Automated tests cover:

- photography manifest schema and draft/published behavior;
- duplicate photo detection, format rejection, orientation, and metadata removal;
- deterministic Darkroom rendering;
- production-page discovery that excludes archives and milestones;
- local reference resolution and filename case;
- media status classification and fallback handling;
- YouTube ID and oEmbed validation using recorded fixtures;
- Spotify episode-marker parsing using recorded fixtures;
- failure on regressing or missing episode markers;
- failure on empty iframe titles and blank sources;
- AI tool-credit rendering;
- no-op update runs leaving Git clean.

Manual verification covers:

- visual comparison against the current site to confirm no unintended redesign;
- Darkroom sequencing on desktop and mobile;
- keyboard and reduced-motion behavior;
- real image and video playback;
- Spotify embed behavior;
- the public GitHub Pages alias after deployment.

## Delivery boundaries

- Work occurs in the isolated `codex/portfolio-editorial-media-overhaul` branch.
- Joshua's existing dirty checkout is not modified.
- No deployment, merge, public publication, automated outreach, or external account change occurs without Joshua's explicit approval.
- Research may update local drafts and manifests; unsupported claims never publish automatically.
- The build may be delivered in verified phases, but each phase must leave production pages coherent and testable.

## Implementation phases

This umbrella design spans several independent systems. Each phase below receives its own implementation plan, test cycle, and review checkpoint. Plans run in order because later editorial and visual work depends on the media registry and reliability foundation established first.

1. **Reliability foundation:** production-page registry, manifests, tests, and strict health checker.
2. **Media repair:** local assets, verified embeds, fallbacks, accessibility labels, and award evidence.
3. **Podcast freshness:** Eclectic Polymath repair, live embed treatment, and scheduled verification.
4. **Photography:** contact-sheet selection, selected sequence, chapters, manifest rendering, and inbox pipeline.
5. **Editorial:** full production-site rewrite and AI attribution corrections.
6. **Release verification:** responsive/browser QA, scheduled workflow validation, and public smoke-check readiness.

## Acceptance criteria

The work is ready for publication only when:

- the current visual identity is preserved outside Photography;
- the Darkroom contains the approved story-led sequence and chapter archive;
- every production image, video, and embed is either working or has an honest working fallback;
- Eclectic Polymath has working artwork, a live Spotify episode surface, and no stale count;
- verified AI projects credit Codex correctly;
- the Gatorade Clio Bronze and any other added award have official evidence links;
- the full production site has completed the editorial pass;
- local tests and health checks pass;
- the scheduled workflow fails on critical breakage and does not create date-only commits;
- the deployment smoke check can verify the real public alias.

## References

- João Falcão, Work: https://joaofalcao.art/work
- Náthalyn Araújo, Work: https://nathalynaraujo.com/work
- Spotify, The Eclectic Polymath Podcast: https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069
- Clio Awards, Gatorade — *No Ordinary Athlete*: https://clios.com/winners-gallery/details/220718
