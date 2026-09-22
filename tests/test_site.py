#!/usr/bin/env python3
"""test_site.py — the arithmetic and the build, checked against published values.

    python3 tests/test_site.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "site"
F = json.loads((ROOT / "build" / "facts.json").read_text(encoding="utf-8"))
LADDER = json.loads((ROOT / "data" / "ladder.json").read_text(encoding="utf-8"))
EXTRA = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
SRC = {**LADDER["sources"], **EXTRA["sources"]}

fails: list[str] = []


def ok(cond: bool, what: str) -> None:
    print(("  ok   " if cond else "  FAIL ") + what)
    if not cond:
        fails.append(what)


def near(got: float, want: float, tol: float, what: str) -> None:
    ok(abs(got - want) <= tol, f"{what}: {got:.6g} (published {want:.6g}, ±{tol:g})")


print("physics, against published values")
near(F["orbit_iss"], 7660, 15, "orbital speed at 420 km, NASA gives ~7.66 km/s")
near(F["orbit_period_min"], 92.7, 1.0, "orbital period at 420 km, NASA gives ~93 min")
near(F["escape_earth"], 11186, 5, "escape velocity, NASA Earth fact sheet 11.186 km/s")
near(F["equator_spin"], 465.1, 0.5, "equatorial spin, 465 m/s")
near(F["gamma99"], 7.0888, 1e-3, "gamma at 0.99c")
near(F["sum_075"], 0.96, 1e-9, "0.75c + 0.75c, relativistic")
near(F["mach_angle_15"], 41.81, 0.02, "Mach cone half-angle at Mach 1.5")
near(F["drag_ratio_60_30"], 8.0, 1e-9, "doubling the speed costs 8x the power")
near(F["c"], 299792458, 0, "c, exact by the SI definition of the metre")

print("\nthe ladder")
rungs = LADDER["rungs"]
ok(len(rungs) >= 20, f"{len(rungs)} rungs")
ok(all(rungs[i]["ms"] < rungs[i + 1]["ms"] for i in range(len(rungs) - 1)),
   "rungs in increasing order")
ok(all(r["src"] in SRC for r in rungs), "a source for each rung")
ok(rungs[-1]["ms"] == 299792458.0, "the top rung is light, exactly")
span = math.log10(rungs[-1]["ms"] / rungs[0]["ms"])
ok(span > 17, f"the ladder spans {span:.1f} powers of ten")

print("\nthe build")
pages = sorted(p.relative_to(SITE).as_posix() for p in SITE.rglob("index.html"))
ok(len(pages) == 9, f"{len(pages)} pages: {', '.join(p.split('/')[0] or 'front' for p in pages)}")
for name in ("sitemap.xml", "robots.txt", "llms.txt", "humans.txt", "icon.svg", "404.html"):
    ok((SITE / name).is_file(), name)
ok(len(list((SITE / "img").glob("*.svg"))) == 6, "six diagrams")

html_all = "\n".join(p.read_text(encoding="utf-8") for p in SITE.rglob("*.html"))
ok("/Users/" not in html_all, "no host path in the pages")
cited = set(re.findall(r'sources/#([a-z0-9-]+)"', html_all))
ok(cited <= set(SRC), f"{len(cited)} citation anchors, all defined")
src_page = (SITE / "sources" / "index.html").read_text(encoding="utf-8")
ok(all(f'id="{k}"' in src_page for k in cited), "every anchor cited has an entry")
ok(all(c in src_page for c in ("CC BY 4.0", "MIT")), "the licence terms are stated")
for who in ("Nature", "Phys. Rev. Lett.", "Living Reviews", "BIPM"):
    ok(who in src_page, f"sources name {who}")

reck = (SITE / "reckoner" / "index.html").read_text(encoding="utf-8")
ok(reck.count('class="calc"') == 4, "four calculators")
ok("1 / Math.sqrt(1 - b * b)" in reck, "the gamma formula is in the page, not a table")

print("\n" + ("FAILED: " + "; ".join(fails) if fails else "all clear"))
sys.exit(1 if fails else 0)
