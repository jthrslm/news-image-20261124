#!/usr/bin/env python3
"""Final entry image for news-image-20261124 (1024x1024 PNG, <=1 MiB).
Six stories from 24 November 2026, each verified against an authoritative
source on 25 Nov 2026 (Reuters / CNN / WSJ / France 24 / Sanofi). The COP31
collapse was left out: it ended on 22 Nov, so it is not 24 Nov news. The
Colombia car bomb was left out: only a single weak source could be found.
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
    ("NVIDIA", "Huang is back as Nvidia chief",
     "The board unanimously reinstates Jensen Huang as president and CEO, 11 days after his resignation; shares jump.", RED),
    ("CHINA", "Shanghai party chief probed",
     "China investigates Politburo member Chen Jining, Shanghai's party boss, the fourth top leader to fall since 2025.", TEAL),
    ("UKRAINE", "Zelensky urges four-party talks",
     "Ukraine's president calls for Ukraine-Russia-US-Europe peace talks 'as soon as possible'; Kyiv is ready tomorrow.", NAVY),
    ("POLAND", "Russian drone enters Polish airspace",
     "A Russian drone briefly crosses into Poland during a night attack on Ukraine; Warsaw says it looks deliberate.", AMBER),
    ("CHIPS", "US blacklists Singapore's Megaspeed",
     "Washington adds Megaspeed to its Entity List over alleged diversion of Nvidia AI chips to China, plus six more firms.", PURPLE),
    ("PHARMA", "Sanofi buys Insmed for $41bn",
     "Sanofi agrees to buy US drugmaker Insmed for $41 billion in cash, the year's biggest biopharma deal, at $175 a share.", GREEN),
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

d.text((48, 992), "Sources: Reuters · CNN · WSJ · France 24 · Sanofi  ·  Reported 24 November 2026", font=load_font(19), fill=GREY)
img.save(OUT, "PNG", optimize=True)
print(OUT, os.path.getsize(OUT), "bytes,", img.size)
