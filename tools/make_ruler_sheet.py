# -*- coding: utf-8 -*-
"""
Sheet 0 — how many cells actually fit on the paper you cut.

    python make_ruler_sheet.py            # writes test-sheets/print-0-ruler.brf

Everything else in this project can be worked out on a desk. This cannot. The
usable width of a page is the paper minus whatever border the embosser cannot
reach, and that border belongs to the machine, not to the standard. Guessing it
and printing a hundred sheets is how words end up split across lines.

So this sheet does not assert a width. It prints bars of solid cells at eight
widths, from 44 down to 30, each on its own line. Emboss it once on the paper you
have actually cut, and the answer is the widest bar that comes out as ONE line.
A bar too wide for the paper wraps, and leaves a short stub on the line below,
which is obvious under a finger and obvious to the eye.

The second block counts in fives so a blind reader can count the cells directly:
four solid cells then a gap, over and over.
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FULL = '='          # all six dots, in the North American Braille ASCII table
WIDTHS = [44, 42, 40, 38, 36, 34, 32, 30]


def bar(n):
    return FULL * n


def fives(n):
    """four solid cells then a space, so the groups can be counted by touch"""
    out = []
    while len(out) < n:
        out += [FULL] * 4 + [' ']
    return ''.join(out[:n]).rstrip()


def main():
    lines = []
    for w in WIDTHS:
        lines.append(bar(w))
        lines.append('')
    lines.append(fives(max(WIDTHS)))
    lines.append('')
    lines.append(fives(max(WIDTHS)))

    brf = '\r\n'.join(lines) + '\r\n\f'
    out = os.path.join(ROOT, 'test-sheets', 'print-0-ruler.brf')
    io.open(out, 'w', encoding='ascii', newline='').write(brf)
    print('print-0-ruler.brf  %d lines, widest %d cells'
          % (len([l for l in lines if l]), max(WIDTHS)))

    key = """# Sheet 0 — the ruler

**Emboss this before anything else, on the paper you have actually cut, with the
binding margin already set on the machine.** It takes one sheet and it settles a
question no calculation can.

## What is on it

Eight bars of solid cells, one per line, with a blank line between each:

| bar | cells |
|---|---|
| 1st | 44 |
| 2nd | 42 |
| 3rd | 40 |
| 4th | 38 |
| 5th | 36 |
| 6th | 34 |
| 7th | 32 |
| 8th | 30 |

Then two lines that count in fives: four solid cells, a gap, four solid cells, a
gap, and so on. Those are for counting by touch.

## How to read it

**Find the widest bar that comes out as a single line.**

A bar wider than the paper does not simply run off the edge. The machine wraps
it, so the leftover cells land on the line below as a short stub. One long line
followed by a short stub means that width is too wide. A clean single line with
nothing under it means that width fits.

That number is the width every file for this press must be built at. Tell me the
number and I will rebuild the test sheets at it.

## Also worth checking on the same sheet

- **Count the lines.** The sheet has 25 lines of content. If the page breaks
  before the last one, the paper holds fewer lines than we assumed, and I need
  that number too.
- **The binding margin.** Set it on the machine to 4 or 5 cells before printing,
  then check by touch that every line starts at the same place and that there is
  room to punch without hitting a dot.
- **Feel the dots.** 150 gsm should hold them. Press a finger firmly across a
  solid bar and then read it again. If the dots flatten, the paper is too soft
  and the weight needs to go up, not the machine.

## Why the bars are solid cells

Every dot in the cell is raised, so a missing hammer shows up as a groove running
down the whole page. If one column of dots is missing from every bar, that is the
machine and not the file, and the embosser's own hammer test will confirm it.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
    io.open(os.path.join(ROOT, 'test-sheets', 'RULER-KEY.md'), 'w',
            encoding='utf-8', newline='\n').write(key)
    print('RULER-KEY.md written')


if __name__ == '__main__':
    main()
