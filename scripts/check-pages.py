#!/usr/bin/env python3
"""Static marketing page checks. No network, dependencies or deployment required."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "/": ROOT / "index.html",
    "/authward/": ROOT / "authward" / "index.html",
    "/billing/": ROOT / "billing" / "index.html",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.h1 = 0
        self.titles = 0
        self.canonical: list[str] = []
        self.og_urls: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.titles += 1
        for kind, attr in (("anchor", "href"), ("image", "src")):
            if tag == ("a" if kind == "anchor" else "img") and attr in attrs:
                self.links.append((kind, attrs[attr]))
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical.append(attrs.get("href", ""))
            if attrs.get("href", "").startswith("/"):
                self.links.append(("asset", attrs["href"]))
        if tag == "meta" and attrs.get("property") == "og:url":
            self.og_urls.append(attrs.get("content", ""))


def local_target(path: str) -> Path:
    if path == "/":
        return ROOT / "index.html"
    path = ROOT / path.lstrip("/")
    return path / "index.html" if path.is_dir() else path


def check_page(route: str, html: Path) -> list[str]:
    errors = []
    page = Page()
    page.feed(html.read_text(encoding="utf-8"))
    wanted = f"https://olaryn.com{route}"
    if page.h1 != 1:
        errors.append(f"{route}: expected exactly one h1, got {page.h1}")
    if page.titles != 1:
        errors.append(f"{route}: expected exactly one title")
    if page.canonical != [wanted]:
        errors.append(f"{route}: incorrect canonical: {page.canonical}")
    if page.og_urls != [wanted]:
        errors.append(f"{route}: incorrect og:url: {page.og_urls}")
    if len(page.ids) != len(set(page.ids)):
        errors.append(f"{route}: duplicate HTML ids")
    for kind, ref in page.links:
        target = urlsplit(ref)
        if target.scheme or target.netloc or ref.startswith("mailto:"):
            continue
        if target.path.startswith("/"):
            file = local_target(target.path)
        elif target.path:
            file = local_target(route + target.path)
        else:
            file = html
        if not file.is_file():
            errors.append(f"{route}: missing {kind}: {ref}")
        if target.fragment and target.path in ("", route):
            if target.fragment not in page.ids:
                errors.append(f"{route}: missing target: {ref}")
    return errors


def main() -> None:
    errors = []
    for route, html in PAGES.items():
        errors += check_page(route, html)
    sitemap = ElementTree.parse(ROOT / "sitemap.xml")
    urls = {item.text for item in sitemap.findall(".//{*}loc")}
    wanted = {f"https://olaryn.com{route}" for route in PAGES}
    if urls != wanted:
        errors.append(f"sitemap: expected {sorted(wanted)}, got {sorted(urls)}")
    if errors:
        print("\n".join(f"FAIL: {e}" for e in errors))
        raise SystemExit(1)
    print(f"PASS: {len(PAGES)} pages; SEO, anchors, local assets and sitemap verified")


if __name__ == "__main__":
    main()
