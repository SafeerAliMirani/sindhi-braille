# -*- coding: utf-8 -*-
"""
Shapes a finger can follow, drawn on the braille dot grid, in a plain .brf.

    python tools/tactile.py --demo --width 38 --lines 25

Why not the embosser's graphics mode: the Everest-D V5 does have one, at 500 dpi
with dots placed to 0.05 mm, but reaching it needs Index's own software or a
graphics-capable braille editor. A plain .brf carries text and nothing else.

So these shapes are drawn on the grid the braille cells already make. Every cell
is two dots across and three down, so a page of W cells by L lines is a grid of
2W by 3L dots, and any of them can be raised. That is coarse, but a triangle
twenty cells wide is thirty centimetres of outline under a finger and there is
no difficulty recognising it.

The grid is not square, and the code does not pretend it is. Within a cell the
dots are 2.5 mm apart; between cells the step is 6.2 mm and between lines
10.0 mm. So a circle drawn by counting dots would come out an egg. Each dot's
real position in millimetres is computed, and the shape is drawn against that.

The advantage over the graphics mode is that this file works on any embosser
anywhere, with no software, no drivers and no format anyone has to support.
"""
import io, math, os, sys

DOT_X   = 2.5    # mm between the two dots across a cell
DOT_Y   = 2.5    # mm between dots down a cell
CELL_X  = 6.2    # mm cell to cell
LINE_Y  = 10.0   # mm line to line

# North American Braille ASCII, the same table the rest of the project uses
BA = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
DOTVAL = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}


def dot_mm(col, row):
    """the real position of dot (col, row) on the page, in millimetres.

    col counts dots across, 0-based: 0 and 1 are the two dots of cell 0.
    row counts dots down: 0, 1, 2 are the three dots of line 0."""
    cell, within = divmod(col, 2)
    line, down = divmod(row, 3)
    return (cell * CELL_X + within * DOT_X,
            line * LINE_Y + down * DOT_Y)


def canvas(width_cells, lines):
    return 2 * width_cells, 3 * lines


def extent(width_cells, lines):
    w, h = canvas(width_cells, lines)
    x, y = dot_mm(w - 1, h - 1)
    return x, y


def _nearest(on, width_cells, lines, x, y):
    """raise the dot closest to a point, if it is close enough to be honest"""
    w, h = canvas(width_cells, lines)
    best, bd = None, 1e9
    for col in range(w):
        for row in range(h):
            dx, dy = dot_mm(col, row)
            d = (dx - x) ** 2 + (dy - y) ** 2
            if d < bd:
                bd, best = d, (col, row)
    if best and bd <= (LINE_Y * 0.75) ** 2:
        on.add(best)


def path(points, width_cells, lines, step=0.8):
    """raise the dots along a path given as millimetre points"""
    on = set()
    for i in range(len(points) - 1):
        (x0, y0), (x1, y1) = points[i], points[i + 1]
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(int(d / step), 1)
        for k in range(n + 1):
            t = k / n
            _nearest(on, width_cells, lines, x0 + t*(x1-x0), y0 + t*(y1-y0))
    return on


def rectangle(x, y, w, h, width_cells, lines):
    return path([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)],
                width_cells, lines)


def square(x, y, side, width_cells, lines):
    return rectangle(x, y, side, side, width_cells, lines)


def triangle(x, y, base, height, width_cells, lines):
    return path([(x, y+height), (x+base, y+height), (x+base/2.0, y), (x, y+height)],
                width_cells, lines)


def circle(cx, cy, r, width_cells, lines, steps=180):
    pts = [(cx + r*math.cos(2*math.pi*k/steps), cy + r*math.sin(2*math.pi*k/steps))
           for k in range(steps + 1)]
    return path(pts, width_cells, lines)


def line(x0, y0, x1, y1, width_cells, lines):
    return path([(x0, y0), (x1, y1)], width_cells, lines)


def to_lines(on, width_cells, lines):
    """the raised dots -> braille ASCII, one string per line"""
    out = []
    for ln in range(lines):
        row = []
        for cell in range(width_cells):
            v = 0
            for d, (dc, dr) in {1: (0, 0), 2: (0, 1), 3: (0, 2),
                                4: (1, 0), 5: (1, 1), 6: (1, 2)}.items():
                if (cell*2 + dc, ln*3 + dr) in on:
                    v |= DOTVAL[d]
            row.append(BA[v])
        out.append(''.join(row).rstrip())
    return out


def merge(*sets):
    out = set()
    for s in sets: out |= s
    return out
