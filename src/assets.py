"""Trace the logo from the menu photo and generate the hatched line art."""
import json
import math
import random

import numpy as np
import potrace
from PIL import Image, ImageFilter

MENU = "menu-photo.png"


def trace_logo():
    im = Image.open(MENU).convert("L").crop((295, 50, 520, 125))
    im = im.resize((im.width * 8, im.height * 8), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2.2))
    bitmap = potrace.Bitmap(np.array(im) >= 142)
    plist = bitmap.trace(turdsize=250, alphamax=1.15, opttolerance=0.6)
    fmt = lambda p: f"{p.x:.0f} {p.y:.0f}"
    parts, xs, ys = [], [], []
    for curve in plist:
        parts.append("M" + fmt(curve.start_point))
        xs.append(curve.start_point.x)
        ys.append(curve.start_point.y)
        for seg in curve.segments:
            if seg.is_corner:
                parts.append(f"L{fmt(seg.c)}L{fmt(seg.end_point)}")
                pts = [seg.c, seg.end_point]
            else:
                parts.append(f"C{fmt(seg.c1)} {fmt(seg.c2)} {fmt(seg.end_point)}")
                pts = [seg.c1, seg.c2, seg.end_point]
            xs += [p.x for p in pts]
            ys += [p.y for p in pts]
        parts.append("Z")
    pad = 4
    box = (min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad)
    return "".join(parts), " ".join(f"{v:.0f}" for v in box)


def bez(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
    return x, y


def blade(rnd, base, tip, width, n):
    """A leaf-like blade: two curved edges with hatch lines ruled between them."""
    (bx, by), (tx, ty) = base, tip
    dx, dy = tx - bx, ty - by
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    mx, my = (bx + tx) / 2, (by + ty) / 2
    c1 = (mx + nx * width, my + ny * width)
    c2 = (mx - nx * width * 0.6, my - ny * width * 0.6)
    outline = (
        f"M{bx:.0f} {by:.0f}Q{c1[0]:.0f} {c1[1]:.0f} {tx:.0f} {ty:.0f}"
        f"Q{c2[0]:.0f} {c2[1]:.0f} {bx:.0f} {by:.0f}"
    )
    hatch = []
    for i in range(1, n):
        t = i / n
        a = bez(base, c1, tip, min(1, t + 0.09))
        b = bez(base, c2, tip, t)
        qx = (a[0] + b[0]) / 2 + dx / length * 7 + rnd.uniform(-1.6, 1.6)
        qy = (a[1] + b[1]) / 2 + dy / length * 7 + rnd.uniform(-1.6, 1.6)
        hatch.append(f"M{a[0]:.0f} {a[1]:.0f}Q{qx:.0f} {qy:.0f} {b[0]:.0f} {b[1]:.0f}")
    return outline, "".join(hatch)


def art():
    rnd = random.Random(11)
    # base point, tip, belly width, hatch count: a low thicket rising from the bottom edge
    spec = [
        ((70, 520), (250, 120), 92, 26),
        ((205, 520), (150, 190), 70, 18),
        ((300, 520), (505, 215), 82, 24),
        ((455, 520), (395, 285), 58, 13),
        ((610, 520), (735, 300), 62, 17),
        ((800, 520), (925, 190), 88, 26),
        ((945, 520), (860, 250), 62, 16),
        ((1055, 520), (1185, 90), 96, 30),
        ((1195, 520), (1120, 225), 66, 18),
    ]
    outlines, hatches = [], []
    for base, tip, width, n in spec:
        o, h = blade(rnd, base, tip, width, int(n * 1.5))
        outlines.append(o)
        hatches.append(h)
    return outlines, "".join(hatches)


path, box = trace_logo()
outlines, hatches = art()
json.dump({"logo": path, "box": box, "outlines": outlines, "hatches": hatches}, open("assets.json", "w"))
print("logo bytes", len(path), "box", box, "art bytes", sum(map(len, outlines)) + len(hatches))
