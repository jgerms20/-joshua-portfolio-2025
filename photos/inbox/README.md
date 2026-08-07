# Photography inbox

Drop new `.jpg`, `.jpeg`, `.png`, or `.webp` photographs in this folder, then run:

```bash
python3 scripts/import-photography.py
```

The importer creates a metadata-stripped WebP in `photos/library/` and adds an unpublished draft to `data/photography.json`. It never publishes a photograph automatically.

Before publishing a draft:

1. Write specific alt text.
2. Set `chapter` to `people`, `places`, or `gatherings`.
3. Leave `sequence` as `null` for the archive, or assign a deliberate sequence position and layout.
4. Set `published` to `true`.
5. Run `python3 scripts/render-photography.py` and the test suite.

The original inbox file is retained so nothing is discarded implicitly.
