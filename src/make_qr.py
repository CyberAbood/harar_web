"""Generate the site's QR code. Usage: python make_qr.py [URL]"""
import pathlib
import sys

import segno
from PIL import Image

URL = sys.argv[1] if len(sys.argv) > 1 else "https://cyberabood.github.io/harar/"
INK, PAPER = "#26263f", "#e4dcc8"
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "qr"
OUT.mkdir(exist_ok=True)

qr = segno.make(URL, error="q", micro=False)
qr.save(OUT / "harar-qr.svg", dark=INK, light="#ffffff", border=4, scale=10)
qr.save(OUT / "harar-qr.png", dark=INK, light="#ffffff", border=4, scale=32)

# Printable card: bundled header (logo and caption) above the code.
header = Image.open(HERE / "qr-header.png").convert("RGB")
code_px = 1000
scale = code_px // (qr.symbol_size(border=4)[0])
qr.save(OUT / "_tmp.png", dark=INK, light=PAPER, border=4, scale=scale)
code = Image.open(OUT / "_tmp.png").convert("RGB")
card = Image.new("RGB", (header.width, header.height + code.height + 90), PAPER)
card.paste(header, (0, 0))
card.paste(code, ((card.width - code.width) // 2, header.height))
card.save(OUT / "harar-qr-card.png", dpi=(300, 300))
(OUT / "_tmp.png").unlink()
print("QR ->", URL, "| version", qr.designator)
