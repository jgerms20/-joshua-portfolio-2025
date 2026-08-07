from dataclasses import dataclass
from datetime import date, datetime, timedelta
import re
from typing import Callable, Protocol

from bs4 import BeautifulSoup
import requests

from portfolio_quality.model import Finding


@dataclass(frozen=True)
class PodcastLatest:
    number: int
    title: str
    episode_path: str
    date_label: str


class PodcastResponse(Protocol):
    status_code: int
    text: str


PodcastFetch = Callable[..., PodcastResponse]


def parse_spotify_latest(markup: str) -> PodcastLatest:
    soup = BeautifulSoup(markup, "lxml")
    block = soup.select_one('[data-testid="episode-0"]')
    if block is None:
        raise ValueError("Spotify latest episode block is missing")
    image = block.select_one('[data-testid="episode-block-image"] img[alt]')
    link = block.select_one('a[href^="/episode/"]')
    if image is None or link is None:
        raise ValueError("Spotify latest episode metadata is incomplete")

    title = str(image.get("alt", "")).strip()
    match = re.match(r"#(\d+)\s+", title)
    if not match:
        raise ValueError("Spotify latest episode title has no numeric marker")

    date_label = ""
    for paragraph in block.find_all("p"):
        candidate = paragraph.get_text(" ", strip=True)
        if candidate in {"Today", "Yesterday"} or re.fullmatch(
            r"[A-Z][a-z]{2} \d{1,2}(?:, \d{4})?", candidate
        ):
            date_label = candidate
            break
    if not date_label:
        raise ValueError("Spotify latest episode date is missing")

    return PodcastLatest(
        number=int(match.group(1)),
        title=title,
        episode_path=str(link.get("href")),
        date_label=date_label,
    )


def _episode_date(label: str, today: date) -> date:
    if label == "Today":
        return today
    if label == "Yesterday":
        return today - timedelta(days=1)
    for pattern in ("%b %d, %Y", "%b %d"):
        try:
            parsed = datetime.strptime(label, pattern).date()
        except ValueError:
            continue
        if pattern == "%b %d":
            parsed = parsed.replace(year=today.year)
            if parsed > today:
                parsed = parsed.replace(year=today.year - 1)
        return parsed
    raise ValueError(f"unsupported Spotify episode date: {label}")


def probe_podcast_entries(
    entries: list[dict[str, object]],
    fetch: PodcastFetch = requests.get,
    today: date | None = None,
) -> list[Finding]:
    checked_on = today or date.today()
    findings: list[Finding] = []
    for entry in entries:
        if entry.get("kind") != "spotify-show":
            continue
        try:
            response = fetch(
                str(entry["url"]),
                timeout=15,
                allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 PortfolioHealth/1.0"},
            )
        except requests.RequestException:
            findings.append(
                Finding(
                    severity="unverifiable",
                    code="podcast-feed-request-failed",
                    page=str(entry["page"]),
                    target=str(entry["url"]),
                    message="could not inspect the Spotify episode feed",
                )
            )
            continue
        if not 200 <= response.status_code < 400:
            continue
        try:
            latest = parse_spotify_latest(response.text)
            published = _episode_date(latest.date_label, checked_on)
        except ValueError as exc:
            findings.append(
                Finding(
                    severity="unverifiable",
                    code="podcast-marker-missing",
                    page=str(entry["page"]),
                    target=str(entry["url"]),
                    message=str(exc),
                )
            )
            continue

        minimum = int(entry.get("minimum_episode", 0))
        if latest.number < minimum:
            findings.append(
                Finding(
                    severity="broken",
                    code="podcast-feed-regressed",
                    page=str(entry["page"]),
                    target=str(entry["url"]),
                    message=f"latest episode #{latest.number:03d} is below expected #{minimum:03d}",
                )
            )
            continue

        maximum_age = int(entry.get("max_age_days", 14))
        age = (checked_on - published).days
        if age > maximum_age:
            findings.append(
                Finding(
                    severity="broken",
                    code="podcast-feed-stale",
                    page=str(entry["page"]),
                    target=str(entry["url"]),
                    message=f"latest episode is {age} days old; threshold is {maximum_age}",
                )
            )
    return findings
