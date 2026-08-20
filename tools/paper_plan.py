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


IN = 25.4


def fits(width_mm, height_mm, bind_cells=0):
    """Riaz asks for the binding margin in cells, not millimetres, which is the
    right unit: it is a whole number of cells the press simply does not use."""
    usable_w = width_mm - 2 * EDGE_X
    usable_h = height_mm - 2 * EDGE_Y
    cells = int(usable_w // CELL_W) - bind_cells
    lines = int(usable_h // LINE_H)
    return max(cells, 0), max(lines, 0)


def inches(w_in, h_in, bind_cells=0):
    return fits(w_in * IN, h_in * IN, bind_cells)


SIZES = [
    ('11 x 12 in, their cut  ', 11 * 25.4, 12 * 25.4),
    ('11 x 14 in, true quarter', 11 * 25.4, 14 * 25.4),
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


def table(binds=(0, 3, 4, 5)):
    head = 'paper                     size mm   ' + '  '.join(
        'bind %d cell%s' % (b, ' ' if b == 1 else 's') for b in binds)
    print(head)
    print('-' * len(head))
    for name, w, h in SIZES:
        cols = []
        for b in binds:
            c, l = fits(w, h, b)
            cols.append('%2d x %2d' % (c, l))
        print('%s %3.0f x %3.0f  %s' % (name, w, h, '   '.join(cols)))
    print()
    print('each cell is "cells per line x lines per page".')
    print()
    c, l = inches(11, 14, 4)
    print('THE SHEET IS 22 x 28 INCHES. Two across and two down is 11 x 14 in,')
    print('with nothing left over. That is the same width as the 11 x 12 they')
    print('cut now, so no line gets shorter, and it is %d lines instead of %d,'
          % (l, inches(11, 12, 4)[1]))
    print('with no offcut strip to throw away.')
    print()
    print('At 11 inches wide with a %d-cell binding margin: %d cells per line.'
          % (4, c))
    print()
    print('These numbers assume the machine cannot emboss within %.0f mm of the'
          % EDGE_X)
    print('paper edge, which is an assumption and not a measurement. Emboss')
    print('test-sheets/print-0-ruler.brf once on the cut paper and read the')
    print('answer off the page instead.')


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
