# -*- coding: utf-8 -*-
"""card.py — the 1200x630 link card, data/card.jpg (site.py copies it into the site).

  python3 tools/card.py

The title and the line from the home page on the left; the twenty speeds of
data/ladder.json on the right, one bar each on the page's base-ten axis.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1200, 630
PAPER, INK, MUTED, LINE = (18, 16, 14), (240, 230, 214), (166, 148, 124), (58, 49, 40)
RED, AMBER = (239, 75, 75), (240, 176, 74)
FD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FB = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
FR = "/System/Library/Fonts/Supplemental/Georgia.ttf"


def f(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def label(ms: float) -> str:
    for lim, div, unit in ((1e3, 1, "m/s"), (1e8, 1e3, "km/s")):
        if ms < lim:
            v = ms / div
            return "%s %s" % (("%.0f" % v) if v >= 100 else ("%.3g" % v), unit)
    return "299,792 km/s"


def main() -> None:
    rungs = json.loads((ROOT / "data" / "ladder.json").read_text(encoding="utf-8"))["rungs"]
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 10], fill=RED)

    d.text((60, 70), "GOIN'", font=f(FD, 200), fill=INK)
    d.text((60, 250), "FAST", font=f(FD, 200), fill=RED)
    d.text((64, 480), "Twenty measured speeds, from the ground", font=f(FB, 28), fill=MUTED)
    d.text((64, 520), "under the house to light itself,", font=f(FB, 28), fill=MUTED)
    d.text((64, 560), "and what each one costs.", font=f(FB, 28), fill=MUTED)

    x0, x1, top, step = 690, 1130, 58, 26.5
    lo, hi = -10.0, 9.0
    sx = lambda v: x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)   # noqa: E731
    for k in range(-9, 10, 3):
        d.line([sx(10.0 ** k), top - 8, sx(10.0 ** k), top + step * 20 - 6], fill=LINE, width=2)
    for i, r in enumerate(rungs):
        y = top + i * step
        x = sx(r["ms"])
        d.line([x0, y + 9, x, y + 9], fill=MUTED, width=3)
        d.ellipse([x - 7, y + 2, x + 7, y + 16], fill=RED if i != len(rungs) - 1 else AMBER)
    show = {0: "a fingernail a year", 8: "sound  343 m/s", len(rungs) - 1: "light  299,792 km/s"}
    for i, t in show.items():
        y = top + i * step
        x = sx(rungs[i]["ms"])
        if i == len(rungs) - 1:
            d.rectangle([x - 262, y - 6, x - 16, y + 24], fill=PAPER)
            d.text((x - 24, y + 9), t, font=f(FR, 24), fill=AMBER, anchor="rm")
        else:
            d.text((x + 16, y + 9), t, font=f(FR, 24), fill=INK, anchor="lm")
    d.text((x0, top + step * 20 + 14), "metres per second, a thousand times per line",
           font=f(FR, 20), fill=MUTED)

    out = ROOT / "data" / "card.jpg"
    im.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print("card  %s  %d KB" % (out, out.stat().st_size // 1024))


if __name__ == "__main__":
    main()
