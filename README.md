# Barnsley Fern + Mandelbrot — Fractal Design Lab

An animated **Barnsley Fern** (drawn point-by-point via the chaos game)
growing on top of a dim, slowly "breathing" **Mandelbrot Set** backdrop —
two different fractal-generation techniques combined into one
composition. Colour runs from deep forest green to bright lime, on black.

![Fern + Mandelbrot](fern_bg_static.png)

![Growth animation](fern_bg_growth.gif)

## Fractal Types

- **Barnsley Fern** (foreground) — an Iterated Function System (IFS):
  repeatedly applying one of four randomly-chosen affine transformations
  to a point, with probabilities tuned so the result resembles a real
  fern (Michael Barnsley, 1988).
- **Mandelbrot Set** (background) — the classic escape-time fractal:
  for each point `c` in the complex plane, `z = z² + c` is iterated from
  `z = 0`; how quickly `z` escapes determines the colour.

## Tools, Languages & Libraries

- **Python 3**
- **NumPy** — vectorised chaos-game steps and Mandelbrot escape-time computation
- **Matplotlib** — rendering and animation (`FuncAnimation`)
- **FFmpeg** — encoding the growth animation to `.mp4`

## Setup & Run

```bash
git clone <this-repo-url>
cd barnsley-fern
pip install -r requirements.txt
python barnsley_fern.py
```

This produces:
- `fern_bg_static.png` — fern + Mandelbrot backdrop, final static render
- `fern_bg_growth.mp4` — animated growth (used for the demo video)
- `fern_bg_growth.gif` — lightweight animated preview (shown above)
- `fern_static.png` / `fern_growth.mp4` / `fern_growth.gif` — fern on its own, no backdrop

An additional bonus piece, `ai_logo.py`, spells out "AI" by filling the
letter **A** with a Mandelbrot set and the letter **I** with a fractal
tree, each masked to the glyph shape (see script for details).

## How It Works

**Fern (foreground):** at each step, one of 4 affine transformations is
applied to the current point `(x, y)`:

| Transform | Probability | Role |
|---|---|---|
| f1 | 1% | Stem |
| f2 | 85% | Successively smaller leaflets |
| f3 | 7% | Left leaflet |
| f4 | 7% | Right leaflet |

Repeating this 60,000 times traces out the full fern shape, coloured by
each point's height (`y` value).

**Mandelbrot (background):** rendered once per animation frame at a
slowly oscillating zoom level (a gentle "breathing" effect), dimmed and
desaturated so the fern stays the clear focal point. The sampling
region's aspect ratio is matched to the canvas so the classic
cardioid/bulb shape isn't stretched out of proportion.

## Author

**Romaisa Kashif**
Registration No: *<add your reg number>*
BS Computer Science, NUST

## Academic Integrity

Original implementation written for Design Lab 01 — Designing Using
Fractals. Built with NumPy and Matplotlib (open-source, credited above).
