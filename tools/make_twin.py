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
    rows = int((page_h - 2 * pp.EDGE_Y) // ROW)
    return dict(left=left, text_w=text_w, rows=rows,
                top=pp.EDGE_Y, page_w=page_w, page_h=page_h)


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


def build(src, width, bind, out_dir, title):
    g = geometry(width, bind)
    lines = []                                  # (sindhi text, [cells])
    for s in sentences(src):
        for parts, _ in wrap(s, width):
            txt = ''.join(w for w, _ in parts)
            cells = [c for _, cs in parts for c in cs]
            lines.append((txt, cells))

    pages = [lines[i:i + g['rows']] for i in range(0, len(lines), g['rows'])] or [[]]

    # ---- the braille file -------------------------------------------------
    brf = []
    # Page one is the registration target: every line a solid bar of full cells,
    # to be embossed onto the printed test sheet. If every bar sits inside its
    # printed band, the two machines agree and the book can be run.
    for _ in range(g['rows']):
        brf.append('=' * width)
        brf.append('')
    brf.append('\f')
    for pg in pages:
        for txt, cells in pg:
            brf.append(''.join(sb.cell_to_ascii(c) if c else ' ' for c in cells))
            brf.append('')                      # the blank line the ink sits in
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

    for pg in pages:
        h.append('<section class="page">')
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
