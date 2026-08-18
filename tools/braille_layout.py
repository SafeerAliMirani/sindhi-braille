# -*- coding: utf-8 -*-
"""
Make a LAYOUT GUIDE for print-braille pages.

    python braille_layout.py page.brf -o guide.pdf --paper 280x292

Feed it the .brf that will be embossed. It draws, at true size, exactly where
every braille dot will land on the sheet, and marks the areas that must be left
free of ink. Give the PDF to the printer's designer as a background layer: they
place the colour artwork in the empty space, print on braille paper, and the
sheets then go through the embosser.

Colour first, braille second — never the other way round; a printer's rollers
flatten dots that are already there.
"""
import sys, argparse, subprocess, os

DOT, CELL, LINE, DOTD = 2.5, 6.2, 10.0, 1.5     # international braille, mm
BA = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="

def read_brf(path):
    raw = open(path, encoding='ascii', errors='replace').read()
    pages = raw.replace('\r\n', '\n').split('\f')
    return [[l for l in p.split('\n')] for p in pages if p.strip()]

def dots_of(ch):
    try: v = BA.index(ch.upper())
    except ValueError: return []
    return [i+1 for i in range(6) if v >> i & 1]

def page_svg(lines, pw, ph, mx, my, cols, rows):
    out = []
    used = set()
    for r, line in enumerate(lines[:rows]):
        for c, ch in enumerate(line[:cols]):
            if ch == ' ': continue
            used.add((c, r))
            x0 = mx + c*CELL
            y0 = my + r*LINE
            for d in dots_of(ch):
                col = 0 if d <= 3 else 1
                row = (d-1) % 3
                cx = x0 + col*DOT + DOTD/2
                cy = y0 + row*DOT + DOTD/2
                out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{DOTD/2:.2f}" '
                           f'fill="#111"/>')
    # the ink-free band for each line that carries braille
    bands = sorted({r for _, r in used})
    for r in bands:
        y0 = my + r*LINE - 1.2
        out.append(f'<rect x="{mx-2:.1f}" y="{y0:.2f}" width="{(cols-1)*CELL+DOT+DOTD+4:.1f}" '
                   f'height="{2*DOT+DOTD+2.4:.2f}" fill="none" stroke="#d33" '
                   f'stroke-width="0.3" stroke-dasharray="2 1.5"/>')
    return '\n'.join(out), bands

def build(brf, out_pdf, pw, ph, mx, my, cols, rows):
    pages = read_brf(brf)
    svgs = []
    for pi, lines in enumerate(pages, 1):
        body, bands = page_svg(lines, pw, ph, mx, my, cols, rows)
        free = [r for r in range(rows) if r not in bands]
        note = (f'page {pi} &nbsp;·&nbsp; {len(bands)} of {rows} lines carry braille &nbsp;·&nbsp; '
                f'artwork may use the {len(free)} empty line-bands')
        svgs.append(f'''<div class="sheet">
 <svg width="{pw}mm" height="{ph}mm" viewBox="0 0 {pw} {ph}">
  <rect x="0.5" y="0.5" width="{pw-1}" height="{ph-1}" fill="none" stroke="#bbb" stroke-width="0.3"/>
  <g stroke="#39c" stroke-width="0.5" fill="none">
    <path d="M {pw/2-15} 4 L {pw/2} 9 L {pw/2+15} 4"/>
  </g>
  <text x="{pw/2}" y="15" font-size="3.5" text-anchor="middle" fill="#39c">
    THIS EDGE FEEDS INTO THE EMBOSSER FIRST</text>
  {body}
  <text x="{mx}" y="{ph-6}" font-size="3" fill="#666">{note}</text>
 </svg></div>''')
    html = f'''<!doctype html><meta charset="utf-8"><style>
@page {{ size: {pw}mm {ph}mm; margin: 0 }}
body {{ margin:0 }} .sheet {{ page-break-after: always }}
</style>{''.join(svgs)}'''
    tmp = out_pdf + '.html'
    open(tmp, 'w', encoding='utf-8').write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto('file://' + os.path.abspath(tmp)); pg.wait_for_timeout(600)
        pg.pdf(path=out_pdf, width=f'{pw}mm', height=f'{ph}mm',
               margin={'top':'0','bottom':'0','left':'0','right':'0'},
               print_background=True)
        b.close()
    os.remove(tmp)
    return len(pages)

def main():
    ap = argparse.ArgumentParser(description='Layout guide for print-braille pages')
    ap.add_argument('brf'); ap.add_argument('-o','--out', default='layout-guide.pdf')
    ap.add_argument('--paper', default='280x292', help='sheet size in mm, e.g. 280x292 or 210x297')
    ap.add_argument('--margin', default='17x21', help='left x top margin in mm')
    ap.add_argument('--cols', type=int, default=40)
    ap.add_argument('--rows', type=int, default=25)
    a = ap.parse_args()
    pw, ph = (float(x) for x in a.paper.lower().split('x'))
    mx, my = (float(x) for x in a.margin.lower().split('x'))
    need_w = (a.cols-1)*CELL + DOT + DOTD + 2*mx
    need_h = (a.rows-1)*LINE + 2*DOT + DOTD + 2*my
    if need_w > pw or need_h > ph:
        print(f'WARNING: {a.cols} cells x {a.rows} lines needs {need_w:.0f} x {need_h:.0f} mm '
              f'but the sheet is {pw:.0f} x {ph:.0f} mm.')
        print(f'         At this paper size the line fits '
              f'{int((pw-2*mx-DOT-DOTD)/CELL)+1} cells.')
    n = build(a.brf, a.out, pw, ph, mx, my, a.cols, a.rows)
    print(f'wrote {a.out} — {n} sheet(s) at {pw:.0f} x {ph:.0f} mm, true size')

if __name__ == '__main__':
    main()
