# Goin' Fast

A dirt-simple explainer about speed, in a country voice, with the arithmetic left in.
Twenty measured speeds from the ground under the house to light itself, what each one
costs, and where the ceiling is.

**Live:** https://nanobotco.github.io/goin-fast/

## The whole thing, dirt simple

1. Fast is always fast *compared to somethin'*. Pick the somethin' first.
2. Holdin' a speed is free. Changin' it costs.
3. Air fights back harder the faster you go — a lot harder.
4. Orbit ain't up. Orbit is sideways, fast enough to keep missin' the ground.
5. There is a top speed. Light. 299,792,458 metres a second.
6. Get near it and your speed quits climbin' — your watch slows down instead.

## What is on it

- **The ladder** — twenty speeds, smallest to biggest, each with its arithmetic and the
  measurement it came off: a racing snail at 0.00275 m/s, Bolt at 12.27, a cheetah at
  25.9, a peregrine at 108, a bullwhip tip at twice the speed of sound, ThrustSSC,
  the SR-71, the X-15, the space station, escape velocity, the Parker Solar Probe, light.
- **Sound** — what the sound barrier is, why the Mach cone has the angle it has, why the
  boom is a strip on the ground rather than an event, and why a whip beat Yeager by a few
  thousand years.
- **Air** — drag goes with the square of speed, power with the cube: 19 hp at 60 mph,
  45 at 80, to shove the same truck-shaped hole through the same still air.
- **Orbit** — Newton's cannonball, integrated from a = −GM/r². Orbital speed at station
  height, escape from the surface, and why the fastest thing ever built got that way by
  falling.
- **The limit** — speeds that will not stack, the gamma factor, the GPS clock correction
  and the 10 km a day it is worth, and what does travel at c.
- **Cheats** — five things that outrun light and break no rule: shadows, scissors, phase
  velocity, the expansion of space, entangled pairs.
- **Reckoner** — four calculators, running in the page.

## Where the numbers come from

`tools/figures.py` computes the orbital and escape speeds, the Mach angle, the drag
figures, the gamma factors and the five cannonball trajectories from the formulas
printed beside them, then writes `build/facts.json`. `tools/site.py` reads that file, so
a sentence and the diagram next to it are the same computation. `tests/test_site.py`
checks the results against published values — NASA's fact sheets, the FAI and FIA
records, CODATA's G — and fails the build on a drift.

Sources are listed at [/sources/](https://nanobotco.github.io/goin-fast/sources/), 34 of
them, numbered, with a link each.

## Build

```
python3 tools/figures.py     # the six diagrams (SVG) and build/facts.json
python3 tools/site.py        # the pages, into build/site/
python3 tests/test_site.py   # the arithmetic, against published values
./publish.sh                 # all of it, checked, into docs/
python3 tools/serve.py 8841  # a local preview, mounted at /goin-fast/
```

Python 3.9 or later, standard library only. The pages are static HTML with the
stylesheet inlined and the diagrams inlined as SVG, so a page is one request.

The hollerin' in the diagrams is CSS, and it stops under
`prefers-reduced-motion: reduce`.

## Licence

- Text, diagrams and data: [CC BY 4.0](LICENSE). Credit line: *Nan · hongdam.net ·
  CC BY 4.0*, with a link to https://nanobotco.github.io/goin-fast/ .
- Code in `tools/`, `js/`, `tests/`: [MIT](LICENSE-CODE).

Made by [Hongdam](https://hongdam.net/), Chiang Rai.
