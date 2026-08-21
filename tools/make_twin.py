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
INK_ABOVE = 8.5                     # mm from the top of the ink to its dots
INK_PT    = 16                      # a class 1 primer is not set in 11 point


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
        if s.startswith('@shape'):
            out.append(s)            # kept as a marker; it gets a page to itself
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


SHAPES = {
    # --- the four geometric shapes ---------------------------------------
    'circle':    lambda w, h: [('circle', w/2, h/2, min(w, h)/2 - 6)],
    'square':    lambda w, h: [('rect', w/2 - (min(w, h)/2 - 6), h/2 - (min(w, h)/2 - 6),
                                2*(min(w, h)/2 - 6), 2*(min(w, h)/2 - 6))],
    'rectangle': lambda w, h: [('rect', 8, h/4, w - 16, h/2)],
    'triangle':  lambda w, h: [('tri', w/2, 8, w - 16, h - 16)],
    # --- things a six-year-old can name ----------------------------------
    'house':     lambda w, h: [('rect', w/2 - w*0.30, h*0.42, w*0.60, h*0.48),
                               ('tri', w/2, h*0.08, w*0.76, h*0.34),
                               ('rect', w/2 - w*0.09, h*0.66, w*0.18, h*0.24)],
    # the trunk starts inside the crown, not below it: a gap of even a few
    # millimetres reads under a finger as two separate objects
    'tree':      lambda w, h: [('circle', w/2, h*0.30, min(w*0.36, h*0.26)),
                               ('rect', w/2 - w*0.07,
                                h*0.30 + min(w*0.36, h*0.26) - 6,
                                w*0.14,
                                h*0.92 - (h*0.30 + min(w*0.36, h*0.26) - 6))],
    # the tail joins the body along an edge, not at a point: two triangles
    # meeting at one dot feel like a bow tie, which is not a fish
    'fish':      lambda w, h: [('poly', [(w*0.06, h*0.50), (w*0.26, h*0.24),
                                         (w*0.60, h*0.24), (w*0.70, h*0.40),
                                         (w*0.70, h*0.60), (w*0.60, h*0.76),
                                         (w*0.26, h*0.76), (w*0.06, h*0.50)]),
                               ('poly', [(w*0.70, h*0.40), (w*0.94, h*0.22),
                                         (w*0.94, h*0.78), (w*0.70, h*0.60)])],
    'star':      lambda w, h: _star(w/2, h/2, min(w, h)/2 - 6),
    'boat':      lambda w, h: [('poly', [(w*0.10, h*0.62), (w*0.90, h*0.62),
                                         (w*0.74, h*0.88), (w*0.26, h*0.88),
                                         (w*0.10, h*0.62)]),
                               ('poly', [(w/2, h*0.10), (w/2, h*0.62)]),
                               ('poly', [(w/2, h*0.14), (w*0.82, h*0.56),
                                         (w/2, h*0.56)])],
    # the handle starts and ends on the cup's own wall, for the same reason
    'cup':       lambda w, h: [('poly', [(w*0.24, h*0.28), (w*0.66, h*0.28),
                                         (w*0.58, h*0.84), (w*0.32, h*0.84),
                                         (w*0.24, h*0.28)]),
                               ('poly', [(w*0.643, h*0.40), (w*0.86, h*0.44),
                                         (w*0.86, h*0.62), (w*0.606, h*0.66)])],
}


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


def shape_page(kind, label, width, g):
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
    # Page format follows the tactile graphics standard: the name on the first
    # line, a blank line, then the graphic, and nothing else on the sheet. The
    # standard requires a blank line before and after a tactile graphic and caps
    # it at 40 cells by 25 lines; this is 26 by 24 at most.
    lines_avail = min(g['shape_lines'] - 2, 25)
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


def build(src, width, bind, out_dir, title):
    g = geometry(width, bind)
    lines, shapes = [], []                      # (sindhi text, [cells])
    pages, cur = [], []
    for s in sentences(src):
        if s.startswith('@shape'):
            p = s.split(None, 2)
            kind, label = p[1], (p[2] if len(p) > 2 else '')
            if cur:
                pages.append(('text', cur)); cur = []
            pages.append(('shape', shape_page(kind, label, width, g)))
            continue
        for parts, _ in wrap(s, width):
            txt = ''.join(w for w, _ in parts)
            cells = [c for _, cs in parts for c in cs]
            lines.append((txt, cells))
            cur.append((txt, cells))
            if len(cur) == g['rows']:
                pages.append(('text', cur)); cur = []
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
    for kind, pg in pages:
        brf.append('')                          # same top margin on every page
        if kind == 'shape':
            brf.extend(pg[0])
        else:
            for txt, cells in pg:
                brf.append(''.join(sb.cell_to_ascii(c) if c else ' ' for c in cells))
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
      font-size:%dpt; line-height:1; color:#000 }
.band { position:absolute; border-bottom:0 }
.tick { position:absolute; background:#000 }
.rule { position:absolute; height:0.3mm; background:#000 }
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

    for kind, pg in pages:
        h.append('<section class="page">')
        if kind == 'shape':
            rows, svg, label, _sep = pg
            lines_avail = min(g['shape_lines'] - 2, 25)
            area_h = lines_avail * pp.LINE_H
            top = g['top'] + 2 * pp.LINE_H          # label line, then blank
            h.append('<div class="ln" style="left:%.2fmm;top:%.2fmm;width:%.2fmm;'
                     'text-align:center">%s</div>'
                     % (g['left'], g['top'] - INK_ABOVE + pp.LINE_H,
                        g['text_w'], html.escape(label)))
            h.append('<svg class="shp" xmlns="http://www.w3.org/2000/svg" '
                     'style="position:absolute;left:%.2fmm;top:%.2fmm;'
                     'width:%.2fmm;height:%.2fmm" viewBox="0 0 %.2f %.2f">'
                     '<g fill="none" stroke="#000" stroke-width="0.8">%s</g></svg>'
                     % (g['left'], top, g['text_w'], area_h,
                        g['text_w'], area_h, svg))
        else:
            for k, (txt, _) in enumerate(pg):
                y = g['top'] + k * ROW - INK_ABOVE
                h.append('<div class="ln" style="left:%.2fmm;top:%.2fmm;width:%.2fmm">%s</div>'
                         % (g['left'], y, g['text_w'], html.escape(txt)))
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
