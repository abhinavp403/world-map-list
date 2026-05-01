#!/usr/bin/env python3
"""Build build/icon.ico from build/icon-1024.png.

Constructs the ICO binary manually (header + PNG-compressed frames) so
every requested size is embedded correctly — Pillow's own ICO encoder
mis-encodes multi-size files in some versions.
"""

import struct, os
from io import BytesIO
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
SRC  = os.path.join(ROOT, 'build', 'icon-1024.png')
OUT  = os.path.join(ROOT, 'build', 'icon.ico')

SIZES = [16, 24, 32, 48, 64, 128, 256]

def build_ico(src_path, out_path, sizes):
    src = Image.open(src_path).convert('RGBA')

    # Render each size to a PNG byte-string
    frames = []
    for s in sizes:
        buf = BytesIO()
        src.resize((s, s), Image.LANCZOS).save(buf, format='PNG')
        frames.append(buf.getvalue())

    n = len(frames)
    # ICO header (6 bytes) + n × directory entry (16 bytes each)
    dir_offset = 6 + n * 16

    header  = struct.pack('<HHH', 0, 1, n)   # reserved, type=1, count
    entries = b''
    data    = b''
    off     = dir_offset

    for s, png in zip(sizes, frames):
        w = h = 0 if s == 256 else s          # 0 encodes 256 in ICO spec
        entries += struct.pack('<BBBBHHII',
            w, h,       # width, height
            0,          # color count  (0 = 32-bit)
            0,          # reserved
            1,          # color planes
            32,         # bits per pixel
            len(png),   # data size
            off,        # data offset
        )
        data += png
        off  += len(png)

    with open(out_path, 'wb') as f:
        f.write(header + entries + data)

if __name__ == '__main__':
    build_ico(SRC, OUT, SIZES)
