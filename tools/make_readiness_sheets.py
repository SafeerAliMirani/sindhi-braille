# -*- coding: utf-8 -*-
"""
The pages before the letters: teaching the finger, not the alphabet.

    python tools/make_readiness_sheets.py --width 38 --lines 25

Writes test-sheets/print-6-readiness.brf and READINESS-KEY.md.

A sighted child arrives at reading with the eye already trained: it has been
tracking, comparing shapes and following lines since infancy. A blind child
arrives with a finger that has done none of that, and a converted textbook gives
them nothing for it, because the book it was converted from had no reason to.

These pages are the reason to write a braille book rather than convert one. Six
exercises, in order:

  1  one dot, then two, then three - is there more here than there
  2  full cell against empty space - where does something begin and end
  3  tracking a long unbroken line without losing it
  4  finding the start of the next line, which is where beginners get lost
  5  same or different, a pair at a time
  6  counting in groups, so a hand learns to move in fives

None of this is Sindhi. A child who cannot yet do these cannot read any script
in braille, and a child who can is ready for the alphabet.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FULL  = '='        # all six dots
D1    = 'A'        # dot 1 alone
D12   = 'B'        # dots 1 and 2
D123  = 'L'        # dots 1, 2 and 3
BLANK = ' '


def line_of(pattern, n):
    out = (pattern * ((n // len(pattern)) + 1))[:n]
    return out.rstrip()


def build(width=38, height=25):
    W = width
    P = []          # pages, each a list of lines

    # ---- 1: one dot, two dots, three dots -------------------------------
    p = []
    p.append(line_of(D1 + BLANK, W))
    p.append('')
    p.append(line_of(D12 + BLANK, W))
    p.append('')
    p.append(line_of(D123 + BLANK, W))
    p.append('')
    p.append(line_of(FULL + BLANK, W))
    P.append(p)

    # ---- 2: something, then nothing -------------------------------------
    p = []
    for run in (2, 4, 6, 8):
        p.append(FULL * run)
        p.append('')
    p.append(FULL * 4 + BLANK * 6 + FULL * 4)
    p.append('')
    p.append(FULL * 2 + BLANK * 10 + FULL * 2 + BLANK * 4 + FULL * 2)
    P.append(p)

    # ---- 3: one unbroken line, as long as the page ----------------------
    p = []
    for _ in range(3):
        p.append(FULL * W)
        p.append('')
    p.append(FULL * W)
    P.append(p)

    # ---- 4: finding the next line ---------------------------------------
    # a full line, then a line that begins after a gap, so the finger has to
    # come back to the left margin and search down rather than sideways
    p = []
    p.append(FULL * W)
    p.append(BLANK * 0 + FULL * 6)
    p.append(FULL * W)
    p.append(BLANK * 0 + FULL * 6)
    p.append(FULL * W)
    p.append(BLANK * 0 + FULL * 6)
    P.append(p)

    # ---- 5: same or different -------------------------------------------
    pairs = [(FULL, FULL), (D1, D1), (D1, D12), (FULL, D123),
             (D12, D12), (D123, D1), (FULL, FULL), (D12, D123)]
    p = []
    for a, b in pairs:
        p.append(a + BLANK * 3 + b)
        p.append('')
    P.append(p)

    # ---- 6: counting in fives -------------------------------------------
    p = []
    for groups in (2, 3, 4, 5):
        p.append(((FULL * 4) + BLANK) * groups)
        p.append('')
    P.append(p)

    pages = []
    for p in P:
        while len(p) < height:
            p.append('')
        pages.append('\r\n'.join(p[:height]).rstrip('\r\n'))
    brf = ('\r\n\f'.join(pages)) + '\r\n\f'

    out = os.path.join(ROOT, 'test-sheets', 'print-6-readiness.brf')
    io.open(out, 'w', encoding='ascii', newline='').write(brf)
    widest = max(len(l) for pg in P for l in pg)
    print('print-6-readiness.brf  %d pages, widest %d cells' % (len(P), widest))
    if widest > W:
        print('  WARNING: wider than the page')

    key = """# Sheet 6 — the pages before the letters

Six pages. **No Sindhi on any of them.** They train the finger, which is the part
a converted textbook cannot help with, because the book it was converted from had
no reason to.

A sighted child comes to reading with an eye that has been tracking and comparing
shapes since infancy. A blind child comes with a finger that has done none of it.

## The six pages

**Page 1 — how much is here.** Rows of one dot, then two, then three, then a
full cell. Ask only: is this row more than the last one? Nothing about letters.

**Page 2 — where something starts and stops.** Blocks of full cells with gaps
between them, the gaps getting wider and less even. Ask: how many blocks, and
which gap is biggest.

**Page 3 — a line that does not stop.** Four full lines, the width of the page.
Ask them to run a finger from the left edge to the right without lifting it.
This is the single most useful thing on the sheet.

**Page 4 — finding the next line.** A full line, then a short one, then a full
line again. The finger must return to the left margin and drop down, not slide
sideways. **This is where beginning braille readers get lost**, and it is worth
more practice than anything else here.

**Page 5 — same or different.** Two cells side by side with a gap. Some pairs
match, some do not. Ask only: same, or different. This is the whole skill of
reading braille, before any meaning is attached to it.

**Page 6 — counting in fives.** Groups of four cells with a gap. The hand learns
to move in units instead of dot by dot, which is what makes reading fast later.

## How to use them

**Do not hurry.** A child may spend weeks on page 3 and 4, and that is time
saved later, not lost. Nothing on the alphabet pages will work until these do.

**Ask Riaz whether the order is right.** He has taught blind children and I have
not. If page 5 should come before page 3, it should.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
    io.open(os.path.join(ROOT, 'test-sheets', 'READINESS-KEY.md'), 'w',
            encoding='utf-8', newline='\n').write(key)
    print('READINESS-KEY.md written')


if __name__ == '__main__':
    a = sys.argv[1:]
    w = int(a[a.index('--width') + 1]) if '--width' in a else 38
    h = int(a[a.index('--lines') + 1]) if '--lines' in a else 25
    build(w, h)
