# -*- coding: utf-8 -*-
"""
Build website/index.html from its two sources.

    python build.py

`page.html` is the page: markup, styling, animation, and all the interface code.
`engine.js` is the translator: the code tables, the forward translation, the
back translation and the word list — a direct port of tools/sindhi_braille.py.

The build is one substitution: engine.js replaces the `/*__ENGINE__*/` marker
inside page.html's script block. The result is a single file with no external
requests, which is what lets the site open offline and be handed to anyone on a
USB stick.

Keep the two engines in step. When tools/sindhi_braille.py changes, change
engine.js the same way, then run this, then re-run the cross-check.
"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, '..', 'index.html')

page   = io.open(os.path.join(HERE, 'page.html'),  encoding='utf-8').read()
engine = io.open(os.path.join(HERE, 'engine.js'), encoding='utf-8').read()

if '/*__ENGINE__*/' not in page:
    raise SystemExit('page.html has no /*__ENGINE__*/ marker')

html = page.replace('/*__ENGINE__*/', engine)
io.open(OUT, 'w', encoding='utf-8', newline='').write(html)
print('index.html  %.1f KB' % (len(html.encode('utf-8')) / 1024.0))
