#!/usr/bin/env python3
"""Static marketing page checks. No network, dependencies or deployment required."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent
PAGES = {
    "/": ROOT / "index.html",
    "/auth/": ROOT / "auth" / "index.html",
    "/billing/": ROOT / "billing" / "index.html",
    "/analytics/": ROOT / "analytics" / "index.html",
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
        self.og_images: list[str] = []
        self.stylesheets: list[str] = []

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
            if attrs.get("rel") == "stylesheet":
                self.stylesheets.append(attrs.get("href", ""))
            if attrs.get("rel") == "canonical":
                self.canonical.append(attrs.get("href", ""))
            if attrs.get("href", "").startswith("/"):
                self.links.append(("asset", attrs["href"]))
        if tag == "meta" and attrs.get("property") == "og:url":
            self.og_urls.append(attrs.get("content", ""))
        if tag == "meta" and attrs.get("property") == "og:image":
            self.og_images.append(attrs.get("content", ""))


def local_target(path: str) -> Path:
    if path == "/":
        return ROOT / "index.html"
    path = ROOT / path.lstrip("/")
    return path / "index.html" if path.is_dir() else path


def redirect_target(path: str) -> Path | None:
    """Resolve a Cloudflare Pages redirect to an existing local marketing page."""
    for line in (ROOT / "_redirects").read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[0] == path and fields[2] == "301":
            target = local_target(fields[1])
            return target if target.is_file() else None
    return None


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
    expected_css = {"/assets/base.css"}
    expected_css.add("/assets/home.css" if route == "/" else "/assets/platform.css")
    if route == "/analytics/":
        expected_css.add("/assets/analytics.css")
    loaded_css = {urlsplit(ref).path for ref in page.stylesheets}
    if not expected_css.issubset(loaded_css):
        errors.append(f"{route}: missing required stylesheet(s): {expected_css - loaded_css}")
    for ref in page.og_images:
        parsed = urlsplit(ref)
        if parsed.netloc == "olaryn.com" and not local_target(parsed.path).is_file():
            errors.append(f"{route}: social image missing: {ref}")
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
        if not file.is_file() and not (kind == "anchor" and redirect_target(target.path)):
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
    # The homepage keeps its original simple layout, headline, copy and product
    # link labels; the logo mark is drawn in the theme's ink colour.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for route, label in (("/auth/", "Zikela: identity"),
                         ("/billing/", "Bilyra: credits &amp; usage"),
                         ("/analytics/", "Yeleva: analytics")):
        if f'href="{route}"' not in home or label not in home:
            errors.append(f"home: missing product link {label} at {route}")
    if '<svg class="mark"' not in home or '/assets/marks.svg#olaryn' not in home:
        errors.append("home: the Olaryn mark must render from /assets/marks.svg#olaryn (follows the theme)")
    for route, html in PAGES.items():
        content = html.read_text(encoding="utf-8")
        if route != "/" and any(old in content for old in ("Authward", "Tallyward", "/authward/")):
            errors.append(f"{route}: stale marketing brand or URL")
    redirects = (ROOT / "_redirects").read_text(encoding="utf-8")
    for legacy, current in (("/authward/", "/auth/"), ("/zikela/", "/auth/"), ("/bilyra/", "/billing/"), ("/yeleva/", "/analytics/")):
        if f"{legacy} {current} 301" not in redirects:
            errors.append(f"redirects: {legacy} must redirect to {current}")
    if errors:
        print("\n".join(f"FAIL: {e}" for e in errors))
        raise SystemExit(1)
    print(f"PASS: {len(PAGES)} pages; SEO, anchors, local assets and sitemap verified")


if __name__ == "__main__":
    main()
