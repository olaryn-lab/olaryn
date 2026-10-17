#!/usr/bin/env python3
"""Rebuild PNG favicons, application icons, and social card from the SVG mark.

Requires Node.js, Playwright/Chromium and Pillow. Run from the repo root:
    python3 scripts/build-brand-assets.py --brand olaryn
    python3 scripts/build-brand-assets.py --brand authward

SVG files are the design source of truth. The output icons deliberately use the
light-mode palette as PNG/ICO files cannot follow the OS colour-scheme setting.
Social cards are rendered from scripts/og-card.html by scripts/render-og-cards.mjs.
"""
import argparse
import subprocess
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def raster_svg(svg: Path, width: int) -> Image.Image:
    # Chromium renders SVG path strokes correctly; the ImageMagick SVG backend
    # silently drops them on some supported machines.
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as tmp:
        png = Path(tmp) / 'svg.png'
        subprocess.run(['node', str(ROOT / 'scripts/render-brand-svg.mjs'), str(svg), str(png)], check=True)
        with Image.open(png) as image:
            return image.convert('RGBA').resize((width, width), Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--brand', choices=['olaryn', 'authward'], required=True)
    brand = parser.parse_args().brand
    base = ROOT if brand == 'olaryn' else ROOT / 'public'
    logo_mark = base / 'logo-mark.svg'
    favicon = base / 'favicon.svg'
    for file in (logo_mark, favicon):
        if not file.is_file():
            raise FileNotFoundError(file)
    icon = raster_svg(favicon, 512)
    for size, name in [(16, 'favicon-16x16.png'), (32, 'favicon-32x32.png'),
                       (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
        icon.resize((size, size), Image.Resampling.LANCZOS).save(base / name, optimize=True)
    icon.save(base / 'favicon.ico', sizes=[(16,16), (32,32), (48,48), (64,64)])
    transparent = raster_svg(logo_mark, 512)
    if brand == 'olaryn':
        transparent.save(base / 'logo-mark.png', optimize=True)
    if brand == 'olaryn':
        subprocess.run(['node', str(ROOT / 'scripts/render-og-cards.mjs')], check=True)
    print(f'Generated {brand} 16/32px favicons, ICO, 180/192/512px icons and social cards from SVG.')


if __name__ == '__main__':
    main()
