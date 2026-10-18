#!/usr/bin/env python3
"""Prevent unsolicited design changes; see AGENTS.md.

No automatic baseline update flag: only update design-lock.json after explicit
owner approval. Text-only edits are allowed if the visual DOM stays the same.
"""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class BodyLayout(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.body = False
        self.layout = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = True
        if not self.body:
            return
        props = dict(attrs)
        self.layout.append(["+", tag, props.get("class", ""), props.get("id", "")])
        if tag in {"img", "input", "source", "br", "hr", "meta", "link"}:
            self.layout.append(["-", tag])

    def handle_endtag(self, tag):
        if self.body:
            self.layout.append(["-", tag])
        if tag == "body":
            self.body = False


def dom_hash(path: str) -> str:
    parser = BodyLayout()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    return sha(json.dumps(parser.layout, separators=(",", ":"), ensure_ascii=False).encode())


def main() -> None:
    baseline = json.loads((ROOT / "design-lock.json").read_text(encoding="utf-8"))
    errors = []
    for path, expected in baseline["layouts"].items():
        if dom_hash(path) != expected:
            errors.append(f"{path}: approved layout has changed")
    for path, expected in baseline["styles"].items():
        if sha((ROOT / path).read_bytes()) != expected:
            errors.append(f"{path}: approved CSS has changed")
    if errors:
        for error in errors:
            print("FAIL:", error)
        print("Do not modify design-lock.json merely to pass CI. Owner approval required; see AGENTS.md.")
        raise SystemExit(1)
    print(f"PASS: {len(baseline['layouts'])} protected layouts and {len(baseline['styles'])} protected stylesheets")


if __name__ == "__main__":
    main()
