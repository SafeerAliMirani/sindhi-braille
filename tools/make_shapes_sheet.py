# -*- coding: utf-8 -*-
"""
Sheet 5 — four shapes a finger can follow, and their names in Sindhi.

    python tools/make_shapes_sheet.py --width 38 --lines 25

Writes test-sheets/print-5-shapes.brf and SHAPES-KEY.md.

This is the proof that the guide book can carry figures. Not photographs, which
do not survive being reduced to dots, but the shapes a beginner actually needs:
a square, a triangle, a circle, a rectangle. Those are outlines already, so the
grid loses nothing that matters.

Nothing here needs the embosser's graphics mode or any special software. The
dots are ordinary braille cells, so this file prints on any embosser that reads
a .brf, which is all of them.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import tactile as t
import sindhi_braille as sb


def put(lines, ln, cell, text):
    """write braille for `text` into line `ln`, starting at cell `cell`"""
    cells = sb.translate(text)[0]
    s = ' '.join(''.join(sb.cell_to_ascii(c) for c in g) for g in cells)
    row = list(lines[ln].ljust(cell + len(s)))
    row[cell:cell + len(s)] = list(s)
    lines[ln] = ''.join(row).rstrip()


def build(width=38, height=25):
    sb.load_words()
    W, L = width, height

    shapes = t.merge(
        t.square(8, 5, 52, W, L),                     # top left
        t.triangle(120, 5, 58, 52, W, L),             # top right
        t.circle(34, 133, 26, W, L),                  # lower left
        t.rectangle(112, 112, 72, 44, W, L),          # lower right
    )
    lines = t.to_lines(shapes, W, L)
    while len(lines) < L:
        lines.append('')

    put(lines, 7, 1, 'چورس')
    put(lines, 7, 19, 'ٽڪنڊو')
    put(lines, 17, 1, 'گول')
    put(lines, 17, 19, 'مستطيل')

    brf = '\r\n'.join(lines).rstrip('\r\n') + '\r\n\f'
    out = os.path.join(ROOT, 'test-sheets', 'print-5-shapes.brf')
    io.open(out, 'w', encoding='ascii', newline='').write(brf)
    used = len([l for l in lines if l.strip()])
    widest = max((len(l) for l in lines), default=0)
    print('print-5-shapes.brf  %d lines used, widest %d cells' % (used, widest))
    if widest > W:
        print('  WARNING: wider than the page')

    key = """# Sheet 5 — the shapes

Four shapes, each with its name in Sindhi underneath.

| where | shape | name |
|---|---|---|
| top left | square | چورس |
| top right | triangle | ٽڪنڊو |
| lower left | circle | گول |
| lower right | rectangle | مستطيل |

## What this sheet is for

To find out whether shapes drawn on the braille grid are recognisable by touch,
before a whole book is built on the assumption that they are.

**Give it to him without saying what is on it.** Do not say "there are four
shapes". Ask what he feels. If he names them unprompted, the method works and
the guide book can carry figures.

Then ask the harder questions:

- Is the circle round, or does it feel like an egg? The dots are 2.5 mm apart
  inside a cell and 6.2 mm apart between cells, so a circle drawn by counting
  dots would come out stretched. This one is drawn against the real millimetre
  positions, which should fix it. His fingers will say whether it did.
- Are the corners of the square sharp enough to feel as corners?
- Is the triangle's sloping side a line, or does it feel like steps?
- Is the rectangle clearly *not* a square?

## Why it matters

If the answers are good, the guide book can have geometry in it, produced by the
same software and the same embosser as the text, with no extra tools.

If the sloping lines feel like steps, the answer is bigger shapes, not better
software: a triangle twenty cells across has twice the outline of one at ten, and
the steps get smaller relative to the shape. Tell me which shapes failed and at
what size, and the next sheet will be drawn larger.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
    io.open(os.path.join(ROOT, 'test-sheets', 'SHAPES-KEY.md'), 'w',
            encoding='utf-8', newline='\n').write(key)
    print('SHAPES-KEY.md written')


if __name__ == '__main__':
    a = sys.argv[1:]
    w = int(a[a.index('--width') + 1]) if '--width' in a else 38
    h = int(a[a.index('--lines') + 1]) if '--lines' in a else 25
    build(w, h)
