# -*- coding: utf-8 -*-
"""
Sheet 7 — ه or ھ. One question, asked six times.

    python tools/make_hey_sheet.py --width 38

Sindhi digital text is written with two different letters that look alike and
are not alike in braille:

    ه   U+0647   dots 1-2-5
    ھ   U+06BE   dots 2-3-6

The committee's own publications use both, for the same words: آهي appears and so
does آھي, ته and تھ, هن and ھن. 326 words in our corpus carry one and 361 carry
the other.

In print that is an orthographic habit. In braille it is two different cells, so
a book has to choose, and every occurrence follows the choice. The first lesson
text written for the primer used ه 207 times and ھ not once.

This sheet prints six ordinary words twice, once each way, and asks him which is
right. Nothing else on it.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

PAIRS = [('گهر', 'گھر'), ('آهي', 'آھي'), ('پڙهان', 'پڙھان'),
         ('هي', 'ھي'), ('ته', 'تھ'), ('پنهنجو', 'پنھنجو')]


def label(n):
    return [sb.LETTERSIGN] + sb.LETTER[n] + [sb.PUNCT['.']]

LET = ['ا', 'ب', 'ج', 'د', 'ه', 'و']


def build(width=38):
    sb.load_words()
    lines = []
    for i, (with_he, with_do) in enumerate(PAIRS):
        a = [label(LET[i])] + sb.translate(with_he)[0]
        b = [label(LET[i])] + sb.translate(with_do)[0]
        lines.append(a)
        lines.append(b)
        lines.append([])
    brf = sb.to_brf(lines, width=width, height=25)
    out = os.path.join(ROOT, 'test-sheets', 'print-7-hey.brf')
    io.open(out, 'w', encoding='ascii', newline='').write(brf)
    rows = [r for r in brf.replace('\f', '').split('\r\n') if r]
    print('print-7-hey.brf  %d lines, widest %d cells'
          % (len(rows), max(len(r) for r in rows)))

    key = """# Sheet 7 — ه or ھ

Six words, each printed twice: once with **ه** (dots 1-2-5) and once with
**ھ** (dots 2-3-6). Same label letter on both lines of a pair.

| pair | first line | second line |
|---|---|---|
| ا. | گهر | گھر |
| ب. | آهي | آھي |
| ج. | پڙهان | پڙھان |
| د. | هي | ھي |
| ه. | ته | تھ |
| و. | پنهنجو | پنھنجو |

**Read him both lines of a pair and ask which one is the word.** Do not tell him
they differ by one cell, and do not tell him which is which.

## Why this matters more than it looks

In print the two letters look nearly alike and Sindhi writers use both. In
braille they are **different cells**, so the book must choose one and every
occurrence follows.

This is not a small number of words. The first draft of the primer's lesson text
used ه **207 times in 161 lines** and ھ not once. If the standard wants ھ in
گھر, then every one of those is the wrong cell, and a child would learn the wrong
letter from the first page.

The committee's own publications will not settle it: our corpus has 326 words
with ه and 361 with ھ, including the same word spelled both ways.

## What we need from him

1. Which cell belongs in each of the six words.
2. Whether there is a rule, or whether it is word by word. If there is a rule,
   the software can enforce it and the typist never has to think about it again.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
    io.open(os.path.join(ROOT, 'test-sheets', 'HEY-KEY.md'), 'w',
            encoding='utf-8', newline='\n').write(key)
    print('HEY-KEY.md written')


if __name__ == '__main__':
    a = sys.argv[1:]
    w = int(a[a.index('--width') + 1]) if '--width' in a else 38
    build(w)
