#!/usr/bin/env python3
"""Draft entry image for news-image-20261124 (1024x1024 PNG, <=1 MiB).
DRAFT only: stories are the morning of 24 Nov 2026 and must be re-verified
against authoritative sources on 25 Nov before finalising.
Draws with PIL only, no network, no external images.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

def load_font(sz, bold=False):
    for p in (f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'Bold' if bold else ''}.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

NAVY = (13, 27, 62)
TEAL = (0, 128, 128)
RED = (178, 34, 34)
AMBER = (176, 124, 0)
GREEN = (34, 120, 60)
PURPLE = (90, 60, 140)
GREY = (90, 90, 90)
LIGHT = (240, 242, 245)

# Header
d.rectangle([0, 0, W, 150], fill=NAVY)
d.text((48, 28), "TUESDAY  24  NOVEMBER  2026", font=load_font(44, bold=True), fill="white")
d.text((48, 88), "THE WORLD IN ONE PICTURE  ·  make.fun news image", font=load_font(26), fill=(180, 200, 230))

stories = [
    ("UKRAINE", "War reaches Libya's coast",
     "Ukraine says it struck a Russian warship off Libya; the UN warns Libya must not become a new front.", RED),
    ("CLIMATE", "COP31 talks stall",
     "Climate talks in Türkiye hit deadlock as nations split over fossil fuels and finance for poorer states.", GREEN),
    ("INDONESIA", "Factory fire, rescue under way",
     "A major fire at an Indonesian industrial plant leaves workers missing; emergency teams search the site.", AMBER),
    ("INDIA", "Himalayan flood",
     "At least four people are dead and about 100 missing after floodwater tore through a mountain valley.", TEAL),
    ("HEALTH", "Bangladesh vaccinates 50m children",
     "A month-long typhoid vaccination drive targets drug-resistant strains across South Asia.", PURPLE),
    ("TRADE", "Japan–US deal lifts markets",
     "Tokyo stocks rally after a Japan–US trade deal; SoftBank plans a $2bn investment in Intel.", NAVY),
]

y = 170
for tag, head, body, color in stories:
    d.rounded_rectangle([36, y, W - 36, y + 120], radius=14, fill=LIGHT)
    d.rectangle([36, y, 52, y + 120], fill=color)
    d.text((72, y + 14), tag, font=load_font(24, bold=True), fill=color)
    d.text((72, y + 42), head, font=load_font(30, bold=True), fill=(20, 20, 20))
    # wrap body to ~62 chars
    words, lines, cur = body.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= 62:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    for i, line in enumerate(lines[:2]):
        d.text((72, y + 78 + i * 20), line, font=load_font(19), fill=GREY)
    y += 134

d.text((48, 992), "Sources: news reported on 24 November 2026  ·  One day, six stories", font=load_font(19), fill=GREY)
img.save(OUT, "PNG", optimize=True)
print(OUT, os.path.getsize(OUT), "bytes,", img.size)
