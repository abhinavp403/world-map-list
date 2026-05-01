#!/usr/bin/env python3
"""
Generates build/icon-1024.png  — a globe icon using Pillow only.
Run: python3 scripts/create_icon.py
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math, os

SIZE = 1024
CX = CY = SIZE // 2
R    = int(SIZE * 0.44)   # globe radius
PAD  = int(SIZE * 0.02)   # breathing room around globe

# ── helpers ───────────────────────────────────────────────────────────────────

def new_layer():
    return Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))

def clip_to_globe(layer):
    """Clip a layer's alpha to the globe circle."""
    mask = Image.new('L', (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([CX-R, CY-R, CX+R, CY+R], fill=255)
    r, g, b, a = layer.split()
    return Image.merge('RGBA', (r, g, b, ImageChops.multiply(a, mask)))

def over(base, layer):
    return Image.alpha_composite(base, layer)

# ── build icon ────────────────────────────────────────────────────────────────

def make_icon():
    img = Image.new('RGBA', (SIZE, SIZE), (8, 12, 24, 255))   # dark bg

    # ── 1. Outer glow ────────────────────────────────────────────────────────
    glow = new_layer()
    gd   = ImageDraw.Draw(glow)
    for s in range(55, 0, -1):
        r = R + s * 2
        a = int(50 * (1 - s / 55) ** 2)
        gd.ellipse([CX-r, CY-r, CX+r, CY+r], fill=(79, 142, 247, a))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=12))
    img  = over(img, glow)

    # ── 2. Ocean base ────────────────────────────────────────────────────────
    ocean = new_layer()
    ImageDraw.Draw(ocean).ellipse([CX-R, CY-R, CX+R, CY+R], fill=(7, 20, 58, 255))
    img = over(img, ocean)

    # ── 3. Lighting gradient (two offset circles = fake 3-D shading) ─────────
    #   bright zone — top-left
    lit = new_layer()
    lx, ly = CX - int(R * 0.30), CY - int(R * 0.30)
    lr = int(R * 0.92)
    ImageDraw.Draw(lit).ellipse([lx-lr, ly-lr, lx+lr, ly+lr], fill=(18, 65, 160, 215))
    img = over(img, clip_to_globe(lit))

    #   mid-tone fill so bottom-right isn't pitch-black
    mid = new_layer()
    ImageDraw.Draw(mid).ellipse([CX-R, CY-R, CX+R, CY+R], fill=(11, 38, 105, 130))
    img = over(img, clip_to_globe(mid))

    # ── 4. Grid lines ────────────────────────────────────────────────────────
    grid = new_layer()
    grd  = ImageDraw.Draw(grid)
    TILT = 0.27   # y-radius of latitude ellipses (perspective squash)

    # latitude lines
    for lat in (-60, -30, 0, 30, 60):
        lat_rad = math.radians(lat)
        yp  = CY - int(R * math.sin(lat_rad))
        xRl = int(R * math.cos(lat_rad))
        yRl = max(3, int(xRl * TILT))
        is_eq  = (lat == 0)
        colour = (105, 170, 255, 135) if is_eq else (79, 142, 247, 78)
        width  = 5 if is_eq else 3
        grd.ellipse([CX - xRl, yp - yRl, CX + xRl, yp + yRl],
                    outline=colour, width=width)

    # longitude lines
    for lon in (30, 60, 90, 120, 150):
        xRl = int(R * math.sin(math.radians(lon)))
        grd.ellipse([CX - xRl, CY - R, CX + xRl, CY + R],
                    outline=(79, 142, 247, 68), width=3)

    # prime meridian — slightly brighter vertical line
    grd.line([CX, CY - R, CX, CY + R],
             fill=(105, 170, 255, 115), width=5)

    img = over(img, clip_to_globe(grid))

    # ── 5. Edge darkening ────────────────────────────────────────────────────
    edge = new_layer()
    ed   = ImageDraw.Draw(edge)
    steps = 55
    for s in range(steps, 0, -1):
        er = R - int(s * 0.55)
        a  = int(210 * (s / steps) ** 2.8)
        ed.ellipse([CX-er, CY-er, CX+er, CY+er],
                   outline=(1, 4, 16, a), width=5)
    img = over(img, edge)

    # ── 6. Specular highlight ─────────────────────────────────────────────────
    spec = new_layer()
    sx, sy = CX - int(R * 0.37), CY - int(R * 0.37)
    sr = int(R * 0.19)
    ImageDraw.Draw(spec).ellipse([sx-sr, sy-sr, sx+sr, sy+sr],
                                  fill=(175, 220, 255, 115))
    spec = spec.filter(ImageFilter.GaussianBlur(radius=24))
    img  = over(img, clip_to_globe(spec))

    # ── 7. Rim highlight ─────────────────────────────────────────────────────
    rim = new_layer()
    ImageDraw.Draw(rim).ellipse([CX-R, CY-R, CX+R, CY+R],
                                 outline=(88, 158, 255, 205), width=6)
    img = over(img, rim)

    return img

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    build_dir = os.path.join(os.path.dirname(__file__), '..', 'build')
    os.makedirs(build_dir, exist_ok=True)

    print('Drawing globe …')
    icon = make_icon()

    out_png = os.path.join(build_dir, 'icon-1024.png')
    icon.save(out_png)
    print(f'✓  Saved {out_png}')

    # Also save a 512 px version (used by iconutil)
    icon.resize((512, 512), Image.LANCZOS).save(
        os.path.join(build_dir, 'icon-512.png'))
    print('✓  Saved build/icon-512.png')
