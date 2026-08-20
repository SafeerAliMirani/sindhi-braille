# -*- coding: utf-8 -*-
"""
What fits on a sheet of paper, once you have cut it and left room for binding.

    python paper_plan.py                     # the table for common cut sizes
    python paper_plan.py 210 297 --bind 12   # one size, in millimetres

There is no braille paper in Larkana, so the press cuts 150 gsm chart paper. The
weight is right: braille paper is 120 to 160 gsm and 150 sits in the middle, so
the dots will hold. What changes is the width, and the width decides everything,
because braille geometry is fixed and does not scale.

Braille is read left to right in every language, Sindhi included, so the binding
margin goes on the LEFT and comes off the line before the cells do.

The numbers below are the standard geometry:

    horizontal pitch, cell to cell     6.2 mm
    vertical pitch, line to line       10.0 mm
    unprintable edge each side          8.0 mm   (a tractor or friction feed
                                                  cannot emboss to the paper's edge)
    unprintable edge top and bottom    10.0 mm

An embosser also has its own maximum line, so treat these as what the PAPER
allows and set the machine to the smaller of the two.
"""
import sys

CELL_W   = 6.2      # mm, cell to cell
LINE_H   = 10.0     # mm, line to line
EDGE_X   = 8.0      # mm, unprintable, each side
EDGE_Y   = 10.0     # mm, unprintable, top and bottom


def fits(width_mm, height_mm, bind_mm=0.0):
    usable_w = width_mm - 2 * EDGE_X - bind_mm
    usable_h = height_mm - 2 * EDGE_Y
    cells = int(usable_w // CELL_W)
    lines = int(usable_h // LINE_H)
    return max(cells, 0), max(lines, 0)


SIZES = [
    ('A4                     ', 210, 297),
    ('A5 (half of A4)        ', 148, 210),
    ('Letter                 ', 216, 279),
    ('Legal                  ', 216, 356),
    ('Foolscap               ', 216, 330),
    ('quarter chart 22x28 in ', 279, 356),
    ('half chart 22x28 in    ', 356, 559),
    ('quarter chart 23x36 in ', 292, 457),
    ('11 in braille paper    ', 280, 292),
]


def table(binds=(0, 10, 12, 15, 20)):
    head = 'paper                    size mm   ' + '  '.join(
        'bind %2d' % b for b in binds)
    print(head)
    print('-' * len(head))
    for name, w, h in SIZES:
        cols = []
        for b in binds:
            c, l = fits(w, h, b)
            cols.append('%2d x %2d' % (c, l))
        print('%s %3d x %3d  %s' % (name, w, h, '  '.join(cols)))
    print()
    print('each cell is "cells per line x lines per page".')
    print()
    c40, l40 = fits(279, 356, 12)
    print('The line worth noticing is the quarter chart sheet. A 22 x 28 inch')
    print('chart sheet cut in four gives 279 x 356 mm, which holds %d cells and'
          % c40)
    print('%d lines even after a 12 mm binding margin. %d cells is the' % (l40, c40))
    print('international braille page width, so cutting to quarters gives a')
    print('standard page on paper the press can actually buy, where cutting to')
    print('A4 throws away twelve cells on every line.')
    print()
    print('A4 is listed as %d cells here because that is what the paper allows.'
          % fits(210, 297, 12)[0])
    print('The embosser has its own margins on top of the paper\'s, and 28 is')
    print('what actually printed on the machine in August 2026. Set the machine')
    print('to the smaller of the two numbers, and prove it on one sheet before')
    print('printing a hundred.')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    bind = 0.0
    if '--bind' in sys.argv:
        bind = float(sys.argv[sys.argv.index('--bind') + 1])
    if len(args) >= 2:
        w, h = float(args[0]), float(args[1])
        c, l = fits(w, h, bind)
        print('%.0f x %.0f mm, binding margin %.0f mm' % (w, h, bind))
        print('  %d cells per line, %d lines per page' % (c, l))
        print('  usable area %.0f x %.0f mm' % (w - 2*EDGE_X - bind, h - 2*EDGE_Y))
    else:
        table()
