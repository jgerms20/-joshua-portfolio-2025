# Photography Darkroom Implementation Plan

**Goal:** Replace the random photography masonry with an authored 21-frame story and a durable People, Places, and Gatherings archive, without redesigning the rest of the site.

## Design calibration

- **Subject:** Joshua's observational photography; the audience is creative directors and collaborators; the section's single job is to make the eye behind the strategy work unmistakable.
- **Color:** keep the existing Darkroom tokens—Carbon `#12100C`, Warm Paper `#F5F1E8`, Safelight `#E8380D`, Raised Black `#1B1813`, and soft Paper at 68% opacity.
- **Type:** retain Fraunces for editorial display, Space Grotesk for prose, and Space Mono for frame/chapter notation.
- **Layout:** one commanding opener, asymmetric diptychs, single-frame pauses, then a chapter archive that remains readable with JavaScript disabled.
- **Signature:** a restrained contact-sheet rhythm, with sequence numbers living in the margin instead of category labels laid over the image.

The first idea—a cleaner masonry grid—was rejected because it would still make the edit feel interchangeable and accidental. The authored sequence is specific to these photographs and spends the visual risk on pacing, not on new decoration.

## Task 1: Manifest and regression tests

- [x] Add `data/photography.json` with stable IDs, source paths, useful alt text, chapter, sequence order, and layout role.
- [x] Add tests for schema, unique IDs and sources, existing files, 18–24 contiguous sequence positions, chapter coverage, and generated markup.
- [x] Run the focused tests red before implementation.

## Task 2: Deterministic renderer

- [x] Add `portfolio_quality/photography.py` to validate the manifest and render the Darkroom markup.
- [x] Add `scripts/render-photography.py` to replace only the marked photography block in `index.html`.
- [x] Prove the renderer is idempotent.

## Task 3: Darkroom composition

- [x] Replace random masonry CSS with sequence, diptych, pause, and chapter-grid primitives.
- [x] Render a 21-frame selected sequence and three archive chapters.
- [x] Keep existing theme behavior and lightbox, and add keyboard-operable photo tiles and chapter controls.
- [x] Remove hard-coded camera-kit claims and replace them with an edit note grounded in the work.

## Task 4: Verification

- [x] Run focused and full tests.
- [x] Run static and live health checks.
- [x] Verify desktop and mobile layout, chapter controls, keyboard lightbox, and reduced-motion behavior in a browser.
- [x] Commit the completed phase without deploying.
