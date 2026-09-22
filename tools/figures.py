#!/usr/bin/env python3
"""figures.py — draws each diagram from the formula it shows, and writes the numbers
the prose quotes into build/facts.json, so the page and the picture cannot drift apart.

    python3 tools/figures.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "img"
C = 299792458.0                      # m/s, exact (SI)
G = 6.67430e-11                      # m^3 kg^-1 s^-2, CODATA 2018
M_EARTH = 5.9722e24                  # kg, IAU
R_EARTH = 6.371e6                    # m, mean
MPH = 0.44704                        # m/s per mph, exact


def svg(w: int, h: int, body: str, title: str, desc: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d">'
            f'<title id="t">{title}</title><desc id="d">{desc or title}</desc>'
            f'<style>'
            f'.ink{{fill:#17120e}} .mut{{fill:#6a5c48}} .acc{{fill:#b7222a}}'
            f'.s{{stroke:#17120e;fill:none;stroke-width:2}}'
            f'.sm{{stroke:#d8c9ae;fill:none;stroke-width:1.4}}'
            f'.sa{{stroke:#b7222a;fill:none;stroke-width:3}}'
            f'.sb{{stroke:#e08a1e;fill:none;stroke-width:2.4}}'
            f'text{{font-family:Georgia,serif;font-size:15px}}'
            f'.lab{{font-family:"Bebas Neue",Oswald,"Arial Narrow",sans-serif;'
            f'letter-spacing:.06em;font-size:17px}}'
            # the hollerin'. All of it is CSS so one media query can switch it off.
            f'.holler{{font-family:"Bebas Neue",Oswald,"Arial Narrow",sans-serif;'
            f'font-size:26px;letter-spacing:.04em;fill:#e08a1e;'
            f'transform-box:fill-box;transform-origin:center}}'
            f'.pop{{animation:pop 4s ease-in-out infinite;opacity:0}}'
            f'@keyframes pop{{0%,58%{{opacity:0;transform:translateY(10px) scale(.85) rotate(-7deg)}}'
            f'66%{{opacity:1;transform:translateY(0) scale(1.12) rotate(-7deg)}}'
            f'72%{{transform:translateY(0) scale(1) rotate(-7deg)}}'
            f'90%{{opacity:1}}100%{{opacity:0;transform:translateY(-8px) scale(1) rotate(-7deg)}}}}'
            f'.rider{{animation:rider 7s linear infinite}}'
            f'@keyframes rider{{0%{{opacity:0}}4%{{opacity:1}}96%{{opacity:1}}100%{{opacity:0}}}}'
            f'.draw{{stroke-dasharray:2400;stroke-dashoffset:2400;'
            f'animation:draw 2.6s ease-out both}}'
            f'@keyframes draw{{to{{stroke-dashoffset:0}}}}'
            f'.slide{{animation:slide .8s cubic-bezier(.2,.9,.3,1) both}}'
            f'@keyframes slide{{0%{{opacity:0;transform:translateX(-26px)}}'
            f'100%{{opacity:1;transform:translateX(0)}}}}'
            f'.throb{{animation:throb 2.6s ease-in-out infinite}}'
            f'@keyframes throb{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}'
            f'@media (prefers-reduced-motion:reduce){{'
            f'*{{animation:none!important;stroke-dashoffset:0!important}}'
            f'.pop,.rider{{opacity:1}}}}'
            f'@media (prefers-color-scheme:dark){{'
            f'.ink{{fill:#f0e6d6}} .mut{{fill:#a6947c}} .acc{{fill:#ef4b4b}}'
            f'.s{{stroke:#f0e6d6}} .sm{{stroke:#3a3128}} .sa{{stroke:#ef4b4b}}'
            f'.sb{{stroke:#f0b04a}} .holler{{fill:#f0b04a}}}}'
            f'</style>{body}</svg>')


def write(name: str, s: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(s, encoding="utf-8")


# ------------------------------------------------------------------ the ladder
def ladder(rungs: list[dict]) -> str:
    """One row per rung, a dot on a shared log axis. Labels stacked on a single axis
    collided into porridge across the crowded decades — a row apiece reads instead."""
    row_h, top, left, right = 26, 54, 260, 168
    w = 980
    h = top + row_h * len(rungs) + 54
    lo, hi = -9.6, 8.8                                   # log10 m/s
    x = lambda L: left + (L - lo) / (hi - lo) * (w - left - right)
    b = []
    for e in range(-9, 9, 3):                            # a decade grid, every third
        xx = x(e)
        b.append(f'<line x1="{xx:.1f}" y1="{top-16}" x2="{xx:.1f}" y2="{h-46}" class="sm"/>')
        b.append(f'<text x="{xx:.1f}" y="{h-28}" text-anchor="middle" class="mut">'
                 f'10<tspan dy="-6" font-size="10">{e}</tspan></text>')
    b.append(f'<text x="{left}" y="{top-26}" class="lab ink">METRES PER SECOND — '
             f'EACH GRID LINE IS A THOUSAND TIMES THE LAST</text>')
    for i, r in enumerate(rungs):
        y = top + i * row_h
        xx = x(math.log10(r["ms"]))
        if i % 2 == 0:
            b.append(f'<rect x="0" y="{y-row_h/2+3:.0f}" width="{w}" height="{row_h}" '
                     f'fill="#b7222a" opacity=".045"/>')
        b.append(f'<text x="{left-14}" y="{y+5}" text-anchor="end" class="ink">'
                 f'{html_escape(r["name"])}</text>')
        d = f'style="animation-delay:{i*0.09:.2f}s"'
        b.append(f'<line x1="{x(lo):.1f}" y1="{y}" x2="{xx:.1f}" y2="{y}" class="sm slide" {d}/>')
        b.append(f'<circle cx="{xx:.1f}" cy="{y}" r="5" class="acc slide" {d}/>')
        b.append(f'<text x="{xx+11:.1f}" y="{y+5}" class="mut slide" {d}>{fast(r["ms"])}</text>')
        if r["id"] == "light":
            b.append(f'<text x="{xx-16:.1f}" y="{y-14}" text-anchor="end" '
                     f'class="holler pop">YEE HAW!</text>')
    return svg(w, h, "".join(b), "The ladder of speed, on a log scale",
               "Twenty measured speeds from continental drift to light, one row each, "
               "plotted on a shared base-ten logarithmic axis of metres per second.")


def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fast(ms: float) -> str:
    """The number, in the unit a person would say it in."""
    if ms >= 1e5:
        return f"{ms/1000:,.0f} km/s"
    if ms >= 1000:
        return f"{ms/1000:,.1f} km/s"
    if ms >= 10:
        return f"{ms:,.0f} m/s"
    if ms >= 1:
        return f"{ms:,.1f} m/s"
    if ms >= 0.001:
        return f"{ms*1000:.1f} mm/s"
    return f"{ms:.1e} m/s"


# ------------------------------------------------------------------ the mach cone
def mach(M: float = 1.5) -> str:
    """Wavefronts one second apart from a source doing Mach M, and the cone they share.
    Sized so the oldest ring still fits the frame — the first cut ran off all four sides."""
    w, h = 900, 470
    cy, x_now, per = 235, 800, 42
    b = []
    for k in range(1, 7):                                 # oldest ring last to draw
        cx = x_now - k * per                              # where the source was, k back
        r = k * per / M                                   # sound went a·t, source went M·a·t
        b.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="{r:.1f}" class="sm throb" '
                 f'style="animation-delay:{-k*0.36:.2f}s"/>')
    mu = math.asin(1 / M)
    dx = 250
    dy = dx * math.tan(mu)
    b.append(f'<line x1="{x_now}" y1="{cy}" x2="{x_now-dx}" y2="{cy-dy:.1f}" class="sa"/>')
    b.append(f'<line x1="{x_now}" y1="{cy}" x2="{x_now-dx}" y2="{cy+dy:.1f}" class="sa"/>')
    b.append(f'<line x1="60" y1="{cy}" x2="{x_now}" y2="{cy}" class="sm"/>')
    b.append(f'<polygon points="{x_now},{cy} {x_now-26},{cy-8} {x_now-26},{cy+8}" class="acc"/>')
    b.append(f'<text x="{x_now}" y="{cy-172}" text-anchor="end" class="lab ink">'
             f'GOIN\' MACH {M} — HALF AGAIN THE SPEED OF SOUND</text>')
    b.append(f'<text x="{x_now-dx-6}" y="{cy+dy+4:.1f}" text-anchor="end" class="acc lab">'
             f'THE BOOM RIDES THIS EDGE</text>')
    b.append(f'<text x="34" y="34" class="mut">each ring is the racket it made one second '
             f'earlier, spreadin\' out at 343 m/s in all directions</text>')
    b.append(f'<text x="{x_now}" y="{cy+92}" text-anchor="end" class="holler pop">'
             f'YEE HAW!</text>')
    b.append(f'<text x="34" y="{h-22}" class="ink">sin μ = 1 / M &#160;→&#160; '
             f'μ = {math.degrees(mu):.1f}° at Mach {M}</text>')
    return svg(w, h, "".join(b), "Why a supersonic thing drags a cone behind it",
               "Circular sound wavefronts emitted one second apart by a source moving at "
               "Mach 1.5, their common tangent forming a cone of half-angle 41.8 degrees.")


# ------------------------------------------------------------------ drag
def drag_curve(cd=0.40, area=3.0, rho=1.225) -> tuple[str, dict]:
    w, h, pad = 900, 420, 70
    vmax = 45.0                                            # m/s
    power = lambda v: 0.5 * rho * cd * area * v ** 3       # watts, air only
    pmax = power(vmax)
    X = lambda v: pad + v / vmax * (w - 2 * pad)
    Y = lambda p: h - pad - p / pmax * (h - 2 * pad)
    pts = " ".join(f"{X(v/20):.1f},{Y(power(v/20)):.1f}" for v in range(0, int(vmax*20)+1))
    b = [f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" class="s"/>',
         f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" class="s"/>',
         f'<polyline points="{pts}" class="sa draw"/>']
    marks = {}
    for mph, lab in ((30, "30"), (60, "60"), (80, "80"), (90, "90")):
        v = mph * MPH
        p = power(v)
        marks[mph] = p
        b.append(f'<line x1="{X(v):.1f}" y1="{Y(p):.1f}" x2="{X(v):.1f}" y2="{h-pad}" class="sm"/>')
        b.append(f'<line x1="{pad}" y1="{Y(p):.1f}" x2="{X(v):.1f}" y2="{Y(p):.1f}" class="sm"/>')
        b.append(f'<circle cx="{X(v):.1f}" cy="{Y(p):.1f}" r="4.5" class="acc"/>')
        b.append(f'<text x="{X(v):.1f}" y="{h-pad+20}" text-anchor="middle" class="mut">{lab} mph</text>')
        b.append(f'<text x="{X(v)+8:.1f}" y="{Y(p)-8:.1f}" class="ink">{p/745.7:.0f} hp</text>')
    b.append(f'<text x="{pad}" y="{pad-18}" class="lab ink">HORSEPOWER SPENT SHOVIN\' AIR</text>')
    b.append(f'<text x="{X(78*MPH):.1f}" y="{Y(power(90*MPH))+14:.1f}" text-anchor="end" '
             f'class="holler pop">WHOA NOW!</text>')
    b.append(f'<text x="{w-pad}" y="{h-20}" text-anchor="end" class="mut">'
             f'P = ½ρv³ · Cd · A &#160;·&#160; Cd {cd}, {area} m² frontal, sea level</text>')
    return svg(w, h, "".join(b), "Air drag costs the cube of the speed",
               "Power needed to push a pickup-sized frontal area through still air, "
               "rising as the cube of speed."), marks


# ------------------------------------------------------------------ cannonball
def cannonball() -> str:
    w, h = 760, 760
    cx, cy, Rpx = w / 2, 320.0, 140.0
    scale = Rpx / R_EARTH
    b = [f'<circle cx="{cx}" cy="{cy}" r="{Rpx}" class="sm" fill="none"/>']
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{Rpx}" fill="#d8c9ae" opacity=".35"/>')
    top = 800000.0                                         # Newton drew an absurd mountain
    r0 = R_EARTH + top
    my = cy - Rpx - top * scale
    b.append(f'<polygon points="{cx},{my:.1f} {cx-26},{cy-Rpx+4:.1f} {cx+26},{cy-Rpx+4:.1f}" '
             f'fill="#d8c9ae" opacity=".55"/>')
    circ = math.sqrt(G * M_EARTH / r0)
    for frac, cls in ((0.40, "s"), (0.70, "s"), (0.90, "sb"), (1.0, "sa"), (1.15, "sb")):
        v = circ * frac
        # integrate the two-body problem, leapfrog, until it hits or comes round
        x, y = 0.0, r0
        vx, vy = v, 0.0
        dt, pts = 2.0, []
        for _ in range(60000):
            r = math.hypot(x, y)
            if r <= R_EARTH:
                break
            a = -G * M_EARTH / r ** 3
            vx += a * x * dt
            vy += a * y * dt
            x += vx * dt
            y += vy * dt
            pts.append((cx + x * scale, cy - y * scale))
            if len(pts) > 2 and x > 0 and abs(math.atan2(x, y)) < 0.02 and len(pts) > 100:
                break
        # a <path>, not a <polyline>: <mpath> can only follow a path, and the ball
        # that rides the closed orbit follows this one
        xy = pts[::6]
        d = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in xy)
        ident = ' id="orbit"' if cls == "sa" else ""
        b.append(f'<path d="{d}" class="{cls}"{ident}/>')
    # a ball ridin' the closed orbit, hollerin' the whole way round
    ride = ('<animateMotion dur="9s" repeatCount="indefinite">'
            '<mpath href="#orbit" xlink:href="#orbit"/></animateMotion>')
    b.append(f'<g class="rider"><circle r="6" class="acc"/>{ride}</g>')
    b.append(f'<g class="rider"><text x="14" y="-12" class="holler">WHOO-EEE!</text>{ride}</g>')
    b.append(f'<circle cx="{cx}" cy="{cy-Rpx-top*scale:.1f}" r="5" class="acc"/>')
    b.append(f'<text x="{cx+14}" y="{cy-Rpx-top*scale-6:.1f}" class="lab ink">THE CANNON</text>')
    b.append(f'<text x="{cx}" y="{cy+6}" text-anchor="middle" class="lab ink">EARTH</text>')
    b.append(f'<text x="16" y="{h-18}" class="mut">every curve integrated from a = −GM/r², '
             f'fired level off an 800 km hill; the red one comes back around</text>')
    return svg(w, h, "".join(b), "Newton's cannonball",
               "Five trajectories fired horizontally from a tall mountain at increasing "
               "speed; the slow ones strike the ground, the fastest closes into an orbit.")


# ------------------------------------------------------------------ addin' speeds
def addup() -> str:
    w, h, pad = 900, 420, 70
    X = lambda u: pad + u * (w - 2 * pad)                  # u in units of c, 0..1
    Y = lambda s: h - pad - (s / 2.0) * (h - 2 * pad)      # sum in units of c, 0..2
    plain = " ".join(f"{X(u/200):.1f},{Y(2*u/200):.1f}" for u in range(0, 201))
    rel = " ".join(f"{X(u/200):.1f},{Y((2*(u/200))/(1+(u/200)**2)):.1f}" for u in range(0, 201))
    b = [f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" class="s"/>',
         f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" class="s"/>',
         f'<line x1="{pad}" y1="{Y(1):.1f}" x2="{w-pad}" y2="{Y(1):.1f}" class="sm" '
         f'stroke-dasharray="6 5"/>',
         f'<polyline points="{plain}" class="sb" stroke-dasharray="8 6"/>',
         f'<polyline points="{rel}" class="sa draw"/>']
    b.append(f'<text x="{w-pad-6}" y="{Y(1)-10:.1f}" text-anchor="end" class="lab acc">'
             f'LIGHT — THE CEILIN\'</text>')
    b.append(f'<text x="{X(.72):.1f}" y="{Y(1.15):.1f}" text-anchor="middle" '
             f'class="holler pop">CAIN\'T GET THERE</text>')
    b.append(f'<text x="{X(.30):.1f}" y="{Y(1.46):.1f}" class="lab ink">'
             f'HOW YOU\'D RECKON IT: u + v</text>')
    b.append(f'<text x="{X(.46):.1f}" y="{Y(.62):.1f}" class="lab acc">'
             f'HOW IT COMES OUT: (u+v)/(1+uv/c²)</text>')
    for u in (0.25, 0.5, 0.75, 1.0):
        b.append(f'<text x="{X(u):.1f}" y="{h-pad+22}" text-anchor="middle" class="mut">'
                 f'{u:g}c</text>')
    b.append(f'<text x="{pad}" y="{pad-18}" class="lab ink">'
             f'TWO TRUCKS, EACH DOIN\' u, HEAD ON</text>')
    return svg(w, h, "".join(b), "Speeds do not stack the way hay bales do",
               "Closing speed of two objects each moving at u, plotted the arithmetic way "
               "and the relativistic way; the second curve approaches but never reaches c.")


# ------------------------------------------------------------------ gamma
def gamma_curve() -> str:
    w, h, pad = 900, 420, 70
    X = lambda b_: pad + b_ * (w - 2 * pad)
    Y = lambda g: h - pad - min(g, 8.0) / 8.0 * (h - 2 * pad)
    pts = " ".join(f"{X(i/400):.1f},{Y(1/math.sqrt(1-(i/400)**2)):.1f}"
                   for i in range(0, 397))
    b = [f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" class="s"/>',
         f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" class="s"/>',
         f'<polyline points="{pts}" class="sa draw"/>']
    for g in (1, 2, 4, 8):
        b.append(f'<line x1="{pad}" y1="{Y(g):.1f}" x2="{w-pad}" y2="{Y(g):.1f}" class="sm"/>')
        b.append(f'<text x="{pad-8}" y="{Y(g)+4:.1f}" text-anchor="end" class="mut">×{g}</text>')
    for b_ in (0.5, 0.9, 0.99):
        g = 1 / math.sqrt(1 - b_ ** 2)
        b.append(f'<circle cx="{X(b_):.1f}" cy="{Y(g):.1f}" r="4.5" class="acc"/>')
        b.append(f'<text x="{X(b_)-8:.1f}" y="{Y(g)-10:.1f}" text-anchor="end" class="ink">'
                 f'{b_:g}c → ×{g:.2f}</text>')
    for b_ in (0, .25, .5, .75, 1):
        b.append(f'<text x="{X(b_):.1f}" y="{h-pad+22}" text-anchor="middle" class="mut">'
                 f'{b_:g}c</text>')
    b.append(f'<text x="{pad}" y="{pad-18}" class="lab ink">'
             f'HOW MANY TIMES HEAVIER THE GOIN\' GETS — γ = 1/√(1−v²/c²)</text>')
    return svg(w, h, "".join(b), "The gamma factor",
               "The Lorentz factor against speed; it is near one for everything on the "
               "ladder below light and climbs without bound as v approaches c.")


def main() -> None:
    d = json.loads((ROOT / "data" / "ladder.json").read_text(encoding="utf-8"))
    write("ladder.svg", ladder(d["rungs"]))
    write("mach.svg", mach())
    dr, marks = drag_curve()
    write("drag.svg", dr)
    write("cannonball.svg", cannonball())
    write("addup.svg", addup())
    write("gamma.svg", gamma_curve())

    truck = 2000.0                                          # kg, a pickup
    g99 = 1 / math.sqrt(1 - 0.99 ** 2)
    facts = {
        "c": C,
        "hp60": marks[60] / 745.7, "hp80": marks[80] / 745.7, "hp30": marks[30] / 745.7,
        "drag_ratio_80_60": marks[80] / marks[60],
        "drag_ratio_60_30": marks[60] / marks[30],
        "orbit_iss": math.sqrt(G * M_EARTH / (R_EARTH + 420e3)),
        "escape_earth": math.sqrt(2 * G * M_EARTH / R_EARTH),
        "orbit_period_min": 2 * math.pi * math.sqrt((R_EARTH + 420e3) ** 3 / (G * M_EARTH)) / 60,
        "equator_spin": 2 * math.pi * 6378137.0 / 86164.0905,
        "gamma99": g99,
        "ke99_J": (g99 - 1) * truck * C ** 2,
        "truck_kg": truck,
        "world_energy_EJ": 620.0,
        "sum_075": (0.75 + 0.75) / (1 + 0.75 * 0.75),
        "gps_speed_us": -7.2, "gps_grav_us": 45.9,
        "mach_angle_15": math.degrees(math.asin(1 / 1.5)),
    }
    facts["ke99_years_of_world"] = facts["ke99_J"] / (facts["world_energy_EJ"] * 1e18)
    (ROOT / "build" / "facts.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
    print(f"figures → {OUT}  ({len(list(OUT.glob('*.svg')))} svg)  facts → build/facts.json")


if __name__ == "__main__":
    main()
