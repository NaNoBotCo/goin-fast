#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site.py — builds the pages into build/site/.

    SITE_URL=https://nanobotco.github.io/goin-fast python3 tools/site.py

The numbers in the prose come from build/facts.json, which tools/figures.py computes
from the same formulas the diagrams are drawn with.
"""
from __future__ import annotations

import html
import json
import math
import os
import shutil
import sys
import urllib.parse
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet                                                   # noqa: E402
from css import CSS                                            # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "build" / "site"
URL = os.environ.get("SITE_URL", "https://nanobotco.github.io/goin-fast").rstrip("/")
# Root-relative links, built off the mount, because a host that serves /x without
# redirecting to /x/ resolves a relative "../y/" one level too high. See tools/links.py.
BASE = (urllib.parse.urlsplit(URL).path or "") + "/"
TODAY = date.today().isoformat()

LADDER = json.loads((ROOT / "data" / "ladder.json").read_text(encoding="utf-8"))
EXTRA = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
F = json.loads((ROOT / "build" / "facts.json").read_text(encoding="utf-8"))
SRC = {**LADDER["sources"], **EXTRA["sources"]}
ORDER = list(LADDER["sources"]) + list(EXTRA["sources"])
NUM = {k: i + 1 for i, k in enumerate(ORDER)}

MPH = 0.44704
C = F["c"]

NAV = [("", "Home"), ("ladder/", "The ladder"), ("sound/", "Sound"), ("drag/", "Air"),
       ("orbit/", "Orbit"), ("limit/", "The limit"), ("cheats/", "Cheats"),
       ("reckoner/", "Reckoner"), ("sources/", "Sources")]


# ------------------------------------------------------------------ small helpers
def ref(*keys: str) -> str:
    """A superscript pointing at the sources page."""
    out = []
    for k in keys:
        out.append(f'<a href="{up()}sources/#{k}" title="{html.escape(SRC[k][0])}">{NUM[k]}</a>')
    return '<sup class="ref">[' + ", ".join(out) + "]</sup>"


def up() -> str:
    return BASE


def mph(ms: float) -> str:
    v = ms / MPH
    return f"{v:,.0f} mph" if v >= 10 else f"{v:,.1f} mph"


def kmh(ms: float) -> str:
    v = ms * 3.6
    return f"{v:,.0f} km/h" if v >= 10 else f"{v:,.1f} km/h"


def si(ms: float) -> str:
    if ms >= 1e6:
        return f"{ms/1e6:,.1f} million m/s"
    if ms >= 1:
        return f"{ms:,.6g} m/s"
    return f"{ms:.3g} m/s"


def mach(ms: float) -> str:
    return f"Mach {ms/343.0:.2f}"


def fig(name: str, caption: str) -> str:
    art = (ROOT / "build" / "img" / name).read_text(encoding="utf-8")
    return (f'<figure class="fig"><div class="canvas">{art}</div>'
            f'<figcaption>{caption}</figcaption></figure>')


# ------------------------------------------------------------------ page chrome
def page(slug: str, title: str, desc: str, body: str, prev_next: str = "",
         out: str = "") -> None:
    u = up()
    bits = []
    for href, label in NAV:
        here = ' aria-current="page"' if href.rstrip("/") == slug.rstrip("/") else ""
        bits.append(f'<a href="{u}{href}"{here}>{html.escape(label)}</a>')
    nav = "".join(bits)
    canon = f"{URL}/{slug}" if slug else f"{URL}/"
    head = (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)}</title>'
        f'<meta name="description" content="{html.escape(desc)}">'
        f'<link rel="canonical" href="{canon}">'
        f'<link rel="icon" href="{u}icon.svg" type="image/svg+xml">'
        f'<meta property="og:title" content="{html.escape(title)}">'
        f'<meta property="og:description" content="{html.escape(desc)}">'
        f'<meta property="og:type" content="article">'
        f'<meta property="og:url" content="{canon}">'
        f'<meta name="author" content="Nan · hongdam.net">'
        f'<style>{CSS}</style></head><body>'
        f'<header class="top"><div class="wrap">'
        f'<a class="mark" href="{u}">GOIN\' <b>FAST</b></a>'
        f'<nav class="site">{nav}</nav></div></header><main class="wrap">')
    foot = (
        f'{prev_next}</main><footer class="foot"><div class="wrap">'
        f'<p>Goin\' Fast — twenty measured speeds and what each one costs. '
        f'Text and diagrams by Nan, '
        f'<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>; '
        f'the code that builds them, '
        f'<a href="https://github.com/NaNoBotCo/goin-fast">MIT</a>. '
        f'Built {TODAY}. Every figure on this site was computed from the formula '
        f'shown beside it.</p>'
        f'{fleet.row_html("goin-fast")}'
        f'{fleet.support_html()}{fleet.maker_html()}'
        f'</div></footer></body></html>')
    dest = SITE / out if out else (SITE / slug / "index.html" if slug else SITE / "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(head + body + foot, encoding="utf-8")


def pn(prev: tuple[str, str] | None, nxt: tuple[str, str] | None) -> str:
    u = up()
    a = f'<a href="{u}{prev[0]}">← {html.escape(prev[1])}</a>' if prev else "<span></span>"
    b = f'<a href="{u}{nxt[0]}">{html.escape(nxt[1])} →</a>' if nxt else "<span></span>"
    return f'<div class="prev-next">{a}{b}</div>'


# ------------------------------------------------------------------ the pages
def p_index() -> None:
    spin = F["equator_spin"]
    body = f"""
<h1>Goin' Fast<span class="sub">Really, super, duper, extra fast — twenty measured
speeds from the ground under the house to light itself, what each one costs, and where
the ceilin' is.</span></h1>

<div class="box sum" id="short">
<h3>The whole thing, dirt simple</h3>
<p>1. Fast is always fast <em>compared to somethin'</em>. Pick the somethin' first.</p>
<p>2. Holdin' a speed is free. Changin' it costs.</p>
<p>3. Air fights back harder the faster you go — a lot harder.</p>
<p>4. Orbit ain't up. Orbit is sideways, fast enough to keep missin' the ground.</p>
<p>5. There is a top speed. Light. {C:,.0f} metres a second.</p>
<p>6. Get near it and your speed quits climbin' — your <em>watch</em> slows down
instead. That part is measured, not argued.</p>
<p>That is the whole page. The rest is the fun part.</p>
</div>

<p class="lede">Fast ain't a thing you own. It's a thing you are, compared to somethin'
else. Set still on the porch with a glass of tea and you are already doin'
{si(spin)} on the spin of the Earth{ref("nasa-earth")} — {mph(spin)}, out at the
equator — and {si(29780)} around the Sun, and about 230 kilometres every second around
the middle of the galaxy. The tea does not slosh. Nothin' hurts. Y'all been haulin'
this whole time.</p>

<p>That is the first thing about speed and it is the thing that trips people up: a speed
is measured against somethin', and you get to pick. The trooper picks the road. The bird
picks the air. The physicist picks whatever makes the arithmetic shortest.</p>

<p class="pull">Speed is free. It's the <em>changin'</em> of it that costs.</p>

<p>Sittin' at 29,780 metres a second costs nothin' — no fuel, no noise, no wind in your
hair. What costs is gettin' from one speed to another, and what you have to shove out of
the way while you do it. Three bills come due, in this order:</p>

<div class="box sum">
<h3>The three bills</h3>
<p><b>Air.</b> Push through it twice as fast and it pushes back four times as hard, and
you spend eight times the horsepower doin' it. <a href="{up()}drag/">The cube law</a>
is why your truck drinks at eighty.</p>
<p><b>Ground.</b> To quit fallin' on it you have to go sideways fast enough to keep
missin' it — {si(F["orbit_iss"])} at the height the space station flies.
<a href="{up()}orbit/">Orbit</a> is not up. Orbit is sideways.</p>
<p><b>The ceilin'.</b> There is one, it is {C:,.0f} metres a second, and it does not
haggle. Past a certain point the speed stops goin' up and your <em>watch</em> starts
goin' slow instead. <a href="{up()}limit/">Here is what that costs.</a></p>
</div>

{fig("ladder.svg", "Twenty rungs, each notch ten times the last. From the Atlantic "
     "gettin' wider to light itself is eighteen powers of ten.")}

<h2>Start here</h2>
<ul class="cards">
<li><h3><a href="{up()}ladder/">The ladder</a></h3><p>Twenty speeds, smallest to
biggest, each one with the arithmetic and who measured it. Snail to light.</p></li>
<li><h3><a href="{up()}sound/">The crack of the whip</a></h3><p>Why a bullwhip pops,
why thunder lags, and why the sound barrier was never a wall — it was your own racket
pilin' up in front of you.</p></li>
<li><h3><a href="{up()}drag/">The air tax</a></h3><p>{F["hp60"]:.0f} horsepower at
sixty, {F["hp80"]:.0f} at eighty, to shove the same truck-shaped hole through the same
still air.</p></li>
<li><h3><a href="{up()}orbit/">Fallin' and missin'</a></h3><p>Newton put a cannon on a
mountain in 1728 and explained satellites a quarter thousand years before there
were any.</p></li>
<li><h3><a href="{up()}limit/">The ceilin'</a></h3><p>Two trucks doin' three-quarters
light speed, head on, close at {F["sum_075"]:.2f}c. Not 1.5. Here is why, and what
it does to a watch.</p></li>
<li><h3><a href="{up()}cheats/">Things that cheat</a></h3><p>A shadow on the barn wall
can outrun light and break no rule at all. Five of these, and what is moving in
each.</p></li>
<li><h3><a href="{up()}reckoner/">The reckoner</a></h3><p>Four calculators. How fast
you are goin' settin' still, what the air costs, how two speeds add, how slow your
watch runs.</p></li>
</ul>
"""
    page("", "Goin' Fast — a plain-spoken explainer about speed",
         "Twenty measured speeds from continental drift to light, the three things that "
         "make going fast cost, and four calculators. Every figure computed from the "
         "formula shown.", body, pn(None, ("ladder/", "The ladder")))


def p_ladder() -> None:
    rows = []
    for r in LADDER["rungs"]:
        ms = r["ms"]
        alt = ""
        if ms >= 1:
            alt = f"{mph(ms)} · {kmh(ms)}"
            if 20 <= ms <= 4e6:
                alt += f" · {mach(ms)}"
        else:
            alt = f"{ms*3.6*1000:.3g} mm/s" if ms >= 1e-6 else "slower than the eye sees"
        rows.append(
            f'<li><div class="v"><b>{si(ms)}</b>{html.escape(alt)}</div>'
            f'<div><h3>{html.escape(r["name"])}{ref(r["src"])}</h3>'
            f'<p>{html.escape(r["say"])}</p>'
            f'<p class="show">{html.escape(r["show"])}</p></div></li>')
    body = f"""
<h1>The ladder<span class="sub">Twenty speeds, each rung about ten times the one below
it. Where a number is arithmetic off somebody's measurement, the arithmetic is printed
under it and the measurement is linked.</span></h1>

{fig("ladder.svg", "The same twenty, on a log scale. A straight ruler cannot show both "
     "a snail and light, so each step along the bottom is a factor of ten.")}

<p>Eighteen powers of ten separate the slowest thing here from the fastest. That is the
same gap as between a second and thirty billion years, which is why the picture needs a
log scale and why your gut is no use above about the third rung.</p>

<ol class="rungs">{''.join(rows)}</ol>

<div class="box">
<h3>What the numbers do not say</h3>
<p>A record is a measured run, under rules, witnessed. A cheetah does not care about
rules, so its number came off a collar in the field and is the best anyone has caught,
not the best there is. A bullwhip tip has been filmed past Mach 2 in a laboratory and
the number depends on the whip and the arm. Take the rungs as the order of things, which
is solid, rather than as the last word on any one line.</p>
</div>
"""
    page("ladder/", "The ladder of speed — snail to light",
         "Twenty measured speeds with their arithmetic and sources, from continental "
         "drift at 7.9e-10 m/s to light at 299,792,458 m/s.", body,
         pn(("", "Home"), ("sound/", "Sound")))


def p_sound() -> None:
    body = f"""
<h1>The crack of the whip<span class="sub">Sound goes {si(343)} through the air out
front. Beat it and you leave your own racket behind — and that is the whole of the
sound barrier.</span></h1>

<p class="lede">Lightning flashes. You count — one Mississippi, two — and thunder comes
at five seconds to the mile. That count is the speed of sound and you have been
measuring it since you were a kid: about {si(343)} in dry air at room
temperature{ref("speed-of-sound")}, slower when it is cold, because sound in air is
nothin' but the air bumpin' into itself, and cold air bumps lazier.</p>

<h2>What the barrier actually is</h2>

<p>Anything movin' through air makes pressure waves and they run out ahead at the speed
of sound, tellin' the air up yonder to get out of the way. That is why air flows around
a slow airplane instead of pilin' up on it — it got word.</p>

<p>Go faster than the news and the news stops arriving. The air out front learns about
you when you hit it. The waves you already made cannot get away, so they stack into one
shock, and that stack is what folks called a barrier. Nothing solid about it. It is
paperwork that did not get delivered.</p>

{fig("mach.svg", f"Each thin ring is the noise made one second earlier, spreading at "
     f"343 m/s. At Mach 1.5 the source outruns them and they share a tangent — a cone "
     f"of half-angle {F['mach_angle_15']:.1f}°, since sin μ = 1/M.")}

<p>The cone drags along behind. When its edge sweeps across your yard you hear the boom
— not once at the moment of breakin' through, but continuously, anywhere the cone
touches ground. A supersonic airplane lays a strip of boom about a mile wide for every
thousand feet of altitude, the whole way it flies{ref("nasa-sonicboom")}. That strip is
why they are not allowed over land in most places.</p>

<h2>The first thing anybody made go supersonic was a whip</h2>

<p>Chuck Yeager got the credit in 1947 with a rocket plane{ref("yeager")}. A drover with
a bullwhip beat him by a few thousand years and did not know it.</p>

<p>The physics is a taper. A whip is thick at the handle and thin at the end, and the
energy you put in the thick part has to keep goin' when the rope runs out of mass to
carry it. Same energy, less and less whip, so the little bit that is left goes faster
and faster. Goriely and McMillen ran the numbers in 2002 and found the tip passes twice
the speed of sound{ref("goriely-whip")}. The crack is a sonic boom you can hold in
your hand.</p>

<div class="box">
<h3>Three ways to hear this for yourself</h3>
<p><b>Count the thunder.</b> Seconds between flash and rumble, divided by five, gives
miles. Divided by three gives kilometres. You are timing 343 metres a second.</p>
<p><b>Listen to a rifle downrange.</b> A .30-06 leaves the muzzle around
{si(853)} — {mach(853)}{ref("saami")}. Stand off to the side and safe and you hear two
noises: the bullet's own boom arriving first from close by, then the powder's bang
from the gun.</p>
<p><b>Watch a jet land.</b> On approach it is subsonic and quiet-ish, because the air
ahead still gets the word.</p>
</div>

<h2>Why the barrier was hard anyway</h2>

<p>Nothing was solid about it, but something was true about it: right around Mach 1 the
drag on a wing spikes, and where the shock sits on the wing moves, so the controls
change their mind about what they do. Early airplanes went into the transonic band and
came out with the stick doing the opposite of what it had done a minute before. Men died
of that before the shape of a wing for those speeds was worked out. The barrier was
never a wall in the air. It was a wall in the engineering.</p>

<p>Fifty years on, the standing record for an air-breathing aeroplane with a person in
it is still {si(980.4)} — the SR-71, 1976{ref("fai-sr71")} — and the fastest car is
still {si(341.1)}, ThrustSSC on the salt in 1997{ref("thrustssc")}. Going fast in air
gets expensive in a hurry, and the next page is the reason.</p>
"""
    page("sound/", "The sound barrier, and the whip that beat it",
         "Sound goes 343 m/s; a bullwhip tip goes twice that. What the sound barrier is, "
         "why the Mach cone has the angle it has, and why the boom is a strip not an "
         "event.", body, pn(("ladder/", "The ladder"), ("drag/", "Air")))


def p_drag() -> None:
    body = f"""
<h1>The air tax<span class="sub">Twice the speed, four times the shove, eight times the
horsepower. This one law explains your gas mileage, the shape of a record car, and why
a bicycle racer hides behind another one.</span></h1>

<p class="lede">Air weighs somethin'. About 1.2 kilograms a cubic metre at sea level,
which sounds like nothin' until you work out how many cubic metres a truck shoulders
aside in an hour at seventy — better than a hundred and fifty thousand of them, near
two hundred tonnes of air, shoved.</p>

<p>The force it takes goes with the <em>square</em> of the speed:</p>

<p class="pull eq">F = ½ · ρ · v² · C<sub>d</sub> · A</p>

<p>ρ is how heavy the air is, v is how fast you are goin', A is how big a hole you are
punchin', and C<sub>d</sub> is a number for how ugly the shape is — about 0.40 for a
pickup, 0.24 for a slick sedan, near 0.04 for a shape drawn for the purpose{ref("hoerner")}.</p>

<p>But the <em>power</em> — the horsepower, the fuel, the bill — goes with the
<strong>cube</strong>, because power is force times speed. Shoving four times as hard
while going twice as fast is eight times the work per second:</p>

{fig("drag.svg", "Power spent on air alone against speed, for a pickup-sized hole "
     "(Cd 0.40, 3 m² frontal, sea-level air). Tyres and driveline are extra.")}

<div class="scroll"><table>
<tr><th>Speed</th><th>Air shoved aside</th><th>Horsepower, air only</th><th>Against 30 mph</th></tr>
<tr><td>30 mph</td><td class="n">{0.5*1.225*(30*MPH)**2*0.4*3:,.0f} N</td>
    <td class="n">{F["hp30"]:.1f} hp</td><td class="n">1×</td></tr>
<tr><td>60 mph</td><td class="n">{0.5*1.225*(60*MPH)**2*0.4*3:,.0f} N</td>
    <td class="n">{F["hp60"]:.1f} hp</td><td class="n">{F["drag_ratio_60_30"]:.0f}×</td></tr>
<tr><td>80 mph</td><td class="n">{0.5*1.225*(80*MPH)**2*0.4*3:,.0f} N</td>
    <td class="n">{F["hp80"]:.1f} hp</td><td class="n">{F["hp80"]/F["hp30"]:.0f}×</td></tr>
</table></div>

<p>Doubling thirty to sixty costs exactly {F["drag_ratio_60_30"]:.0f} times the power.
Going from sixty to eighty — a third again as fast — costs
{F["drag_ratio_80_60"]:.1f} times. That is the whole story of your gas gauge on the
interstate, and the EPA puts the same thing in money: past about fifty, every five
miles an hour you add costs you like paying another fifteen to twenty cents a
gallon{ref("epa-mileage")}.</p>

<h2>What the cube law makes people do</h2>

<p><b>Draft.</b> Sit in the hole somebody else already punched and your own bill drops
by a third or better. Ducks do it, bicycle racers do it, and stock cars do it at two
hundred miles an hour with a foot of air between them.</p>

<p><b>Get skinny, not slick.</b> The frontal area A is a plain multiplier and the
cheapest thing to cut. A record car is needle-thin because every square metre you
delete is a square metre you never pay for again.</p>

<p><b>Go where the air is thin.</b> ρ falls off with height. At sixty thousand feet
there is about a tenth the air, so a tenth the drag at the same speed — which is exactly
why the SR-71 cruised up where the sky goes dark, and why nothing fast flies low for
long.</p>

<p><b>Quit the air entirely.</b> Above a hundred kilometres or so there is almost
nothing left to shove, and that is where the numbers on the ladder stop being thousands
and start being tens of thousands. <a href="{up()}orbit/">Which is the next page.</a></p>

<div class="box">
<h3>The bill you cannot cut</h3>
<p>Rolling resistance — tyres flexing — is roughly flat with speed, so it dominates
down low and disappears into the noise up high. Somewhere around fifty miles an hour in
an ordinary car the air takes over and never gives it back. Below that, a heavy car
costs you. Above it, a wide one does.</p>
</div>
"""
    page("drag/", "The air tax — why speed costs the cube",
         "Drag rises with the square of speed and power with the cube: 19 hp at 60 mph, "
         "45 at 80, for the same truck-shaped hole. Worked from ½ρv³CdA.", body,
         pn(("sound/", "Sound"), ("orbit/", "Orbit")))


def p_orbit() -> None:
    body = f"""
<h1>Fallin' and missin'<span class="sub">Orbit is not about goin' up. Up is the easy
part and it does not stay bought. Orbit is about goin' <em>sideways</em> fast enough
that the ground curves away as quick as you drop toward it.</span></h1>

<p class="lede">Newton explained satellites in 1728, which is two hundred and twenty-nine
years before there was one{ref("principia")}. He drew a cannon on a mountain so tall it
was above the weather and fired it level. Small charge: the ball arcs over and lands in
the next county. Bigger charge: the next country. Big enough charge, and the ball falls
toward the Earth at the same rate the Earth is curving out from under it, and it never
lands at all. It comes around and hits you in the back of the head.</p>

{fig("cannonball.svg", "Every curve here was integrated from a = −GM/r², fired level "
     "off a 300 km hill. The slow ones strike. The red one closes.")}

<h2>The number</h2>

<p>Set the fall equal to the curve and the speed drops out of the arithmetic:</p>

<p class="pull eq">v = √(GM / r)</p>

<p>G is the constant of gravity{ref("codata")}, M is the mass of the Earth, r is how far
you are from the middle of it — not from the ground, from the <em>middle</em>. At the
height the space station flies, about 420 kilometres up, that comes to
{si(F["orbit_iss"])}{ref("nasa-iss")}, which is {mph(F["orbit_iss"])}, which is
{mach(F["orbit_iss"])} if there were any air left to measure it against. One lap in
{F["orbit_period_min"]:.1f} minutes. Sixteen sunrises a day.</p>

<p>Farther out is slower — a bigger r means a smaller v. The Moon is doin' about a
kilometre a second and takes a month. A satellite parked over one spot on the equator
sits at 35,786 km and takes exactly a day, which is the whole point of it.</p>

<h2>Quittin' entirely</h2>

<p>Go faster still and the loop opens up. Put in a factor of two under the root:</p>

<p class="pull eq">v = √(2GM / r) = {si(F["escape_earth"])} at the ground</p>

<p>Throw somethin' that fast and it does not come back — no engine after the throw, no
fuel, nothing. It coasts out forever, slowin' the whole way, never quite stopping. That
is escape velocity{ref("nasa-earth")}, and notice what it is not: it is not a speed you
have to hold. It is a speed you have to <em>have</em>, once, and then you are done
paying.</p>

<div class="box">
<h3>Why nobody launches at escape velocity</h3>
<p>Because of the air. Eleven kilometres a second at sea level would cook a rocket like
a meteor — and meteors are exactly the demonstration. A rocket goes up slow through the
thick part, where the <a href="{up()}drag/">cube law</a> is brutal, then turns sideways
and does its real accelerating up high where there is nothing left to shove. Going up
is not the mission. Going up is just gettin' out of the way of the air so you can go
sideways in peace.</p>
</div>

<h2>The fastest thing we ever built did it by fallin'</h2>

<p>The Parker Solar Probe touched {si(192000)} — about {kmh(192000)} — in December
2024{ref("nasa-parker")}. No engine on Earth did that. The Sun did. The probe gave up
speed at Venus seven times to drop its orbit closer in, and then it <em>fell</em>, the
same way a rock falls off a barn, except the barn is the Sun and the drop is ninety
million miles deep. Falling is free. Everything fast in the solar system is fast because
it fell a long way, and the ones we call slow are the ones that stayed up.</p>
"""
    page("orbit/", "Orbit is sideways — fallin' and missin'",
         "Why orbital speed is √(GM/r) = 7,661 m/s at station height, why escape is the "
         "same with a 2 under the root, and why the fastest thing ever built got that "
         "way by falling.", body, pn(("drag/", "Air"), ("limit/", "The limit")))


def p_limit() -> None:
    gps_net = F["gps_grav_us"] + F["gps_speed_us"]
    drift_km = gps_net * 1e-6 * C / 1000
    body = f"""
<h1>The ceilin'<span class="sub">{C:,.0f} metres a second. Not a speed limit anybody
set, not a limit of engines or money or nerve. Past a certain point the speed quits
going up and your watch starts going slow instead.</span></h1>

<p class="lede">Here is the strange part, and it is the whole of it: light goes the same
speed past everybody. Run at it, run away from it, sit still — the number you measure
comes out {C:,.0f} metres a second every time{ref("einstein-1905")}. That cannot be true
of hay bales and it is not true of trucks, but it is true of light, it has been measured
to death for a hundred and twenty years, and everything else on this page is the price
of it being true.</p>

<h2>Speeds do not stack</h2>

<p>Two trucks come at each other, each doin' seventy. Closin' speed a hundred and forty,
and that is near enough correct that the highway patrol uses it. It is not exactly
correct. The exact version is:</p>

<p class="pull eq">sum = (u + v) / (1 + uv/c²)</p>

<p>At seventy miles an hour that correction is a few parts in a quadrillion — the
difference does not show up until a good deal past the last rung on the ladder. Take
two trucks at three-quarters the speed of light, though, head on, and they do not close
at one and a half c. They close at {F["sum_075"]:.2f}c.</p>

{fig("addup.svg", "Two objects each doing u, head on. Dashed is how you would reckon "
     "it. Solid is how it comes out. The solid one gets closer and closer to c and "
     "does not cross.")}

<p>Feed light into that formula and it spits light back out, at any u you like. That is
the ceiling doing its work: you can shove forever and get closer forever and not
arrive.</p>

<h2>So where does the shovin' go?</h2>

<p>Into the γ — gamma — a single number that measures how much the world has stopped
behaving arithmetically:</p>

<p class="pull eq">γ = 1 / √(1 − v²/c²)</p>

{fig("gamma.svg", "Gamma against speed. It sits at 1.000 for everything on the ladder "
     "below light, then leaves the page.")}

<p>At walking pace, γ is 1.0000000000000001. At half light speed it is 1.15. At 0.99c it
is {F["gamma99"]:.2f}, and getting a two-tonne pickup to that speed takes
{F["ke99_J"]:.2e} joules — {F["ke99_years_of_world"]:.1f} times everything the human
race burned, in every form, for all purposes, in the year 2024{ref("energy-institute")}.
For one truck. To not quite get there.</p>

<h2>Your watch runs slow and this is measured, not argued</h2>

<p>The same γ says a moving clock ticks slow by that factor. It sounds like a story
until you look at what it costs to ignore it.</p>

<div class="box sum">
<h3>GPS, which would not work otherwise</h3>
<p>The satellites are doing about 3,874 metres a second, so their clocks lose
{abs(F["gps_speed_us"]):.1f} microseconds a day to speed. They are also twenty thousand
kilometres up where gravity is weaker, so they gain {F["gps_grav_us"]:.1f} microseconds
a day to that{ref("ashby-gps")}. Net: <b>{gps_net:+.1f} microseconds a day</b>, fast.</p>
<p>A GPS fix is a light-travel-time measurement, so an error in the clock is an error in
your position at {C:,.0f} metres a second. {gps_net:.1f} microseconds of drift is
<b>{drift_km:.1f} kilometres</b> of wrong, and it is {drift_km:.1f} kilometres more
wrong every day. The satellites are built with their clocks deliberately set off-rate
before launch so that they run correct once they are up there. The phone in your pocket
is a working relativity experiment that gets checked by a hundred million people
daily.</p>
</div>

<p>It has also been measured directly, the old-fashioned way. Hafele and Keating flew
caesium clocks around the world on airliners in 1971 and brought them home reading
different{ref("hafele-keating")}. In 2010 the NIST group did it with a clock carried up
one-third of a metre, and with an atom moving about ten metres a
second{ref("chou-clocks")} — walking pace, and the effect showed.</p>

<h2>What actually goes the speed limit</h2>

<p>Light does, in vacuum. Anything with no mass does. Gravity does, and that has been
checked: on 17 August 2017 two neutron stars collided, and the shiver in spacetime and
the gamma rays from the same event arrived 1.7 seconds apart after 130 million years of
travel{ref("gw170817")}. Two signals, a hundred and thirty million years, under two
seconds between them. The speeds agree to about a part in a thousand trillion.</p>

<p>Everything with mass is stuck below. Not almost. Below. And the closer you get, the
more the difference shows up as the clock slowing rather than the ground going by — go
fast enough and a trip that takes a thousand years from the porch takes a year in the
cab. The ceiling does not stop you crossing the galaxy. It only stops you coming home to
anybody you knew.</p>
"""
    page("limit/", "The ceilin' — 299,792,458 metres a second",
         "Why speeds do not add, what gamma costs, how GPS would drift 10 km a day "
         "without the correction, and what actually travels at c.", body,
         pn(("orbit/", "Orbit"), ("cheats/", "Cheats")))


def p_cheats() -> None:
    body = f"""
<h1>Things that cheat<span class="sub">Five things that go faster than light, or look
like it, and break no rule at all. In each one the trick is the same: ask what is
actually movin', and whether you could send a message with it.</span></h1>

<p class="lede">The speed limit is not on <em>motion</em>. It is on cause getting from
here to there — on one thing making another thing happen. Plenty of patterns beat it.
A pattern cannot carry a message, so nobody minds.</p>

<h3>1. The shadow on the barn</h3>
<p>Hold your hand in front of a flashlight and throw a shadow on a barn wall a mile off.
Twitch your wrist. The shadow's edge sweeps the wall at whatever speed the geometry
says, and if the wall is far enough it sweeps faster than light, easy.</p>
<p><b>What is movin':</b> nothing. There is no object called the shadow. The wall is
dark at one spot, then dark at another spot, and the news that made each spot dark came
from your hand at exactly light speed, no quicker. You cannot signal the far end of the
barn any faster than the near end. Same trick works with a laser pointer swept across
the face of the Moon — the dot outruns light, the photons do not.</p>

<h3>2. Scissors</h3>
<p>A very long pair of scissors, closing. The crossing point of the blades runs out
toward the tips faster and faster, and with long enough blades it goes superluminal.</p>
<p><b>What is movin':</b> a point of intersection, which is a place, not a thing. And
the scissors cheat a second time: real steel does not close rigidly. When you squeeze the
handle, the news travels up the blade at the speed of sound in steel — about five
thousand metres a second, which is sixty thousand times slower than the limit you were
worried about.</p>

<h3>3. The wave that outruns its own light</h3>
<p>In some materials the crests of a light wave move faster than c. This is the phase
velocity, it is a measured, ordinary thing, and it is not a loophole: the crests carry
no information, because a pure endless wave says the same thing forever. Chop the wave
to make it say something and the chop — the envelope, the front — travels at or below c.
Any actual message rides the front.</p>

<h3>4. Space itself</h3>
<p>Distant galaxies recede from us faster than light and they are not moving. The space
between is getting bigger, everywhere at once, and far enough away there is enough
between-ness accumulating per second to beat c{ref("hubble-law")}. Nothing is being
pushed. Nothing local exceeds anything. The rule is about motion <em>through</em>
space, and expansion is not that — which is also the only known way anybody could
get somewhere faster than light, and the arithmetic for it wants a kind of matter
nobody has found{ref("alcubierre")}.</p>

<h3>5. The entangled pair</h3>
<p>Two particles prepared together, carried apart, measured. The outcomes match, and
they match whether the measurements happen a mile apart or a light-year apart, with no
time for a signal between them.</p>
<p><b>What is movin':</b> still nothing. Each side alone sees plain noise. The
correlation only shows up when the two sides compare notes, and comparing notes takes a
phone call, and the phone call goes at light speed like everything else{ref("epr-nosignal")}.
You cannot make your side come out heads on purpose. The universe is coordinated, and
it is not a telegraph.</p>

<div class="box sum">
<h3>The test, every time</h3>
<p>Ask: could I use this to send one bit of news, of my choosing, to somebody, sooner
than light could carry it? If the answer is no, the thing can go as fast as the geometry
allows and nobody in physics loses any sleep. So far the answer has been no every time
anybody has checked.</p>
</div>
"""
    page("cheats/", "Five things that beat light and break no rule",
         "Shadows, scissors, phase velocity, the expansion of space and entangled pairs "
         "— what is actually moving in each, and why none of them carries a message.",
         body, pn(("limit/", "The limit"), ("reckoner/", "Reckoner")))


def p_reckoner() -> None:
    body = f"""
<h1>The reckoner<span class="sub">Four calculators. They run in the page — the
arithmetic is printed under each one so you can check it on paper.</span></h1>

<div class="calc" id="still">
<h3>How fast are you goin' settin' still?</h3>
<label for="lat">Your latitude, degrees (Nashville 36, Chiang Mai 18.8, Reykjavík 64)</label>
<input id="lat" type="number" value="36" min="-90" max="90" step="0.1">
<div class="out" id="still-out"></div>
</div>

<div class="calc" id="air">
<h3>What the air is costin' you</h3>
<div class="grid2">
<div><label for="v">Speed, mph</label><input id="v" type="number" value="70" min="1" max="800"></div>
<div><label for="cd">Drag coefficient</label>
<select id="cd"><option value="0.40">pickup, 0.40</option>
<option value="0.32">SUV, 0.32</option><option value="0.27">sedan, 0.27</option>
<option value="0.24">slick sedan, 0.24</option><option value="0.90">motorcycle + rider, 0.90</option>
<option value="0.05">record streamliner, 0.05</option></select></div>
<div><label for="area">Frontal area, m²</label><input id="area" type="number" value="3.0" step="0.1" min="0.1"></div>
<div><label for="alt">Altitude, m</label><input id="alt" type="number" value="0" step="100" min="0" max="20000"></div>
</div>
<div class="out" id="air-out"></div>
</div>

<div class="calc" id="add">
<h3>Addin' two speeds, the correct way</h3>
<label for="u">First, as a fraction of light speed</label>
<input id="u" type="range" min="0" max="1" step="0.001" value="0.75">
<label for="w">Second, as a fraction of light speed</label>
<input id="w" type="range" min="0" max="1" step="0.001" value="0.75">
<div class="out" id="add-out"></div>
</div>

<div class="calc" id="clock">
<h3>How slow does the watch run?</h3>
<label for="b">Speed, as a fraction of light speed</label>
<input id="b" type="range" min="0" max="0.999999" step="0.000001" value="0.5">
<div class="out" id="clock-out"></div>
</div>

<div class="box">
<h3>Where these come from</h3>
<p>The porch speed is the circumference of your line of latitude divided by a sidereal
day, plus the Earth's orbit, plus the Sun's trip around the galaxy — each one measured
against a different thing, which is the point of the first page.</p>
<p>The air cost is P = ½ρv³C<sub>d</sub>A with ρ falling off by the standard
atmosphere. It is the air only: tyres, driveline and hills are on top.</p>
<p>The other two are (u+v)/(1+uv/c²) and γ = 1/√(1−v²/c²), which is the whole of
<a href="{up()}limit/">the ceilin'</a> in two lines.</p>
</div>

<script>{(ROOT / "js" / "reckoner.js").read_text(encoding="utf-8")}</script>
"""
    page("reckoner/", "The reckoner — four speed calculators",
         "How fast you are moving sitting still, what air drag costs at any speed, how "
         "two near-light speeds add, and how much a moving clock loses.", body,
         pn(("cheats/", "Cheats"), ("sources/", "Sources")))


def p_sources() -> None:
    items = []
    for k in ORDER:
        name, url = SRC[k]
        items.append(f'<li id="{k}" value="{NUM[k]}">{html.escape(name)}. '
                     f'<a href="{html.escape(url)}" rel="noopener">{html.escape(url)}</a></li>')
    body = f"""
<h1>Sources<span class="sub">{len(ORDER)} of them. A number in the text points
here.</span></h1>

<p>Where a rung on the ladder is arithmetic off a published measurement — miles an hour
turned into metres a second, a course record turned into a speed — the arithmetic is
printed under the rung and the measurement is what is linked here.</p>

<ol class="sources">{''.join(items)}</ol>

<h2>What was computed rather than looked up</h2>
<p>Orbital and escape speeds, the Mach cone angle, the drag and power figures, the
gamma factors, the energy to accelerate a two-tonne truck, and the five cannonball
trajectories were all computed in <code>tools/figures.py</code> from the formulas
printed beside them, using G from CODATA{ref("codata")} and the Earth's mass and radius
from the NASA fact sheet{ref("nasa-earth")}. The diagrams are drawn from those same
computations, so a figure and the sentence beside it cannot drift apart.</p>

<h2>Reuse</h2>
<p>Text and diagrams are <a href="https://creativecommons.org/licenses/by/4.0/">CC BY
4.0</a> — take them anywhere, keep the credit line: <i>Nan · hongdam.net · CC BY 4.0</i>,
with a link back to <a href="{URL}/">{URL}/</a>. The build code is MIT. The
repository is at <a href="https://github.com/NaNoBotCo/goin-fast">github.com/NaNoBotCo/goin-fast</a>.</p>
"""
    page("sources/", "Sources", "Every source cited on the site, numbered, with links.",
         body, pn(("reckoner/", "Reckoner"), None))


def p_404() -> None:
    body = """
<h1>Went past it<span class="sub">You were goin' too fast and this page was not
there.</span></h1>
<p>Try <a href="__B__">the front</a>, or <a href="__B__ladder/">the ladder</a>.</p>
""".replace("__B__", BASE)
    page("", "Not here", "Page not found.", body, out="404.html")


# ------------------------------------------------------------------ machine files
def machine_files() -> None:
    pages = [f"{URL}/" if not h else f"{URL}/{h}" for h, _ in NAV]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in pages:
        sm.append(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>")
    sm.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")

    roster = fleet.load()
    maps = "\n".join(f"Sitemap: {s['sitemap']}" for s in roster["sites"] if s.get("sitemap"))
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n{maps}\n", encoding="utf-8")

    rungs = "\n".join(f"- {r['name']}: {r['ms']:g} m/s ({r['show']})" for r in LADDER["rungs"])
    (SITE / "llms.txt").write_text(f"""# Goin' Fast

> A plain-spoken explainer about speed: twenty measured speeds from continental drift to
> light, what each one costs, and where the limit is. Text and diagrams CC BY 4.0, code MIT.

Site: {URL}/
Repository: https://github.com/NaNoBotCo/goin-fast
Built: {TODAY}

## Pages
{chr(10).join(f"- {label}: {URL}/{h}" for h, label in NAV)}

## The ladder, in metres per second
{rungs}

## Computed here, not looked up
Orbital speed at 420 km: {F["orbit_iss"]:.1f} m/s. Escape from the surface:
{F["escape_earth"]:.1f} m/s. Orbital period: {F["orbit_period_min"]:.2f} min. Equatorial
spin: {F["equator_spin"]:.2f} m/s. Drag power for Cd 0.40 / 3 m²: {F["hp30"]:.2f} hp at
30 mph, {F["hp60"]:.2f} at 60, {F["hp80"]:.2f} at 80. gamma at 0.99c: {F["gamma99"]:.4f}.
Kinetic energy of 2000 kg at 0.99c: {F["ke99_J"]:.4g} J. 0.75c + 0.75c = {F["sum_075"]:.4f}c.
Mach cone half-angle at Mach 1.5: {F["mach_angle_15"]:.3f} degrees.

## Terms
Text, diagrams and data: CC BY 4.0, credit "Nan · hongdam.net · CC BY 4.0" with a link
to {URL}/. Code: MIT.
""", encoding="utf-8")

    (SITE / "humans.txt").write_text(
        f"/* the people */\nBuilt by Nan · hongdam.net · Chiang Rai\n"
        f"Contact: {fleet.load()['contact']}\n\n/* the site */\n"
        f"Static HTML, no framework. Diagrams drawn by tools/figures.py from the "
        f"formulas they show.\nLast built: {TODAY}\n", encoding="utf-8")

    (SITE / ".basepath").write_text(BASE, encoding="utf-8")

    # the roster into the machine files: fleet.json, llms.txt, robots.txt, humans.txt
    fleet.decorate(SITE, "goin-fast")

    (SITE / "icon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" fill="#b7222a"/>'
        '<path d="M8 44h30M4 32h34M12 20h26" stroke="#f6efe3" stroke-width="5" '
        'stroke-linecap="round"/>'
        '<path d="M40 14l18 18-18 18z" fill="#e08a1e"/></svg>', encoding="utf-8")


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    p_index(); p_ladder(); p_sound(); p_drag(); p_orbit(); p_limit(); p_cheats()
    p_reckoner(); p_sources()
    shutil.copytree(ROOT / "build" / "img", SITE / "img")
    machine_files()
    p_404()
    n = len(list(SITE.rglob("index.html")))
    print(f"build/site ← {n} pages, {sum(f.stat().st_size for f in SITE.rglob('*'))//1024} KB")


if __name__ == "__main__":
    main()
