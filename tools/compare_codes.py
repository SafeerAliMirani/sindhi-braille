# -*- coding: utf-8 -*-
"""
Compare Standard Sindhi Braille against the neighbouring Perso-Arabic codes.

    python compare_codes.py            # a report
    python compare_codes.py --brief    # one line per code

WHAT THIS IS FOR, AND WHAT IT IS NOT

Sindhi braille is defined by the Sindhi Language Authority committee, and no
other code overrules it.  Arabic, Persian and Urdu braille cannot tell us what
Sindhi *should* be.

What they can do is corroborate.  These scripts share most of their letters, so
where four codes independently give a letter the same cell, our reading of the
Sindhi book is very unlikely to be a transcription slip.  Where Sindhi differs,
there should be a reason visible in the alphabet itself, and if there is not,
that is worth looking at again.

This is the only check in the project that uses evidence neither the author nor
Riaz Hussain Memon produced.  It is weaker than a blind reader on paper and
stronger than the software agreeing with itself.

The reference tables are liblouis's own, in brailleTables/reference/.
"""
import io, os, re, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindhi_braille as sb

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'brailleTables', 'reference')

CODES = [
    ('Arabic',  ['ar-ar-g1-core.uti']),
    ('Persian', ['fa-ir-g1.utb']),
    ('Urdu',    ['ur-pk-g1.utb']),
]

RULE = re.compile(
    r'^(?:no(?:back|for)\s+)?(?:letter|sign|punctuation|always|lowercase)'
    r'\s+(\S+)\s+([0-9]+(?:-[0-9]+)*)(?:\s|$)')


def load(names):
    """letter -> dots, from one or more liblouis tables"""
    out = {}
    for n in names:
        p = os.path.join(REF, n)
        if not os.path.exists(p):
            continue
        for line in io.open(p, encoding='utf-8', errors='replace'):
            m = RULE.match(line.split('#')[0])
            if not m:
                continue
            ch, dots = m.group(1), m.group(2)
            esc = re.fullmatch(r'\\x([0-9a-fA-F]{4})', ch)
            if esc:
                ch = chr(int(esc.group(1), 16))
            if len(ch) == 1 and '؀' <= ch <= 'ۿ':
                out.setdefault(ch, dots)
    return out


def compare():
    """-> [(code name, agree, [(letter, ours, theirs)])]"""
    rows = []
    for name, files in CODES:
        theirs = load(files)
        if not theirs:
            continue
        agree, diff = 0, []
        for ch, cells in sb.LETTER.items():
            ours = '-'.join(cells)
            t = theirs.get(ch)
            if t is None:
                continue
            if t == ours:
                agree += 1
            else:
                diff.append((ch, ours, t))
        rows.append((name, agree, sorted(diff)))
    return rows


def unassigned_cells():
    """Cells Standard Sindhi Braille gives no meaning to at all.

    Everything counts: letters, diacritics, punctuation, the number and letter
    signs, the arithmetic and bracket cells, the verse marks, and the Grade 2
    series prefixes.  What is left over is genuinely spare."""
    used = set()
    for cells in sb.LETTER.values():   used |= set(cells)
    for cells in sb.DIGRAPH.values():  used |= set(cells)
    used |= set(sb.DIACRITIC.values())
    used |= set(sb.PUNCT.values())
    used |= set(sb.DIGIT.values()) | set(sb.LOWDIGIT.values())
    for v in list(sb.MATH.values()) + list(sb.QUOTE.values()) + \
             list(sb.BRACKET.values()) + list(sb.MATHBRACKET.values()):
        used |= set(v)
    used |= {sb.NUMSIGN, sb.NUMEND, sb.LETTERSIGN, sb.RATIO, sb.DECPT,
             sb.NUMCOMMA, sb.LATINCAP, sb.WAW_ATF, sb.SLASH, sb.TAKHALLUS}
    used |= set(sb.DOUBLING) | set(sb.POETRY) | set(sb.FOOTNOTE) | set(sb.BLANK3)
    used |= set(sb.FOREIGN_OPEN) | set(sb.FOREIGN_CLOSE)
    sb.load_grade2()
    for cells in sb.GRADE2.values():   used |= set(cells)
    for _, cells in sb.GRADE2P:        used |= set(cells)
    for _, cells in sb.GRADE2G:        used |= set(cells)

    every = set()
    for n in range(1, 64):
        every.add(''.join(str(i + 1) for i in range(6) if n >> i & 1))
    free = sorted(every - used, key=lambda s: (len(s), s))
    out = []
    for name, files in CODES:
        t = load(files)
        for c in free:
            for ch, d in t.items():
                if d == c:
                    out.append((c, name, ch))
    return free, out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--brief', action='store_true')
    a = ap.parse_args()

    rows = compare()
    if not rows:
        print('no reference tables found in %s' % REF)
        return 1

    total_a = sum(r[1] for r in rows)
    total_d = sum(len(r[2]) for r in rows)

    if a.brief:
        print('%d of %d shared letters agree with Arabic, Persian and Urdu braille'
              % (total_a, total_a + total_d))
        return 0

    print(__doc__.split('WHAT THIS IS FOR')[0].strip())
    print()
    for name, agree, diff in rows:
        n = agree + len(diff)
        print('%-8s  %2d of %2d shared letters agree' % (name, agree, n))
        for ch, ours, theirs in diff:
            print('              %s   Sindhi %-8s %s %s' % (ch, ours, name.lower(), theirs))
    print()
    print('%d of %d agreements across the three codes.' % (total_a, total_a + total_d))

    free, found = unassigned_cells()
    print()
    if not free:
        print('Every one of the 63 cells carries something in this code.')
    else:
        print('Of the 63 cells, %s carr%s nothing at all in either grade: %s'
              % (len(free), 'ies' if len(free) == 1 else 'y', ', '.join(free)))
        if found:
            print('The neighbouring codes do use %s:'
                  % ('it' if len(free) == 1 else 'some of them'))
            for c, name, ch in found:
                print('   %-6s %-8s %s' % (c, name, ch))
        else:
            print('The neighbouring codes leave %s empty too.'
                  % ('it' if len(free) == 1 else 'them'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
