# -*- coding: utf-8 -*-
"""Build the showcase sheet: A4, colour, print-ready."""
import io, os, sys, json
sys.path.insert(0, '/tmp/sb')
import sindhi_braille as sb

L1 = ['1','12','14','145','15','124','1245','125','24','245']
add = lambda c, d: ''.join(sorted(set(c) | set(d)))
low = lambda c: ''.join(sorted({'1':'2','2':'3','4':'5','5':'6'}.get(x, x) for x in c))
LINES = {1:list(L1), 2:[add(c,'3') for c in L1], 3:[add(c,'36') for c in L1],
         4:[add(c,'6') for c in L1], 5:[low(c) for c in L1],
         6:['34','346','3456','345','3','36'], 7:['4','45','456','5','46','56','6']}
member = {}
for n, cs in LINES.items():
    for c in cs: member.setdefault(c, n)

rows = {n: [] for n in range(1, 8)}
for ch, cells in sb.LETTER.items():
    rows[member[cells[0]]].append((ch, cells))

# mineral palette, one per line
INK = {1:'#2b3a67', 2:'#1f5f5b', 3:'#7a5c1e', 4:'#8c3d2b', 5:'#5a3357', 6:'#3f4a52'}
NAME = {1:'first line', 2:'add dot 3', 3:'add dots 3 6', 4:'add dot 6',
        5:'lower every dot', 6:'the remainder'}

def cell(dots, col, s=1.3):
    """one braille cell, drawn at true proportion"""
    w, h = 13*s, 20*s
    xs, ys = [4.0*s, 9.4*s], [4.2*s, 10.0*s, 15.8*s]
    out = ['<svg class="c" viewBox="0 0 %g %g" width="%g" height="%g">' % (w,h,w,h)]
    for ci in range(2):
        for ri in range(3):
            n = str(ri+1+3*ci)
            on = n in dots
            out.append('<circle cx="%g" cy="%g" r="%g" fill="%s"%s/>'
                       % (xs[ci], ys[ri], 1.95*s if on else 0.62*s,
                          col if on else '#c9c3b6', '' if on else ' opacity=".9"'))
    return ''.join(out) + '</svg>'

def glyph(ch, cells, col):
    dots = '<span class="cells">' + ''.join(cell(c, col) for c in cells) + '</span>'
    num = '-'.join(cells)
    two = ' two' if len(cells) > 1 else ''
    return ('<div class="g%s"><span class="sd" style="color:%s">%s</span>%s'
            '<span class="n">%s</span></div>' % (two, col, ch, dots, num))

body = []
for n in range(1, 7):
    col = INK[n]
    items = ''.join(glyph(ch, cells, col) for ch, cells in rows[n])
    body.append(
      '<section class="ln"><div class="lbl"><span class="num" style="color:%s">%d</span>'
      '<span class="nm">%s</span><span class="ct">%d</span></div>'
      '<div class="row">%s</div></section>' % (col, n, NAME[n], len(rows[n]), items))

seven = ''.join(
    '<div class="p"><span class="cells">%s</span><span class="n">%s</span></div>'
    % (cell(c, '#8a8578'), c) for c in LINES[7])

SENT = 'سنڌي ٻولي هڪ شاهوڪار ٻولي آهي.'
strip = ''.join('<span class="sc">%s</span>' % ''.join(cell(c, '#1a1a17') for c in cs)
                for cs in sb.translate(SENT)[0])

# The same sentence as the strip above, so the two bands compare directly.
# Not a constructed one: this is the sentence used throughout the project's
# tests, and the reduction it gives is the honest one for ordinary prose.
G2SENT = SENT
sb.load_grade2()
g1 = sb.translate(G2SENT)[0]
g2 = sb.translate(G2SENT, grade2=True)[0]
n1 = sum(len(t) for t in g1); n2 = sum(len(t) for t in g2)
def band(toks, col):
    return ''.join('<span class="sc">%s</span>' % ''.join(cell(c, col) for c in cs)
                   for cs in toks)
uncon, con = band(g1, '#a49d8c'), band(g2, '#1f5f5b')

HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Standard Sindhi Braille — the fifty-two letters</title>
<style>
@page{size:A4 portrait;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:210mm;height:297mm}
body{background:#faf7f0;color:#1a1a17;
  font:400 10px/1.4 "Helvetica Neue",Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;padding:11mm 13mm 26mm}
.sd{font-family:"Noto Naskh Arabic","Scheherazade New","Segoe UI",serif}
header{display:flex;justify-content:space-between;align-items:flex-end;
  padding-bottom:3.4mm;border-bottom:.5px solid #ccc5b4}
h1{font-size:23px;font-weight:400;letter-spacing:-.015em;line-height:1.05}
h1 em{font-style:normal;color:#8a8578}
.meta{text-align:right;font-size:7.2px;letter-spacing:.1em;text-transform:uppercase;
  color:#8a8578;line-height:1.7}
.intro{margin:3.6mm 0 5.0mm;font-size:8.6px;line-height:1.6;color:#57534a;max-width:138mm}
.intro b{font-weight:600;color:#1a1a17}

.ln{margin-bottom:3.6mm}
.lbl{display:flex;align-items:baseline;gap:2.4mm;margin-bottom:1.6mm}
.num{font:600 11px/1 ui-monospace,Menlo,monospace}
.nm{font-size:7.4px;letter-spacing:.14em;text-transform:uppercase;color:#8a8578}
.ct{margin-left:auto;font:400 7.4px ui-monospace,Menlo,monospace;color:#c0b9a8}
.row{display:flex;gap:1.6mm;flex-wrap:nowrap}
.g{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;
  gap:1.15mm;padding:2.1mm .4mm 1.7mm;border:.4px solid #e6e0d2;border-radius:1.4mm;
  background:#fffdf8}
.g.two{flex:1.9 1 0}
.g .sd{font-size:19px;line-height:1}
.cells{display:flex;gap:.9mm;align-items:flex-start}
.c{display:block}
.n{font:400 6.8px/1 ui-monospace,Menlo,monospace;color:#a49d8c;letter-spacing:.03em}

.seven{margin-top:1.0mm;padding-top:3.4mm;border-top:.5px solid #e6e0d2;
  display:flex;align-items:center;gap:3mm}
.seven .cap{font-size:7.4px;letter-spacing:.14em;text-transform:uppercase;
  color:#8a8578;width:31mm;line-height:1.5}
.seven .set{display:flex;gap:2.4mm}
.p{display:flex;flex-direction:column;align-items:center;gap:.7mm}
.note{font-size:7.6px;color:#8a8578;line-height:1.6;max-width:74mm}

.strip{margin-top:3.6mm;padding-top:3.0mm;border-top:.5px solid #e6e0d2}
.strip .cap{font-size:7.4px;letter-spacing:.14em;text-transform:uppercase;
  color:#8a8578;margin-bottom:1.8mm}
.line{display:flex;gap:2.6mm;align-items:flex-start;flex-wrap:wrap}
.sc{display:flex;gap:.9mm}
.trans{margin-top:2.0mm;font-size:11px;color:#57534a;direction:rtl}
.pair{display:flex;align-items:flex-start;gap:5mm;margin-top:2.8mm}
.tag{width:23mm;flex:0 0 23mm;font-size:7px;letter-spacing:.13em;text-transform:uppercase;
  color:#8a8578;line-height:1.5;padding-top:.4mm}
.tag span{display:block;font-family:ui-monospace,Menlo,monospace;font-size:7.6px;
  letter-spacing:0;text-transform:none;color:#c0b9a8}

footer{position:absolute;left:13mm;right:13mm;bottom:7mm;display:flex;
  justify-content:space-between;align-items:flex-end;
  padding-top:2.6mm;border-top:.5px solid #ccc5b4;font-size:6.9px;
  letter-spacing:.05em;color:#8a8578;line-height:1.65}
footer b{font-weight:600;color:#1a1a17}
</style></head><body>

<header>
  <h1>Standard Sindhi Braille<br><em>the fifty-two letters</em></h1>
  <div class="meta">Sindhi Language Authority · 7 November 2016<br>
  Perso-Arabic · Pakistan · 63 cells</div>
</header>

<p class="intro">Every letter of Sindhi sits inside the six-line structure Louis
Braille published in 1829. Each line takes the ten shapes of the first and moves
them: <b>add dot 3</b>, <b>add dots 3 and 6</b>, <b>add dot 6</b>, <b>lower every
dot by one row</b>. Nothing in this sheet was designed. It was found, in the
committee's own printed book, and set here in the order the structure already
had.</p>

__BODY__

<div class="seven">
  <div class="cap">the seventh line<br>carries no letter</div>
  <div class="set">__SEVEN__</div>
  <div class="note">These seven cells are reserved. Six of them open a Grade&nbsp;2
  contraction series, one is the letter sign, and the last is a group prefix. No
  Sindhi letter is written with any of them.</div>
</div>

<div class="strip">
  <div class="cap">one sentence, twice · at true size · 2.5 mm dot pitch · 6.2 mm cell pitch</div>
  <div class="pair">
    <div class="tag">grade one<span>__N1__ cells</span></div>
    <div class="line">__STRIP__</div>
  </div>
  <div class="pair">
    <div class="tag">grade two<span>__N2__ cells</span></div>
    <div class="line teal">__CON__</div>
  </div>
  <div class="trans sd">__SENT__</div>
</div>

<footer>
  <div>Digital implementation, verification and documentation by
  <b>Safeer Ali Mirani</b>, 2026<br>
  in partnership with <b>Riaz Hussain Memon</b> · Pakistan Association of the
  Blind (Sindh) · member of the authoring committee<br>
  with <b>Mansoor Ali Kori</b>, who works alongside him on the composing and has
  been part of the meetings throughout</div>
  <div style="text-align:right">The braille code is the committee's<br>
  and is not altered here</div>
</footer>
</body></html>"""

out = (HTML.replace('__BODY__', '\n'.join(body))
           .replace('__SEVEN__', seven)
           .replace('__STRIP__', strip)
           .replace('__SENT__', SENT)
           .replace('__UNCON__', uncon).replace('__CON__', con)
           .replace('__G2SENT__', G2SENT)
           .replace('__N1__', str(n1)).replace('__N2__', str(n2)))
io.open('/tmp/poster/sheet.html', 'w', encoding='utf-8').write(out)
print('sheet.html %.1f KB' % (len(out.encode())/1024))
