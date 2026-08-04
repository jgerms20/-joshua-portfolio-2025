from dataclasses import dataclass
from datetime import date
from pathlib import Path
import unittest

from portfolio_quality.podcast_checks import parse_spotify_latest, probe_podcast_entries


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class FakeResponse:
    status_code: int
    text: str


def spotify_html(number=106, date_label="Today"):
    return f'''<div data-testid="episode-0">
        <div data-testid="episode-block-image"><img alt="#{number:03d} A current episode"></div>
        <a href="/episode/episode-id">Listen</a>
        <div><p>{date_label}</p><p data-testid="episode-progress-not-played"><span>38 min</span></p></div>
    </div>'''


def entry(**overrides):
    value = {
        "id": "eclectic-polymath-spotify",
        "page": "podcasts/podcast-eclectic-polymath.html",
        "kind": "spotify-show",
        "url": "https://open.spotify.com/show/example",
        "minimum_episode": 106,
        "max_age_days": 14,
    }
    value.update(overrides)
    return value


class PodcastFreshnessTests(unittest.TestCase):
    def test_parser_reads_latest_episode_number_title_link_and_date_label(self):
        latest = parse_spotify_latest(spotify_html())

        self.assertEqual(latest.number, 106)
        self.assertEqual(latest.title, "#106 A current episode")
        self.assertEqual(latest.episode_path, "/episode/episode-id")
        self.assertEqual(latest.date_label, "Today")

    def test_current_feed_returns_no_findings(self):
        findings = probe_podcast_entries(
            [entry()],
            fetch=lambda *_args, **_kwargs: FakeResponse(200, spotify_html()),
            today=date(2026, 8, 4),
        )

        self.assertEqual(findings, [])

    def test_regressed_episode_marker_is_broken(self):
        findings = probe_podcast_entries(
            [entry()],
            fetch=lambda *_args, **_kwargs: FakeResponse(200, spotify_html(number=105)),
            today=date(2026, 8, 4),
        )

        self.assertEqual(findings[0].severity, "broken")
        self.assertEqual(findings[0].code, "podcast-feed-regressed")

    def test_feed_older_than_threshold_is_broken(self):
        findings = probe_podcast_entries(
            [entry()],
            fetch=lambda *_args, **_kwargs: FakeResponse(200, spotify_html(date_label="Jul 1, 2026")),
            today=date(2026, 8, 4),
        )

        self.assertEqual(findings[0].severity, "broken")
        self.assertEqual(findings[0].code, "podcast-feed-stale")

    def test_eclectic_page_uses_live_language_without_fixed_episode_counts(self):
        page = (ROOT / "podcasts/podcast-eclectic-polymath.html").read_text(encoding="utf-8")

        self.assertIn("Live catalog", page)
        self.assertIn("Newest first", page)
        self.assertNotIn("56 Episodes", page)
        self.assertNotIn('id="ep-count">99', page)


if __name__ == "__main__":
    unittest.main()
