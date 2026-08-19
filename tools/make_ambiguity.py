# -*- coding: utf-8 -*-
"""
Derive the ambiguity table from the code tables, and write it into the website.

    python make_ambiguity.py            # rewrite website/src/engine.js
    python make_ambiguity.py --check    # fail if the file is out of date

The table under "Where the difficulty is" used to be written by hand. It drifted:
it listed three readings for dot 2 when the tables give five, and it was missing
two cells entirely. Deriving it means it cannot drift again — when a table in
sindhi_braille.py changes, this changes with it.

What counts as a reading of a single cell:

  * a letter written in one cell
  * a diacritic
  * a punctuation mark
  * a digit, and a lower digit
  * a sign that is one cell on its own (number sign, letter sign, decimal point,
    the pen-name mark, the ratio mark, the و joiner)
  * a mark made of the same cell repeated (the doubling mark, the verse marks,
    the footnote mark, the blank line) — the cell is the mark, twice

Two-cell marks whose cells differ are deliberately left out: the foreign-word
marks and the arithmetic signs mean nothing cell by cell, only as a pair. They
are described in the note under the table instead.
"""
import io, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

ENGINE = os.path.join(ROOT, 'website', 'src', 'engine.js')
OPEN, CLOSE = 'const AMBIGUITY = [', '];'

# Each label is a pair: English, then Sindhi.  The site shows one or the other,
# so a Sindhi reader gets a Sindhi table rather than an English one sitting the
# wrong way round on the page.
DIA = {'َ': ('zabar', 'زبر'), 'ِ': ('zer', 'زير'), 'ُ': ('pesh', 'پيش'),
       'ّ': ('tashdid', 'شد'), 'ْ': ('jazam', 'جزم'),
       'ٍ': ('double zer', 'ٻہ زير'), 'ٌ': ('double pesh', 'ٻہ پيش'),
       'ٰ': ('khari zabar', 'کڙي زبر')}
PUN = {'.': ('full stop', 'ٽِڪ'), '،': ('comma', 'ڪاما'),
       '؟': ('question', 'سواليہ'), '!': ('exclamation', 'جذباتي'),
       '؛': ('semicolon', 'ننڍو وقفو'), ':': ('colon', 'ٻہ ٽِڪ')}
SIGN = {'NUMSIGN': ('number sign', 'عدد جو نشان'),
        'LETTERSIGN': ('letter sign', 'اکر جو نشان'),
        'DECPT': ('decimal point', 'ڏهائي جي ٽِڪ'),
        'TAKHALLUS': ('pen-name mark', 'تخلص جو نشان'),
        'RATIO': ('ratio mark', 'نسبت جو نشان'),
        'WAW_ATF': ('و joiner', 'واو عطف')}
RUN = {'DOUBLING': ('doubling mark', 'ورجاءَ جو نشان'),
       'POETRY': ('verse mark', 'شعر جو نشان'),
       'FOOTNOTE': ('footnote mark', 'حاشيي جو نشان'),
       'BLANK3': ('blank line', 'خالي جاءِ')}
KIND = {'letter': 'اکر', 'diacritic': 'اعرابو', 'punctuation': 'رمز',
        'digit': 'عدد', 'lower digit': 'هيٺيون عدد', 'sign': 'نشان'}


def pair(text, kind):
    """'ب (letter)' in English, 'ب (اکر)' in Sindhi.  The Sindhi names of the
    signs already say نشان, so they are left to speak for themselves."""
    en, sd = (text, text) if isinstance(text, str) else text
    return ['%s (%s)' % (en, kind),
            sd if kind == 'sign' else '%s (%s)' % (sd, KIND[kind])]


def all_readings():
    """Every single-cell assignment the code makes, including the cells that
    carry only one. The paper counts meanings from this, so the count and the
    table of shared cells are the same universe rather than two."""
    return _use()


def _use():
    use = collections.defaultdict(list)

    def put(cell, text):
        if text not in use[cell]:
            use[cell].append(text)

    for ch, cs in sb.LETTER.items():
        if len(cs) == 1: put(cs[0], pair(ch, 'letter'))
    for ch, c in sb.DIACRITIC.items(): put(c, pair(DIA.get(ch, ch), 'diacritic'))
    for ch, c in sb.PUNCT.items():
        if ch in PUN: put(c, pair(PUN[ch], 'punctuation'))
    for d, c in sb.DIGIT.items():    put(c, pair(d, 'digit'))
    for d, c in sb.LOWDIGIT.items(): put(c, pair(d, 'lower digit'))

    for name, label in SIGN.items():
        v = getattr(sb, name, None)
        if isinstance(v, str): put(v, pair(label, 'sign'))
    for name, label in RUN.items():
        v = getattr(sb, name, None)
        if isinstance(v, list) and len(set(v)) == 1: put(v[0], pair(label, 'sign'))

    return use


def readings():
    use = _use()
    return {c: v for c, v in use.items() if len(v) > 1}


def table():
    m = readings()
    # most ambiguous first, then by cell, so the hard cases are read first
    order = sorted(m, key=lambda c: (-len(m[c]), len(c), c))
    return [{'cell': c, 'n': len(m[c]), 'readings': m[c]} for c in order]


def block(rows):
    body = ',\n'.join(json.dumps(r, ensure_ascii=False, indent=0)
                      .replace('\n', ' ').replace('  ', ' ') for r in rows)
    return OPEN + '\n' + body + '\n' + CLOSE


def main(check=False):
    rows = table()
    src = io.open(ENGINE, encoding='utf-8').read()
    a = src.index(OPEN)
    b = src.index(CLOSE, a) + len(CLOSE)
    out = src[:a] + block(rows) + src[b:]
    if check:
        ok = out == src
        print('ambiguity table is %s' % ('up to date' if ok else 'OUT OF DATE'))
        return 0 if ok else 1
    io.open(ENGINE, 'w', encoding='utf-8', newline='\n').write(out)
    print('%d cells carry more than one reading' % len(rows))
    for r in rows:
        print('  %-6s %d  %s' % (r['cell'], r['n'],
                                 ' / '.join(x[0] for x in r['readings'])))
    return 0


if __name__ == '__main__':
    raise SystemExit(main('--check' in sys.argv))
