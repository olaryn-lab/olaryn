#!/usr/bin/env python3
"""Rebuild PNG favicons, application icons, and social card from the SVG mark.

Requires Node.js, Playwright/Chromium and Pillow. Run from the repo root:
    python3 scripts/build-brand-assets.py --brand olaryn
    python3 scripts/build-brand-assets.py --brand authward

SVG files are the design source of truth. The output icons deliberately use the
light-mode palette as PNG/ICO files cannot follow the OS colour-scheme setting.
"""
import argparse
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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


def font(candidates, size):
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def make_social(brand: str, mark: Image.Image):
    parchment = '#F5EFE3' if brand == 'olaryn' else '#FAF8F5'
    burgundy, ink = '#6B3F4B', '#211E1B'
    image = Image.new('RGB', (1200, 630), parchment)
    draw = ImageDraw.Draw(image)
    serif = font(['/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'], 104)
    sans = font(['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'], 30)
    subtitle = font(['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'], 46)
    if brand == 'olaryn':
        image.paste(mark.resize((205, 205), Image.Resampling.LANCZOS), (120, 204), mark.resize((205, 205), Image.Resampling.LANCZOS))
        draw.text((364, 187), 'Olaryn', fill=ink, font=serif)
        draw.text((366, 325), 'Learning compounds.', fill=burgundy, font=subtitle)
        draw.text((368, 413), 'What we learn, improve, and create', fill='#70695E', font=sans)
        draw.text((368, 457), 'should strengthen everything around it.', fill='#70695E', font=sans)
    else:
        draw.rounded_rectangle((83, 93, 1117, 538), radius=18, fill='#FFFFFF', outline='#EAE5E2', width=2)
        symbol = mark.resize((200, 200), Image.Resampling.LANCZOS)
        image.paste(symbol, (137, 204), symbol)
        draw.text((381, 187), 'Authward', fill=ink, font=serif)
        draw.text((385, 323), 'Secure identity, simply.', fill=burgundy, font=subtitle)
        draw.text((388, 422), 'An Olaryn product', fill='#70695E', font=sans)
    image.save((ROOT if brand == 'olaryn' else ROOT / 'public') / 'og-image.png', optimize=True)


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
    make_social(brand, transparent)
    print(f'Generated {brand} 16/32px favicons, ICO, 180/192/512px icons and OG image from SVG.')


if __name__ == '__main__':
    main()
