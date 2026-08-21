# -*- coding: utf-8 -*-
"""
Twin-vision pages: one sheet a blind child and a sighted adult read together.

    python tools/make_twin.py book/draft/gemini-v1.txt --out book/out

Two files come out of one source and they are made to register with each other:

  twin-ink.html   the Sindhi in ink, each sentence on its own line, with an
                  empty band underneath it exactly where the braille will land
  twin.brf        the same sentences in braille, with a blank line after every
                  line of text

**How the registration works, and why it needs nothing special from the
embosser.** Every braille embosser writes lines at a 10.0 mm pitch and cannot be
asked for anything else. A blank line therefore costs exactly 10.0 mm, so a file
with a blank line after every line of text puts its text lines 20.0 mm apart.
The ink page is laid out on that same 20.0 mm grid with each sentence sitting
6 mm above its own braille band. Print the sheet on the laser first, feed it to
the embosser second, and the dots fall into the empty bands.

Nothing here depends on the embosser being told about the layout. It depends
only on the blank lines being in the file, which is why they are.

**Check the scale before embossing.** A laser printer asked to "fit to page"
will shrink the sheet by a few per cent, which is invisible on the page and
fatal to the registration. Page one carries a 100 mm rule. Measure it. If it is
not 100 mm, print again with scaling off, at 100%, margins none.
"""
import io, os, re, sys, html, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb
import paper_plan as pp

PAGE_W, PAGE_H = 210.0, 297.0        # A4 in mm
ROW = 2 * pp.LINE_H                  # 20.0 mm: one braille line plus one blank
PER_SHEET = 2                        # shapes to a sheet
GUTTER    = 4                        # cells kept at the left of every line for
                                     # its number: three for the number itself
                                     # and one blank before the text
SD_DIGITS = '۰۱۲۳۴۵۶۷۸۹'


def sd_num(n):
    return ''.join(SD_DIGITS[int(d)] for d in str(n))


def num_cells(n):
    """a number in braille: the number sign, then its digits"""
    out = [sb.NUMSIGN]
    for d in str(n):
        out.append(sb.DIGIT[d])
    return out


def gutter_cells(n):
    """the line number, in a fixed three cells, with one blank after it.

    Every line of the book carries its number on the left in braille and the
    same number in ink, so a sighted teacher and a blind child can say line
    five and mean the same line. It costs four cells of a twenty-six cell page,
    which is the price of the two of them being able to talk about the text."""
    c = num_cells(n)
    return (c + [''] * (GUTTER - len(c)))[:GUTTER]
# A braille line's dots are 5.0 mm deep, so between one line's dots and the
# next line's there are 15.0 mm of blank paper. The ink for a sentence lives in
# that gap, in a box of its own with clearance at both ends, and the box is
# clipped so that a deep Naskh descender cannot reach down into the dots it is
# supposed to sit above. Without the clearance the tails of ۾ and ن landed in
# the band and the embossed dots came down on top of them.
INK_BOX   = 9.5                     # mm, the height the ink is given
INK_CLEAR = 5.0                     # mm of blank paper between ink and dots
INK_PT    = 15                      # a class 1 primer is not set in 11 point


def geometry(width_cells, bind_cells, page_w=PAGE_W, page_h=PAGE_H):
    """where everything sits on the sheet, in millimetres"""
    left = pp.EDGE_X + bind_cells * pp.CELL_W
    text_w = width_cells * pp.CELL_W
    # The grid starts one braille line below the top edge. A laser printer
    # cannot put ink in the first few millimetres of a sheet, and the ink for a
    # line sits above its dots, so a grid starting at the edge loses its first
    # sentence. The .brf pays for this with one blank line at the top of each
    # page, which costs exactly the 10.0 mm the ink needs.
    top = pp.EDGE_Y + pp.LINE_H
    rows = int((page_h - top - pp.EDGE_Y) // ROW)
    return dict(left=left, text_w=text_w, rows=rows,
                top=top, page_w=page_w, page_h=page_h,
                shape_lines=int((page_h - top - pp.EDGE_Y) // pp.LINE_H))


def sentences(path):
    """the source, one readable line at a time.

    A lesson file in book/FORMAT.md form, or plain text. Markers are kept as
    their own line so a heading stays a heading; @page and @figure are dropped
    here because a twin-vision page carries no figures yet."""
    out = []
    for raw in io.open(path, encoding='utf-8'):
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('@page') or s.startswith('@figure'):
            continue
        if s.startswith('@shape') or s.startswith('@table'):
            out.append(s)            # markers, expanded by the page builder
            continue
        if s.startswith('@heading'):
            s = s[8:].strip()
        elif s.startswith('@exercise'):
            s = s[9:].strip()
        out.append(s)
    return out


def wrap(line, width):
    """break one sentence into braille lines of at most `width` cells.

    Wrapping is done on the cells, not on the characters, because a word's
    length in cells is not its length in letters: ک is two cells and a number
    carries a sign in front of it."""
    words = [w for w in line.split(' ') if w]
    rows, cur, cur_n = [], [], 0
    for w in words:
        cells = sb.word_to_cells(w)
        n = len(cells)
        if cur and cur_n + 1 + n > width:
            rows.append((cur, cur_n)); cur, cur_n = [], 0
        if cur:
            cur.append((' ', [''])); cur_n += 1
        cur.append((w, cells)); cur_n += n
    if cur:
        rows.append((cur, cur_n))
    return rows


# Every shape is a list of primitives in millimetres inside the drawing area,
# so the same description draws the dots and the printed outline and the two
# cannot drift apart.  w and h are the area; the shapes are written against
# them rather than against fixed numbers, so a wider page draws a bigger circle.
#
# What survives on this grid: the dots are 2.5 mm apart inside a cell, 6.2 mm
# between cells and 10.0 mm between lines, so a curve is felt as a curve only if
# it is large.  These are drawn to fill the page for that reason, and the animals
# are cut down to the outline a finger can actually trace - a fish is a body and
# a tail, not scales and an eye.
def _star(cx, cy, r):
    import math
    pts = []
    for k in range(11):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = r if k % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return [('poly', pts)]


def _arc(cx, cy, r, a0, a1, steps=64):
    import math
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / steps),
             cy + r * math.sin(a0 + (a1 - a0) * k / steps)) for k in range(steps + 1)]


def _crescent(cx, cy, r):
    """the moon of the flag: one closed outline, not two overlapping circles.

    A crescent is the outer disc with a second disc bitten out of it, so its
    boundary is the part of the outer circle that lies OUTSIDE the biting
    circle, joined to the part of the biting circle that lies INSIDE the outer
    one. Taking the wrong half of the second arc - which is easy, and which I
    did first - gives a circle with a chord across it, and under a finger that
    is a circle with a line in it, not a moon."""
    import math
    R = r
    r2 = R * 0.86
    d = R * 0.42                              # how far the bite is offset
    ox = cx + d
    x = (d * d - r2 * r2 + R * R) / (2 * d)   # where the two circles cross
    y = math.sqrt(max(R * R - x * x, 0.0))
    a_out = math.atan2(y, x)                  # measured from the outer centre
    a_in = math.atan2(y, x - d)               # measured from the biting centre
    outer = _arc(cx, cy, R, a_out, 2 * math.pi - a_out)      # convex, the back
    inner = _arc(ox, cy, r2, a_in, 2 * math.pi - a_in)       # concave, the belly
    return [('poly', outer + inner[::-1] + [outer[0]])]


SHAPES = {
    # --- the four geometric shapes ---------------------------------------
    'circle':    lambda w, h: [('circle', w/2, h/2, min(w, h)/2 - 4)],
    'square':    lambda w, h: [('rect', w/2 - (min(w, h)/2 - 4), h/2 - (min(w, h)/2 - 4),
                                2*(min(w, h)/2 - 4), 2*(min(w, h)/2 - 4))],
    'rectangle': lambda w, h: [('rect', 6, h/4, w - 12, h/2)],
    'triangle':  lambda w, h: [('tri', w/2, 6, w - 12, h - 12)],
    # --- things a six-year-old can name ----------------------------------
    'house':     lambda w, h: [('rect', w/2 - w*0.30, h*0.42, w*0.60, h*0.52),
                               ('tri', w/2, h*0.06, w*0.76, h*0.36),
                               ('rect', w/2 - w*0.09, h*0.70, w*0.18, h*0.24)],
    # A crown made of a circle on a stick is a lollipop under a finger. A tree
    # is a triangle on a trunk, which is also how a child draws one.
    'tree':      lambda w, h: [('tri', w/2, h*0.04, w*0.72, h*0.70),
                               ('rect', w/2 - w*0.08, h*0.74 - 2, w*0.16, h*0.24)],
    # A hexagon with a triangle stuck on it is not a fish. This is a body that
    # narrows to a waist and a tail cut from the same outline, one closed curve.
    'fish':      lambda w, h: [('poly', [(w*0.05, h*0.50), (w*0.16, h*0.30),
                                         (w*0.36, h*0.20), (w*0.56, h*0.26),
                                         (w*0.66, h*0.42),
                                         (w*0.92, h*0.16), (w*0.86, h*0.50),
                                         (w*0.92, h*0.84), (w*0.66, h*0.58),
                                         (w*0.56, h*0.74), (w*0.36, h*0.80),
                                         (w*0.16, h*0.70), (w*0.05, h*0.50)])],
    # A cup with a straight-sided handle reads as a box with a flap. This one
    # has a round handle, joined to the wall at both ends.
    'cup':       lambda w, h: [('poly', [(w*0.22, h*0.26), (w*0.62, h*0.26),
                                         (w*0.56, h*0.82), (w*0.28, h*0.82),
                                         (w*0.22, h*0.26)]),
                               ('poly', [(w*0.607, h*0.38), (w*0.78, h*0.41),
                                         (w*0.84, h*0.50), (w*0.78, h*0.59),
                                         (w*0.581, h*0.62)])],
    'star':      lambda w, h: _star(w/2, h/2, min(w, h)/2 - 4),
    'boat':      lambda w, h: [('poly', [(w*0.08, h*0.60), (w*0.92, h*0.60),
                                         (w*0.74, h*0.90), (w*0.26, h*0.90),
                                         (w*0.08, h*0.60)]),
                               ('poly', [(w/2, h*0.06), (w/2, h*0.60)]),
                               ('poly', [(w/2, h*0.10), (w*0.84, h*0.54),
                                         (w/2, h*0.54)])],
    # --- Pakistan --------------------------------------------------------
    # The hoist strip, the crescent and the star. The green and the white are
    # not felt, so the strip is drawn as a line and the rest is the emblem.
    # The star sits in the crescent's opening, clear of it. On the first try it
    # was drawn beside the moon and its lower point ran into the moon's back;
    # two lines that cross are one line under a finger.
    'flag':      lambda w, h: (lambda x0, fw, cx, cy, R: [
                     ('rect', 4, h*0.18, w - 8, h*0.64),
                     ('poly', [(x0 + fw*0.25, h*0.18), (x0 + fw*0.25, h*0.82)])]
                     + _crescent(cx, cy, R)
                     + _star(cx + R*1.05, cy - R*0.55, R*0.42)
                 )(4, w - 8, 4 + (w - 8)*0.52, h*0.50, min(h*0.22, w*0.15)),
    # --- the body --------------------------------------------------------
    # Head, body, two arms, two legs, joined into one figure. Naming the parts
    # on the drawing would need lead lines and 3 mm clearances the grid cannot
    # give, so the parts are named in the sentences, not on the picture.
    'body':      lambda w, h: [('circle', w/2, h*0.13, min(h*0.11, w*0.13)),
                               ('poly', [(w/2, h*0.13 + min(h*0.11, w*0.13)),
                                         (w/2, h*0.56)]),
                               ('poly', [(w*0.20, h*0.46), (w/2, h*0.28),
                                         (w*0.80, h*0.46)]),
                               ('poly', [(w*0.26, h*0.94), (w/2, h*0.56),
                                         (w*0.74, h*0.94)])],
}


def table_lines(kind, per_line=4):
    """the alphabet and the digits, as the front of the book.

    Both readers need the chart, and they need the same chart: the blind child
    feels the letter itself, the sighted teacher reads the letter and the dots
    that make it. So each line carries the letters in braille, and the ink over
    it names the same letters with their dot numbers, in the order the website
    prints them.

    Returns a list of (ink text, [cells]) - ordinary lines, so they page and
    number like any other."""
    out = []
    if kind == 'numbers':
        items = [(d, sb.DIGIT[d]) for d in '1234567890']
        out.append(('عدد جو نشان: ' + ''.join(SD_DIGITS[int(c)] for c in sb.NUMSIGN),
                    [sb.NUMSIGN]))
        per_line = 5
        pairs = [(sd_num(int(d)), [c]) for d, c in items]
    else:
        pairs = []
        for L, cells in sb.LETTER.items():
            pairs.append((L, list(cells)))
    for i in range(0, len(pairs), per_line):
        chunk = pairs[i:i + per_line]
        ink = ' · '.join('%s (%s)' % (name, '-'.join(
            ''.join(SD_DIGITS[int(d)] for d in c) for c in cells))
            for name, cells in chunk)
        cells = []
        for j, (_, cs) in enumerate(chunk):
            if j:
                cells.append('')
            cells.extend(cs)
        out.append((ink, cells))
    return out


def _draw(prims, width, lines_avail):
    """one shape description -> the raised dots, and the same curve as SVG"""
    import tactile as t
    on, svg, parts = set(), [], []
    for p in prims:
        k = p[0]
        if k == 'circle':
            _, cx, cy, r = p
            d = t.circle(cx, cy, r, width, lines_avail); on |= d; parts.append(d)
            svg.append('<circle cx="%.2f" cy="%.2f" r="%.2f"/>' % (cx, cy, r))
        elif k == 'rect':
            _, x, y, w, h = p
            d = t.rectangle(x, y, w, h, width, lines_avail); on |= d; parts.append(d)
            svg.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f"/>'
                       % (x, y, w, h))
        elif k == 'tri':
            _, x, y, base, height = p
            d = t.triangle(x, y, base, height, width, lines_avail); on |= d; parts.append(d)
            svg.append('<polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f"/>'
                       % (x, y, x - base/2, y + height, x + base/2, y + height))
        else:
            _, pts = p
            d = t.path(pts, width, lines_avail); on |= d; parts.append(d)
            svg.append('<polyline points="%s"/>'
                       % ' '.join('%.2f,%.2f' % q for q in pts))
    return on, ''.join(svg), parts


# The tactile graphics standard asks for 1/8 inch, 3 mm, between a component
# and any other, because two lines closer than that are felt as one. On a
# braille cell grid the finest step is 2.5 mm, so two lines are either adjacent
# dots - which reads as one line, and is what you want where a roof meets a
# wall - or at least two steps apart. There is no way to draw 3 mm on this
# grid. So the rule enforced here is the grid's version of the standard's:
#
#   parts that are meant to join must adjoin      (<= 2.5 mm, one dot step)
#   parts that are meant to be separate must be   (>= 5.0 mm, two dot steps)
#
# and anything landing between the two is the ambiguous case the standard is
# warning about. A gap of 2.5 mm between a cup and its handle is not a handle.
JOIN_MM  = 2.5       # one dot step: the parts touch
CLEAR_MM = 5.0       # two dot steps: the parts read as separate


def separation(parts):
    """the closest approach between two different parts of one shape, in mm"""
    import tactile as t
    worst = None
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            for (c1, r1) in parts[i]:
                x1, y1 = t.dot_mm(c1, r1)
                for (c2, r2) in parts[j]:
                    x2, y2 = t.dot_mm(c2, r2)
                    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                    if worst is None or d < worst:
                        worst = d
    return worst


def shape_block(kind, label, width, lines_avail):
    """one shape, embossed and printed on the same sheet, on the same curve.

    Text has to be interlined because dots on top of letters destroy both. A
    shape is the opposite case: the printed outline and the embossed outline are
    the same line, so they are drawn at the same millimetres and the finger
    follows exactly what the eye sees.

    The shape is drawn at the ordinary 10.0 mm line pitch, not the 20.0 mm of
    the text pages, because vertical resolution is what a curve needs most."""
    import tactile as t
    if kind not in SHAPES:
        raise SystemExit('unknown shape %r; have: %s'
                         % (kind, ' '.join(sorted(SHAPES))))
    # Page format follows the tactile graphics standard: the name on its own
    # line, a blank line, then the graphic, and a blank line after it. The
    # standard caps a graphic at 40 cells by 25 lines; these are 26 by 21.
    area_w = width * pp.CELL_W
    area_h = lines_avail * pp.LINE_H
    on, svg, parts = _draw(SHAPES[kind](area_w, area_h), width, lines_avail)
    body = t.to_lines(on, width, lines_avail)
    while len(body) < lines_avail:
        body.append('')
    cells = sb.word_to_cells(label)
    pad = max(0, (width - len(cells)) // 2)
    rows = [' ' * pad + ''.join(sb.cell_to_ascii(c) for c in cells), ''] + body
    sep = separation(parts)
    if sep is not None and JOIN_MM < sep < CLEAR_MM:
        print('  WARNING  %-10s two parts sit %.1f mm apart: too far to feel '
              'joined, too close to feel separate. Move them together or at '
              'least %.1f mm apart.' % (kind, sep, CLEAR_MM))
    return rows, svg, label, (sep if sep is not None else float('inf'))


def shape_page(shapes, width, g):
    """one sheet carrying one or two shapes.

    Two to a page halves the paper, and at 26 cells by 10 lines a shape is still
    100 mm by 161 mm, far above anything the standard calls small. The two are
    separated by a blank line, and each keeps its own name on the line above it,
    so a finger running down the page meets name, shape, blank, name, shape."""
    n = len(shapes)
    per = (g['shape_lines'] - 1) // n - 2      # name + blank belong to each
    per = min(per, 25)
    blocks = [shape_block(k, l, width, per) for k, l in shapes]
    rows = []
    for i, (r, _, _, _) in enumerate(blocks):
        if i:
            rows.append('')
        rows.extend(r)
    return rows, blocks, per


def build(src, width, bind, out_dir, title, back_shift=0.0):
    g = geometry(width, bind)
    lines = []                                  # (sindhi text, [cells])
    pages, cur, pending = [], [], []
    textw = width - GUTTER                      # cells left for the text itself
    rows_per_page = g['rows'] - 1               # one row goes to the page number
    for s in sentences(src):
        if s.startswith('@table'):
            kind = s.split(None, 1)[1].strip() if ' ' in s else 'letters'
            for ink, cells in table_lines(kind):
                lines.append((ink, cells))
                cur.append((ink, cells))
                if len(cur) == rows_per_page:
                    pages.append(('text', cur)); cur = []
            continue
        if s.startswith('@shape'):
            p = s.split(None, 2)
            pending.append((p[1], p[2] if len(p) > 2 else ''))
            if cur:
                pages.append(('text', cur)); cur = []
            if len(pending) == PER_SHEET:
                pages.append(('shape', shape_page(pending, width, g)))
                pending = []
            continue
        for parts, _ in wrap(s, textw):
            txt = ''.join(w for w, _ in parts)
            cells = [c for _, cs in parts for c in cs]
            lines.append((txt, cells))
            cur.append((txt, cells))
            if len(cur) == rows_per_page:
                pages.append(('text', cur)); cur = []
    if pending:
        pages.append(('shape', shape_page(pending, width, g)))
    if cur:
        pages.append(('text', cur))
    if not pages:
        pages = [('text', [])]

    # ---- the braille file -------------------------------------------------
    brf = []
    # Page one is the registration target: every line a solid bar of full cells,
    # to be embossed onto the printed test sheet. If every bar sits inside its
    # printed band, the two machines agree and the book can be run.
    brf.append('')                              # the top margin the ink needs
    for _ in range(g['rows']):
        brf.append('=' * width)
        brf.append('')
    brf.append('\f')
    pageno_brl = 0
    def row(cells):
        return ''.join(sb.cell_to_ascii(c) if c else ' ' for c in cells)

    for kind, pg in pages:
        brf.append('')                          # same top margin on every page
        pageno_brl += 1
        # The page number goes on a line of its own at the top, pushed to the
        # right margin, which is where a braille book puts it.
        pn = num_cells(pageno_brl)
        brf.append(row([''] * (width - len(pn)) + pn))
        brf.append('')
        if kind == 'shape':
            brf.extend(pg[0])
        else:
            for i, (txt, cells) in enumerate(pg, 1):
                brf.append(row(gutter_cells(i) + cells))
                brf.append('')                  # the blank line the ink sits in
        brf.append('\f')
    body = '\r\n'.join(brf)
    io.open(os.path.join(out_dir, 'twin.brf'), 'w',
            encoding='ascii', newline='').write(body)

    # ---- the ink page -----------------------------------------------------
    css = """
@page { size: 210mm 297mm; margin: 0 }
html,body { margin:0; padding:0 }
body { font-family:"Noto Naskh Arabic","Segoe UI","Times New Roman",serif;
       -webkit-print-color-adjust:exact; print-color-adjust:exact }
.page { position:relative; width:210mm; height:297mm; overflow:hidden;
        page-break-after:always; break-after:page }
.page:last-child { page-break-after:auto; break-after:auto }
.ln { position:absolute; direction:rtl; text-align:right; white-space:nowrap;
      font-size:%dpt; line-height:1.15; color:#000; overflow:hidden;
      display:flex; align-items:center; justify-content:flex-start }
.band { position:absolute; border-bottom:0 }
.tick { position:absolute; background:#000 }
.rule { position:absolute; height:0.3mm; background:#000 }
.pn   { position:absolute; direction:ltr; font-size:11pt; color:#000;
        display:flex; align-items:center; justify-content:flex-end;
        overflow:hidden }
.lnum { position:absolute; direction:ltr; font-size:10pt; color:#000;
        display:flex; align-items:center; justify-content:flex-start;
        overflow:hidden }
.note { position:absolute; direction:rtl; font-size:8pt; color:#444 }
.en   { position:absolute; direction:ltr; font-size:8pt; color:#444;
        font-family:"Segoe UI",sans-serif }
"""
    h = ['<!doctype html><html lang="sd" dir="rtl"><head><meta charset="utf-8">',
         '<title>%s</title><style>%s</style></head><body>'
         % (html.escape(title), css % INK_PT)]

    # Test sheet one: the scale check. A laser printer asked to fit-to-page
    # shrinks the sheet a few per cent, which is invisible and fatal.
    h.append('<section class="page">')
    h.append('<div class="en" style="left:20mm;top:30mm;width:170mm">'
             '<b>Before you emboss anything, measure the line below.</b> It is '
             '100 mm. If your ruler says otherwise the printer scaled the sheet: '
             'print again at 100%, scaling off, margins none. A sheet 3% small '
             'puts the last braille line 8 mm outside its band.</div>')
    h.append('<div class="rule" style="left:20mm;top:50mm;width:100mm"></div>')
    h.append('<div class="en" style="left:20mm;top:52mm">100 mm</div>')
    h.append('<div class="en" style="left:20mm;top:70mm;width:170mm">'
             'The next sheet carries %d empty bands, %d cells wide and %.1f mm '
             'apart, drawn exactly where the braille lines land. Print it, emboss '
             'the first page of twin.brf onto it, and every solid bar of dots '
             'should sit inside a band. That one sheet settles the registration '
             'for the whole book.</div>' % (g['rows'], width, ROW))
    h.append('<div class="en" style="left:20mm;top:110mm;width:170mm">'
             'Geometry: A4, %d cells per line, %d lines per sheet, %.1f mm from '
             'the top edge to the first braille line, %.1f mm from the left edge '
             'to the first cell (%d cells of binding margin), %.1f mm cell to '
             'cell, %.1f mm line to line inside a pair.</div>'
             % (width, g['rows'], g['top'], g['left'], bind, pp.CELL_W, pp.LINE_H))
    h.append('</section>')

    # Test sheet two: the bands, at their true positions and nothing else.
    h.append('<section class="page">')
    for k in range(g['rows']):
        y = g['top'] + k * ROW
        h.append('<div class="rule" style="left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                 'background:#c8c8c8"></div>' % (g['left'], y, g['text_w']))
        h.append('<div class="rule" style="left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                 'background:#c8c8c8"></div>' % (g['left'], y + 5.0, g['text_w']))
    h.append('</section>')

    pageno_ink = 1
    for pageno, (kind, pg) in enumerate(pages):
        # The book is printed on both sides, so the binding margin has to be on
        # the outside of each leaf: left on the front, right on the back. The
        # braille itself never moves - the embosser writes from the same left
        # edge on both sides - so only the ink swaps, and on a back page the
        # text area starts at the sheet's own left edge instead.
        left = g['left'] if pageno % 2 == 0 else pp.EDGE_X
        # Some interpoint embossers drop the reverse side by half a line pitch
        # so its dots interleave with the front's. If yours does, the ink on the
        # back has to move with it: measure the test sheet and pass
        # --back-shift 5. On a machine that keeps the lines level this is 0.
        dy = 0.0 if pageno % 2 == 0 else back_shift
        h.append('<section class="page">')
        h.append('<div class="pn" style="left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                 'height:%.2fmm">%s</div>'
                 % (left, g['top'] + dy - INK_CLEAR - INK_BOX,
                    g['text_w'], INK_BOX, html.escape(sd_num(pageno_ink))))
        body_top = g['top'] + dy + ROW          # the page number takes row nought
        if kind == 'shape':
            rows, blocks, per = pg
            area_h = per * pp.LINE_H
            line0 = 2                           # page number line, then blank
            for i, (r, svg, label, _sep) in enumerate(blocks):
                if i:
                    line0 += 1              # the blank line between two shapes
                ytop = g['top'] + dy + line0 * pp.LINE_H
                h.append('<div class="ln" style="left:%.2fmm;top:%.2fmm;'
                         'width:%.2fmm;height:%.2fmm;justify-content:center">%s</div>'
                         % (left, ytop + pp.LINE_H - INK_CLEAR - INK_BOX,
                            g['text_w'], INK_BOX, html.escape(label)))
                h.append('<svg class="shp" xmlns="http://www.w3.org/2000/svg" '
                         'style="position:absolute;left:%.2fmm;top:%.2fmm;'
                         'width:%.2fmm;height:%.2fmm" viewBox="0 0 %.2f %.2f">'
                         '<g fill="none" stroke="#000" stroke-width="0.8">%s</g>'
                         '</svg>'
                         % (left, ytop + 2 * pp.LINE_H, g['text_w'], area_h,
                            g['text_w'], area_h, svg))
                line0 += 2 + per
        else:
            for k, (txt, _) in enumerate(pg):
                y = body_top + k * ROW - INK_CLEAR - INK_BOX
                # the line number, in the gutter the braille keeps for it
                h.append('<div class="lnum" style="left:%.2fmm;top:%.2fmm;'
                         'width:%.2fmm;height:%.2fmm">%s</div>'
                         % (left, y, GUTTER * pp.CELL_W - 2, INK_BOX,
                            html.escape(sd_num(k + 1))))
                h.append('<div class="ln" style="left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                         'height:%.2fmm">%s</div>'
                         % (left + GUTTER * pp.CELL_W, y,
                            g['text_w'] - GUTTER * pp.CELL_W, INK_BOX,
                            html.escape(txt)))
        pageno_ink += 1
        h.append('</section>')
    h.append('</body></html>')
    io.open(os.path.join(out_dir, 'twin-ink.html'), 'w', encoding='utf-8').write('\n'.join(h))

    return g, len(lines), len(pages)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('--width', type=int, default=0, help='cells per line')
    ap.add_argument('--bind', type=int, default=5, help='binding margin in cells')
    ap.add_argument('--out', default=os.path.join(ROOT, 'book', 'out'))
    ap.add_argument('--title', default='سنڌي بريل: پهريون ڪتاب')
    a = ap.parse_args()
    if not a.width:
        a.width = pp.fits(PAGE_W, PAGE_H, a.bind)[0]
    os.makedirs(a.out, exist_ok=True)
    sb.load_words()
    g, n, pages = build(a.source, a.width, a.bind, a.out, a.title)
    print('A4 %d cells x %d twin rows, binding %d cells'
          % (a.width, g['rows'], a.bind))
    print('%d lines of text over %d sheets' % (n, pages))
    print('  %s' % os.path.join(a.out, 'twin-ink.html'))
    print('  %s' % os.path.join(a.out, 'twin.brf'))


if __name__ == '__main__':
    main()
