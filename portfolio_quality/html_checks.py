from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError

from portfolio_quality.model import Finding


BROKEN_CODES = {
    "blank-source",
    "missing-local-file",
    "unreadable-image",
    "duplicate-id",
    "missing-fragment",
    "placeholder-media",
}

IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
EXTERNAL_SCHEMES = {"data", "http", "https", "javascript", "mailto", "tel"}
PLACEHOLDER_PHRASES = ("video coming soon", "placeholder")


def _finding(code: str, page: Path, root: Path, target: str, message: str) -> Finding:
    severity = "broken" if code in BROKEN_CODES else "degraded"
    return Finding(
        severity=severity,
        code=code,
        page=page.relative_to(root).as_posix(),
        target=target,
        message=message,
    )


def _local_path(root: Path, page: Path, target: str) -> Path | None:
    if target.startswith("//"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme.lower() in EXTERNAL_SCHEMES:
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    if path_text.startswith("/"):
        return root / path_text.lstrip("/")
    return page.parent / path_text


def _image_decodes(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            width, height = image.size
            image.verify()
        return width > 0 and height > 0
    except (OSError, UnidentifiedImageError):
        return False


def check_page(root: Path, page: Path) -> list[Finding]:
    root = Path(root)
    page = Path(page)
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "lxml")
    findings: list[Finding] = []

    for image in soup.find_all("img"):
        if not image.has_attr("alt"):
            findings.append(
                _finding("missing-alt", page, root, image.get("src", ""), "image has no alt attribute")
            )

    for iframe in soup.find_all("iframe"):
        if not str(iframe.get("title", "")).strip():
            findings.append(
                _finding(
                    "missing-iframe-title",
                    page,
                    root,
                    iframe.get("src", ""),
                    "iframe has no descriptive title",
                )
            )

    ids = [str(tag["id"]) for tag in soup.find_all(attrs={"id": True})]
    for identifier, count in Counter(ids).items():
        if count > 1:
            findings.append(
                _finding(
                    "duplicate-id",
                    page,
                    root,
                    f"#{identifier}",
                    f"id appears {count} times",
                )
            )

    known_ids = set(ids)
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"]).strip()
        if href.startswith("#") and len(href) > 1 and unquote(href[1:]) not in known_ids:
            findings.append(
                _finding("missing-fragment", page, root, href, "fragment target does not exist")
            )

    text = soup.get_text(" ", strip=True).lower()
    for phrase in PLACEHOLDER_PHRASES:
        if phrase in text:
            findings.append(
                _finding("placeholder-media", page, root, phrase, "placeholder media copy is public")
            )

    for tag in soup.find_all(True):
        attributes = ["src", "poster"]
        if tag.name in {"a", "link"}:
            attributes.append("href")
        for attribute in attributes:
            if not tag.has_attr(attribute):
                continue
            target = str(tag.get(attribute, "")).strip()
            if attribute in {"src", "poster"} and not target:
                findings.append(
                    _finding("blank-source", page, root, target, f"{tag.name} has a blank {attribute}")
                )
                continue
            if "placeholder" in target.lower():
                findings.append(
                    _finding("placeholder-media", page, root, target, "media URL contains placeholder")
                )
            local_path = _local_path(root, page, target)
            if local_path is None:
                continue
            if not local_path.exists():
                findings.append(
                    _finding("missing-local-file", page, root, target, "referenced local file does not exist")
                )
                continue
            if tag.name == "img" and local_path.suffix.lower() in IMAGE_SUFFIXES and not _image_decodes(local_path):
                findings.append(
                    _finding("unreadable-image", page, root, target, "image cannot be decoded")
                )

    return findings
