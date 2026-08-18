# -*- coding: utf-8 -*-
"""
Build the on-screen check sheet for verse, arithmetic and other languages.

    python make_check_sheet.py     # ../test-sheets/CHECK-poetry-maths-foreign.html

One row per case: the Sindhi you type, the braille it becomes, the dot numbers,
and what comes back when that braille is read again.  A row whose text does not
come back identically is marked, so that a property of the code is never mistaken
for a fault in the software.

The same material, embossable, is test-sheets/print-3-poetry-maths-foreign.brf.
"""
import io, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindhi_braille as sb

MATHS = [
    ('8 + 9 = 17',      'the guide&rsquo;s own first sum, p.49'),
    ('20 − 13 = 7', 'subtraction, p.50'),
    ('12 × 8 = 96', 'multiplication &mdash; the × sign is 5-6 2-3-6, the same '
                         'two cells that open a foreign word. Which one it is, is '
                         'decided by whether a word follows with no space'),
    ('91 ÷ 7 = 13', 'division, p.51'),
    ('3/7 1/2 13/44',   'fractions &mdash; the denominator drops to the lower dots, '
                        'and a numerator of 1 is not written at all'),
    ('1.75',            'decimal point &mdash; dot 2, p.50'),
    ('1,000',           'thousands comma &mdash; dot 3, because dot 2 is taken'),
    ('2:3',             'ratio &mdash; dots 2-5, then a fresh number sign'),
    ('50%',             'per cent &mdash; the guide prints the sign <em>before</em> '
                        'the number, and it carries no letter sign'),
    ('1%',              'the guide&rsquo;s own example, p.51'),
    ('(8 + 9) = 17',    'brackets in arithmetic are 126 and 345 (p.53), not the '
                        'prose 2356 &mdash; a different set of cells entirely'),
    ('{12 + 3} = 15',   'braces, p.53'),
    ('VIII IX X',       'Roman numerals, one letter sign per numeral'),
    ('ا. ب. ج. د.',
                        'exercise labels &mdash; letter sign, letter, full stop'),
    ('ڪتاب جو قيمت 250 روپيا آهي.',
                        'a number inside ordinary prose'),
]

FOREIGN = [
    ('هي Thanks لفظ آهي.',
     'one English word. The guide&rsquo;s own example prints Thanks as '
     '6 2345 125 1 1345 13 234 &mdash; dot 6 is the capital'),
    ('اسڪول جو نالو City School آهي.',
     'two English words &mdash; <strong>one</strong> pair of marks around the '
     'whole run, not one pair each (p.46)'),
    ('مان Computer Science پڙهان ٿو.',
     'capitals inside a longer run'),
    ('هن ۾ اردو لفظ کتاب آهي.',
     'an Urdu word. It is in the same script, so it needs no marks &mdash; it is '
     'simply spelled with the Sindhi letters'),
    ('هي word هڪ لفظ آهي',
     'lower case only, no capital sign'),
]

GRADE2 = [
    ('اسين ٿو وڃون. البته توهان ڀلو آهي.',
     'a whole sentence in contracted braille &mdash; thirty-four cells become '
     'twelve. Each contraction is a series prefix and one letter'),
    ('اسين به ٻه ڀلو توهان ٿو',
     'the whole-word series: a single letter standing alone as a word'),
    ('آهي اوهان بيهن ٻاهر ڀلائي', 'the dot 5 series'),
    ('اڳتي بابت پاڻ', 'the dots 4-5 series'),
    ('شروع جنهن صورت خراب اڳواڻ', 'the dots 4-5-6 series'),
    ('تيئن ته ڇاڪاڻ ته مطلب ته',
     'the dot 6 series &mdash; three of these stand for a phrase, not a word'),
    ('البته اتفاق امڪان بعد', 'the Sindhi abbreviations'),
    ('آباد آزارا',
     'the ڳانڊڙا groups, written inside a word and never at its start'),
]

POEM = ['سنڌ ڀٽائي جي ڀونءِ',
        'هتي امن ۽ محبت آهي',
        'لطيف چوي ٿو سچ']
TAKHALLUS = 'لطيف'


def uni(lines):
    return '⠀'.join(''.join(sb.cell_to_unicode(c) for c in cs)
                         for line in lines for cs in line)


def dots(lines):
    return '   '.join('-'.join(cs) for line in lines for cs in line)


def _dir(t):
    """a row of arithmetic must not be flipped by the bidi algorithm"""
    return 'rtl' if any('\u0600' <= c <= '\u06ff' for c in t) else 'ltr'


def row(text, note, **kw):
    lines = sb.translate(text, **kw)
    r = sb.back(lines, poetry=kw.get('poetry', False),
                grade2=kw.get('grade2', False))
    same = ' '.join(r.split()) == ' '.join(text.split())
    return ('<tr class="%s">'
            '<td class="sd" dir="%s">%s</td>'
            '<td class="brl">%s</td>'
            '<td class="dots">%s</td>'
            '<td class="sd" dir="%s">%s</td>'
            '<td class="note">%s</td></tr>'
            % ('ok' if same else 'diff',
               _dir(text), html.escape(text).replace('\n', '<br>'),
               uni(lines), dots(lines),
               _dir(r), html.escape(r).replace('\n', '<br>'), note))


def section(title, sd, rows):
    return ('<h2>%s<span class="sd">%s</span></h2><table>'
            '<thead><tr><th>you type</th><th>braille</th><th>dots</th>'
            '<th>read back</th><th>what it tests</th></tr></thead><tbody>%s'
            '</tbody></table>' % (title, sd, ''.join(rows)))


CSS = """
:root{--ink:#16181d;--ink2:#4a5160;--ink3:#7b8496;--line:#e3e6ec;--panel:#fff;
  --bg:#f6f7f9;--ok:#1f8a4c;--diff:#b26a00}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:44px 24px 80px}
h1{font-size:30px;margin:0 0 8px;letter-spacing:-.02em}
.lede{color:var(--ink2);max-width:76ch;margin:0 0 30px}
h2{font-size:19px;margin:46px 0 12px;display:flex;align-items:baseline;gap:12px}
h2 .sd{font-size:16px;color:var(--ink3);font-weight:400}
table{width:100%;border-collapse:collapse;background:var(--panel);
  border:1px solid var(--line);border-radius:12px;overflow:hidden}
th{text-align:start;font-size:11px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--ink3);font-weight:600;padding:11px 13px;
  border-bottom:1px solid var(--line);background:#fbfcfd}
td{padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
.sd{font-family:'Noto Naskh Arabic','Segoe UI',serif;font-size:17px;
  unicode-bidi:isolate}
h2 .sd{direction:rtl}
.brl{font-size:20px;line-height:1.4;letter-spacing:.5px;word-break:break-all;
  direction:ltr;unicode-bidi:isolate;max-width:300px}
.dots{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10.5px;
  color:var(--ink3);direction:ltr;unicode-bidi:isolate;max-width:250px}
.note{font-size:13px;color:var(--ink2);max-width:36ch}
tr.ok td:first-child{box-shadow:inset 3px 0 0 var(--ok)}
tr.diff td:first-child{box-shadow:inset 3px 0 0 var(--diff)}
.key{margin:20px 0 0;font-size:13.5px;color:var(--ink2);max-width:80ch}
.key b{color:var(--ink)}
footer{margin-top:56px;padding-top:20px;border-top:1px solid var(--line);
  font-size:13px;color:var(--ink3)}
"""

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Check sheet — verse, arithmetic and other languages</title>
<style>%s</style></head><body><div class="wrap">
<h1>Check sheet — verse, arithmetic, other languages</h1>
<p class="lede">The three parts of the code that had not been checked. Each row
shows what you type, the braille it becomes, the dot numbers, and what comes back
when that braille is read again. Compare the <em>dots</em> against the printed
guide, and the <em>read back</em> against the first column.</p>
"""

KEY = """<p class="key"><b>Green edge</b> — the text comes back exactly as it went
in. <b>Amber edge</b> — something changed. The only amber rows here should be the
ones where Sindhi writes something braille has no cell for: ۾ becomes مين, ۽
becomes اءين, ئ becomes a bare ء, and the diacritics are dropped. Anything else
amber is a real finding.</p>
<footer>Generated by <code>tools/make_check_sheet.py</code>. The same material,
embossable, is <code>test-sheets/print-3-poetry-maths-foreign.brf</code>.<br>
Digital implementation by Safeer Ali Mirani, 2026, in partnership with Riaz
Hussain Memon.</footer>
</div></body></html>"""


def main():
    sb.load_words()
    sb.load_grade2()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                       'test-sheets', 'CHECK-poetry-maths-foreign.html')
    body = [
        section('Arithmetic', 'حساب',
                [row(t, n) for t, n in MATHS]),
        section('Other languages inside Sindhi',
                'سنڌيءَ ۾ ٻيون ٻوليون',
                [row(t, n) for t, n in FOREIGN]),
        section('Contracted braille (Grade 2)', 'درجو ٻيو',
                [row(t, n, grade2=True) for t, n in GRADE2]),
        section('Verse', 'شعر',
                [row('\n'.join(POEM),
                     'a whole bait: 12356 twice at the start of the stanza, once '
                     'more attached to the end of every hemistich, a full stop '
                     'closing the stanza, and dot 2 immediately before the '
                     'pen-name (pp.40&ndash;41)',
                     poetry=True, takhallus=TAKHALLUS)]),
    ]
    doc = (HEAD % CSS) + ''.join(body) + KEY
    io.open(out, 'w', encoding='utf-8', newline='\n').write(doc)
    print('%s  %.1f KB' % (os.path.basename(out),
                           len(doc.encode('utf-8')) / 1024.0))


if __name__ == '__main__':
    main()
