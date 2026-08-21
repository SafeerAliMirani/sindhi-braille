# -*- coding: utf-8 -*-
"""
Sindhi <-> braille, in the code of Riaz Hussain Memon, ratified by the
Sindhi Language Authority on 7 November 2016.

    python sindhi_braille.py book.txt -o book.brf      # Sindhi -> embosser file
    python sindhi_braille.py book.brf --back           # braille -> Sindhi
    python sindhi_braille.py --selftest                # verify round-trip

Pure standard library. No installation, no liblouis, runs on any Python 3.
Output is 40 cells x 25 lines, the international page, confirmed with Riaz.
"""
import sys, argparse, re, unicodedata

# ---------------------------------------------------------------- the code --
LETTER = {
 'ا':['1'],    'ب':['12'],   'ٻ':['26'],    'ڀ':['23'],    'ت':['2345'],
 'ٿ':['1256'], 'ٽ':['246'],  'ٺ':['135'],   'ث':['1456'],  'پ':['1234'],
 'ج':['245'],  'ڄ':['356'],  'ڃ':['35'],    'چ':['14'],    'ڇ':['16'],
 'ح':['156'],  'خ':['1346'], 'د':['145'],   'ڌ':['1236'],  'ڏ':['34'],
 'ڊ':['346'],  'ڍ':['256'],  'ذ':['2346'],  'ر':['1235'],  'ڙ':['12456'],
 'ز':['1356'], 'س':['234'],  'ش':['146'],   'ص':['12346'], 'ض':['1246'],
 'ط':['23456'],'ظ':['123456'],'ع':['12356'],'غ':['126'],   'ف':['124'],
 'ڦ':['235'],  'ق':['12345'],'ڪ':['13'],    'ک':['13','236'],      # ڪ + ھ; see KEHEH
 'گ':['1245'], 'ڳ':['13456'],'ڱ':['2356'],  'ل':['123'],   'م':['134'],
 'ن':['1345'], 'ڻ':['3456'], 'و':['2456'],  'ه':['125'],   'ھ':['236'],
 'ي':['24'],   'ء':['3'],    'آ':['345'],
}
DIGRAPH = {'جھ':['245','236'], 'گھ':['1245','236']}      # ج/گ + aspirate

# NOTE KEHEH.  ک is written as TWO cells, ڪ (13) followed by ھ (236).  This is
# what Riaz Hussain Memon's chart gives and what his printed Grade 2 book uses,
# and both are primary sources.
#
# An earlier revision of this file changed ک to the single cell 4-6, because the
# standard guide's own printed dots appear to show 4-6 where ک was expected
# (pp.31, 41, 42, 44).  That change was wrong and has been reverted: where the
# guide's typesetting and the author's own book disagree, the book decides.
#
# Dots 4-6 are settled.  Riaz Hussain Memon confirmed on 15 August 2026 that they
# are the ڳانڊڙا group prefix - the same thing in Grade 1 as in Grade 2 - and that
# «وڏو اکر» on his chart is his label for it, not a second function and not ک.
# Grade 1 therefore emits nothing for the cell, which is what this file has always
# done, and the guide's printed 4-6 is a fault in its typesetting.

# Composed forms and the two Sindhi signs, spelled as his own book spells them.
# Evidence: لائبريري -> "la/brere" (ئ written as bare ء, carrier dropped);
#           ۾ -> "men";  ۽ -> "aQ/en".  Both appear twice in the standard guide.
NORMALISE = {'ئ':'ء', 'ؤ':'ء', 'أ':'ا', 'إ':'ا', 'ٱ':'ا',
             'ة':'ه', 'ہ':'ه', 'ی':'ي', 'ك':'ڪ'}
SPELLOUT  = {'۾':'مين', '۽':'اَئين'}
# zabar zer pesh shad jazam, plus the tanwins and khari zabar (guide p.33)
DIACRITIC = {'َ':'2', 'ِ':'15', 'ُ':'136', 'ّ':'6', 'ْ':'25',
             'ٍ':'35', 'ٌ':'26', 'ٰ':'4'}    # double zer, double pesh, ڪڙا زبر
DIGIT = {'1':'1','2':'12','3':'14','4':'145','5':'15',
         '6':'124','7':'1245','8':'125','9':'24','0':'245'}
# Two sets of eastern digits reach us, and Sindhi uses the second.
#   U+0660-0669  Arabic-Indic          ٠١٢٣٤٥٦٧٨٩
#   U+06F0-06F9  Extended Arabic-Indic ۰۱۲۳۴۵۶۷۸۹   <- Sindhi, Urdu, Persian
# Only the first was here until a lesson written in ordinary Sindhi arrived and
# the translator raised KeyError on ۱. Both map to the same braille digits.
ARABIC_DIGIT = {'٠':'0','١':'1','٢':'2','٣':'3','٤':'4',
                '٥':'5','٦':'6','٧':'7','٨':'8','٩':'9',
                '۰':'0','۱':'1','۲':'2','۳':'3','۴':'4',
                '۵':'5','۶':'6','۷':'7','۸':'8','۹':'9'}
NUMSIGN, NUMEND = '3456', '6'        # dot 6 closes numeric mode before punctuation
# guide p.35. Semicolon is dots 23, not 25 — 25 is the colon.
PUNCT = {'.':'256', '،':'2', ',':'2', '؟':'236', '?':'236',
         '!':'235', '؛':'23', ';':'23', ':':'25'}
# Digits again, dropped to the lower dots (guide p.52: the "Lower Sign").
# Used for the denominator of a fraction.  Every cell is its upper counterpart
# moved down one row: 1->2, 2->3, 4->5, 5->6.
LOWDIGIT = {'1':'2', '2':'23', '3':'25', '4':'256', '5':'26',
            '6':'235', '7':'2356', '8':'236', '9':'35', '0':'356'}

# The letter sign, اکر جو نشان, dots 5-6 (guide p.42).  It marks a letter that is
# doing the work of a number or a symbol: the ا ب ج د of a numbered exercise, an
# abjad numeral, a Roman numeral, and every arithmetic operator.
LETTERSIGN = '56'

# Arithmetic (guide pp.49-51).  Every operator carries the letter sign.
MATH = {'+':['56','235'], '\u2212':['56','36'], '-':['56','36'],
        '\u00d7':['56','236'], '*':['56','236'], 'x':['56','236'],
        '\u00f7':['56','256'], '/':['56','256'],
        '=':['56','2356'], '%':['25','1234']}
RATIO   = '25'      # a : b        (guide p.51)
DECPT   = '2'       # 1.75         (guide p.50) - dot 2, as in prose the comma
NUMCOMMA= '3'       # 1,000        (guide p.51) - dot 3, because dot 2 is taken
SLASH   = '34'      # the slash of p.50, kept for back-translation only

# English braille, for the Latin-script words the guide wraps in the foreign
# marks (p.46).  A capital is marked by dot 6, exactly as in English braille -
# the guide's own example prints "Thanks" as 6 2345 125 1 1345 13 234.
LATIN = {'a':'1','b':'12','c':'14','d':'145','e':'15','f':'124','g':'1245',
         'h':'125','i':'24','j':'245','k':'13','l':'123','m':'134','n':'1345',
         'o':'135','p':'1234','q':'12345','r':'1235','s':'234','t':'2345',
         'u':'136','v':'1236','w':'2456','x':'1346','y':'13456','z':'1356'}
LATINCAP = '6'

# Roman numerals are the English letters, each after the letter sign (p.48).
ROMAN = {'I':'24', 'V':'1236', 'X':'1346', 'L':'123', 'C':'14',
         'D':'145', 'M':'134'}

# Religious abbreviations, guide p.54.  The full stop is part of the sign and is
# written with no space.  ع does double duty: after a prophet's name it is
# عليه السلام, after a year it is عيسوي (p.55).
ABBREV = [
    ('رحمة الله عليه', ['1235','156','256']),
    ('رحمت الله عليه', ['1235','156','256']),
    ('رضي الله عنه',   ['1235','1246','256']),
    ('ڪرم الله وجه',   ['13','1235','134','256']),
    ('كرم الله وجه',   ['13','1235','134','256']),
    ('عليه السلام',    ['12356','256']),
    ('قبل مسيح',       ['12345','134','256']),
    ('\ufdfa',          ['12346','256']),      # ﷺ
    ('صلعم',           ['12346','256']),
    ('حضرت',           ['156','1246','256']),
    ('تعالى',          ['2345','12356','256']),
    ('تعاليٰ',          ['2345','12356','256']),
    ('تعالي',          ['2345','12356','256']),
    ('هجري',           ['125','256']),
    ('عيسوي',          ['12356','256']),
]

# Marks that are not punctuation (guide pp.39-46, 53).
POETRY   = ['12356','12356']   # twice at the head of a stanza, standing alone
                               # with a space after; once more at the end of each
                               # hemistich, attached to the last word, followed by
                               # the line's punctuation if it has any
TAKHALLUS= '2'                 # dot 2 immediately before the poet's pen-name
BLANK3   = ['3','3','3']       # a fill-in-the-blank gap
FOOTNOTE = ['35','35']         # the star / حاشيه mark
FOREIGN_OPEN  = ['56','236']   # Arabic, Urdu or English inside Sindhi
FOREIGN_CLOSE = ['356','23']
QUOTE = {'\u201c':['236'], '\u201d':['356'], '"':['236'],
         '\u2018':['6','236'], '\u2019':['356','3']}
BRACKET = {'(':['2356'], ')':['2356'],            # prose, guide p.32
           '[':['6','2356'], ']':['2356','3']}
MATHBRACKET = {'(':['126'], ')':['345'],          # arithmetic, guide p.53
               '{':['246'], '}':['135'],
               '[':['126'], ']':['123456']}
COLONDASH = ['25','36','36']   # the :- of a heading (guide p.32)

# Words whose marks are obligatory, and are therefore written whether or not
# anyone typed them.  Ordinary Sindhi text writes الله bare, as four letters, but
# the shadda and the khari zabar belong to the word and a reader expects them.
#
# The order is Riaz Hussain Memon's, given on 15 August 2026: the shadda falls
# BETWEEN the two lams.  That agrees with the Arabic braille convention, which
# writes the shadda before the letter it doubles rather than after it - liblouis
# says so in ar-ar-g1-core.uti, and the Urdu table writes the whole ligature
# U+FDF2 as 1-6-123-4-125, putting the khari zabar after the lam and before the
# ه.  Urdu collapses the two lams into one; this keeps both, as he described.
# Every cell here is the same cell in Sindhi as it is in Urdu.
ALWAYS_MARKED = {
    'الله':  ['1','123','6','123','4','125'],   # ا  ل  shadda  ل  khari zabar  ه
    'اللہ':  ['1','123','6','123','4','125'],
    '\ufdfa'[:0] or 'ﷲ': ['1','123','6','123','4','125'],
}

DOUBLING = ['3','3']                 # word repeated: write once + dot 3 twice
WAW_ATF  = '36'                      # word و word  ->  word + dots 3 6 + word
HYPHEN   = '36'

# ------------------------------------------------------- ASCII braille (BRF) --
BA = " A1B'K2L@CIF/MSP\"E3H9O6R^DJG>NTQ,*5<-U8V.%[$+X!&;:4\\0Z7(_?W]#Y)="
def cell_to_ascii(dots):
    return BA[sum(1 << (int(d)-1) for d in dots)]
def cell_to_unicode(dots):
    """the braille pattern block: U+2800 plus the dot bitmask"""
    return chr(0x2800 + sum(1 << (int(d)-1) for d in dots))
def ascii_to_cell(ch):
    v = BA.index(ch.upper())
    return ''.join(str(i+1) for i in range(6) if v >> i & 1)

# ---------------------------------------------------------------- forward ----
def _digits(tok, i, out):
    """number, decimal point, thousands comma. returns the new index."""
    out.append(NUMSIGN)
    while i < len(tok):
        d = ARABIC_DIGIT.get(tok[i], tok[i])
        if d.isdigit():
            if d not in DIGIT:        # a digit-shaped character we do not know:
                i += 1; continue      # skip it, let unknown_chars report it
            out.append(DIGIT[d]); i += 1; continue
        nxt = ARABIC_DIGIT.get(tok[i+1:i+2], tok[i+1:i+2])
        if tok[i] == '.' and nxt.isdigit():
            out.append(DECPT); i += 1; continue          # guide p.50
        if tok[i] == ',' and nxt.isdigit():
            out.append(NUMCOMMA); i += 1; continue       # guide p.51
        break
    return i

def _fraction(tok):
    """3/4 -> number sign, numerator above, denominator below (guide pp.52-53).
    A numerator of 1 is not written at all - that is the book's own rule."""
    a, _, b = tok.partition('/')
    a = ''.join(ARABIC_DIGIT.get(c, c) for c in a)
    b = ''.join(ARABIC_DIGIT.get(c, c) for c in b)
    if not (a.isdigit() and b.isdigit()): return None
    out = [NUMSIGN]
    if a != '1': out += [DIGIT[d] for d in a]
    out += [LOWDIGIT[d] for d in b]
    return out

def _roman(tok):
    t = tok.rstrip('.')
    if not t or any(c not in ROMAN for c in t): return None
    out = [LETTERSIGN] + [ROMAN[c] for c in t]
    if tok.endswith('.'): out.append(PUNCT['.'])
    return out

def word_to_cells(w, diacritics=False, arithmetic=False, grade2=False):
    if w in ALWAYS_MARKED: return list(ALWAYS_MARKED[w])
    if w and w[-1] in PUNCT and w[:-1] in ALWAYS_MARKED:      # الله.  الله،
        return list(ALWAYS_MARKED[w[:-1]]) + [PUNCT[w[-1]]]
    w = ''.join(SPELLOUT.get(c, c) for c in w)          # expand ۾ ۽ first
    w = ''.join(NORMALISE.get(c, c) for c in w)         # then fold ئ ؤ أ …

    # whole-token forms that are not built letter by letter
    if '/' in w:
        f = _fraction(w)
        if f: return f
    if w in MATH:  return list(MATH[w])
    if w.endswith('%') and len(w) > 1:                  # 50% -> 25 1234 3456 5 0
        body = ''.join(ARABIC_DIGIT.get(c, c) for c in w[:-1])
        if body.isdigit():
            out = list(MATH['%']); _digits(body, 0, out); return out
    r = _roman(w)
    if r: return r
    if w and all(c.lower() in LATIN or c in PUNCT for c in w):
        out = list(FOREIGN_OPEN)                  # guide p.46
        for c in w:
            if c in PUNCT: out.append(PUNCT[c]); continue
            if c.isupper(): out.append(LATINCAP)
            out.append(LATIN[c.lower()])
        return out + list(FOREIGN_CLOSE)
    # an exercise label: a single Sindhi letter used as a number - الف. ب. ج.
    if len(w) == 2 and w[0] in LETTER and w[1] in '.\u06d4':
        return [LETTERSIGN] + LETTER[w[0]] + [PUNCT['.']]

    out, i = [], 0
    while i < len(w):
        # ڳانڊڙا: a group written mid-word or word-final, never word-initial
        if grade2 and GRADE2G and i > 0:
            hit = None
            for g, cells in GRADE2G:
                if w.startswith(g, i): hit = (g, cells); break
            if hit:
                out += list(hit[1]); i += len(hit[0]); continue
        two = w[i:i+2]
        if two in DIGRAPH:
            out += DIGRAPH[two]; i += 2; continue
        c = w[i]
        if c in ARABIC_DIGIT: c = ARABIC_DIGIT[c]
        if c.isdigit():
            i = _digits(w, i, out)
            if i < len(w) and w[i] == ':':        # a ratio, 14:7 (guide p.51)
                out.append(RATIO); i += 1; continue
            if i < len(w) and w[i] in PUNCT:      # 4. would read back as 44
                out.append(NUMEND)
            continue
        if c in LETTER:
            # guide p.31: zer, zabar and pesh are written in the cell AFTER their
            # letter, but shadda is written in the cell BEFORE it.
            if diacritics and w[i+1:i+2] == 'ّ':
                out.append(DIACRITIC['ّ'])
            out += LETTER[c];  i += 1; continue
        if c in DIACRITIC:
            if diacritics and c != 'ّ':
                out.append(DIACRITIC[c])
            i += 1; continue
        if c == '\u2605' or c == '\u2606':        # the footnote star (guide p.44)
            out += FOOTNOTE; i += 1; continue
        if c == '\u2026':                        # an ellipsis: the omission sign
            out += BLANK3; i += 1; continue
        if c == '_' :                            # a fill-in-the-blank run
            while i < len(w) and w[i] == '_': i += 1
            out += BLANK3; continue
        if c in QUOTE:     out += QUOTE[c];    i += 1; continue
        if arithmetic and c in '{}':
            out += MATHBRACKET[c]; i += 1; continue
        if c in BRACKET:
            table = MATHBRACKET if arithmetic else BRACKET
            cs = table[c]
            out += cs if isinstance(cs, list) else [cs]
            i += 1; continue
        if c in PUNCT:     out.append(PUNCT[c]); i += 1; continue
        i += 1                                     # anything else: drop
    return out

def _abbreviate(words):
    """Replace a religious phrase by its abbreviation (guide pp.54-55).
    Returns a list of items, each either a word string or a list of cells."""
    out, i = [], 0
    while i < len(words):
        hit = None
        for phrase, cells in ABBREV:
            n = len(phrase.split())
            if [w.strip('.\u06d4\u060c') for w in words[i:i+n]] == phrase.split():
                hit = (n, cells); break
        if hit:
            out.append(list(hit[1])); i += hit[0]
        else:
            out.append(words[i]); i += 1
    return out

# ------------------------------------------------------------------ grade 2 --
# The contraction list of ڪامل سنڌي بريل درجو II.  A contraction is a series
# prefix followed by one ordinary letter and stands for a whole word.  Loaded
# from official-code/grade2_contractions.csv so the table and this file cannot
# drift apart.
#
# NOTE: the list is certain; the PLACEMENT RULES are not.  Nothing in the source
# says when a contraction may be used inside a word, so every one is applied as a
# whole word only.  That is the conservative choice - it misses contractions a
# human transcriber would make, and never makes a wrong one.  Pending Riaz
# Hussain Memon.
GRADE2 = {}          # single words
GRADE2P = []         # phrases, longest first
GRADE2G = []         # ڳانڊڙا: groups written mid-word or word-final, longest first
def load_grade2(path=None):
    import os, csv
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'official-code', 'grade2_contractions.csv')
    try:
        with open(path, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                w = r['word'].strip()
                cells = r['braille_dots'].split('-')
                if not w: continue
                if ' ' in w:
                    GRADE2P.append((w.split(), cells))
                elif w not in GRADE2:
                    GRADE2[w] = cells
        GRADE2P.sort(key=lambda x: -len(x[0]))
    except OSError:
        pass
    gp = os.path.join(os.path.dirname(os.path.abspath(path)), 'grade2_groups.csv')
    try:
        with open(gp, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                g = r['group'].strip()
                if g: GRADE2G.append((g, r['braille_dots'].split('-')))
        GRADE2G.sort(key=lambda x: -len(x[0]))
    except OSError:
        pass
    _build_grade2_back()
    return len(GRADE2) + len(GRADE2P) + len(GRADE2G)

G2BACK  = {}     # cells -> the word or phrase they stand for
G2GBACK = {}     # cells -> the ڳانڊڙا group they stand for
G2AMBIG = {}     # cells -> every word sharing them, where more than one does

def _build_grade2_back():
    """Reverse the contraction tables.

    Some contractions share their cells with another contraction - that is in
    the book, not in this software.  Where they do, the first entry in the
    book's own order is the reading, and every candidate is recorded in
    G2AMBIG so the collision can be shown rather than hidden."""
    G2BACK.clear(); G2GBACK.clear(); G2AMBIG.clear()
    for w, cells in GRADE2.items():
        k = tuple(cells)
        G2AMBIG.setdefault(k, []).append(w)
        G2BACK.setdefault(k, w)
    for parts, cells in GRADE2P:
        k = tuple(cells)
        G2AMBIG.setdefault(k, []).append(' '.join(parts))
        G2BACK.setdefault(k, ' '.join(parts))
    for g, cells in GRADE2G:
        G2GBACK.setdefault(tuple(cells), g)
    for k in list(G2AMBIG):
        if len(G2AMBIG[k]) < 2: del G2AMBIG[k]

ARITH = set('\u2212\u00d7\u00f7') | {'+', '=', '*', '/'}
def _is_arithmetic(words):
    """a line carrying an arithmetic operator uses the arithmetic brackets"""
    return any(isinstance(w, str) and w in MATH and w not in '-x' for w in words)

def translate(text, diacritics=False, doubling=True, waw=True,
              poetry=False, takhallus=None, grade2=False):
    """Sindhi text -> list of lines, each a list of cell strings ('' = space).

    poetry=True treats every line as one hemistich of a bait and marks it the
    way the guide does (pp.40-41): 12356 twice at the start of the stanza, once
    more attached to the end of each hemistich, a full stop at the stanza's end.
    takhallus is the poet's pen-name; dot 2 is written immediately before it
    wherever it appears (p.41).
    """
    lines = []
    stanza_open = False
    for para in text.split('\n'):
        words = _abbreviate([w for w in para.split(' ') if w])
        arith = _is_arithmetic(words)
        toks, k = [], 0
        while k < len(words):
            w = words[k]
            if isinstance(w, list):               # already-made cells
                toks.append(w); k += 1; continue
            if k+1 < len(words) and isinstance(words[k+1], list):
                pass                              # next item is an abbreviation
            bare = ''.join(ch for ch in w if ch not in PUNCT)
            nxt  = words[k+1] if k+1 < len(words) else None
            nxt2 = words[k+2] if k+2 < len(words) else None
            if isinstance(nxt, list):  nxt  = None
            if isinstance(nxt2, list): nxt2 = None
            # same word twice -> write once, attach dot 3 twice
            if doubling and nxt is not None and bare and w == bare and \
               ''.join(ch for ch in nxt if ch not in PUNCT) == bare:
                cells = word_to_cells(words[k+1], diacritics, arith, grade2)
                toks.append(word_to_cells(bare, diacritics, arith, grade2) + DOUBLING +
                            cells[len(word_to_cells(bare, diacritics, arith, grade2)):])
                k += 2; continue
            # word و word  ->  joined by dots 3 6, no spaces
            if waw and nxt2 is not None and nxt == 'و':
                toks.append(word_to_cells(w, diacritics, arith, grade2) + [WAW_ATF] +
                            word_to_cells(words[k+2], diacritics, arith, grade2))
                k += 3; continue
            if grade2 and GRADE2P:
                hit = None
                for parts, cells in GRADE2P:
                    seg = [x.strip('.\u06d4\u060c\u061f!\u061b:')
                           for x in words[k:k+len(parts)]
                           if not isinstance(x, list)]
                    if seg == parts: hit = (len(parts), cells); break
                if hit:
                    toks.append(list(hit[1])); k += hit[0]; continue
            if grade2 and GRADE2:
                bare2 = w.strip('.\u06d4\u060c\u061f!\u061b:')
                if bare2 in GRADE2:
                    tail = [PUNCT[c] for c in w[len(bare2):] if c in PUNCT]
                    toks.append(list(GRADE2[bare2]) + tail); k += 1; continue
            toks.append(word_to_cells(w, diacritics, arith, grade2)); k += 1
        if takhallus and toks:
            mark = word_to_cells(takhallus, diacritics, arith, grade2)
            for j, t in enumerate(toks):
                if t == mark: toks[j] = [TAKHALLUS] + t     # guide p.41

        if poetry and toks:
            if not stanza_open:
                # The pair opens the stanza and stands on its own, with a space
                # after it.  It used to be joined to the first word; Riaz Hussain
                # Memon corrected that on 15 August 2026 - the marks are not part
                # of the word.
                toks = [list(POETRY)] + toks                # 12356 12356 · word
                stanza_open = True
            toks[-1] = toks[-1] + [POETRY[0]]               # unspaced, each line
        elif poetry:
            stanza_open = False                             # a blank line ends it

        if arith:
            toks = _close_comparison(toks)
        lines.append(_merge_foreign(toks))

    if poetry:                                  # a full stop closes the stanza
        for j, ln in enumerate(lines):
            nxt = lines[j+1] if j+1 < len(lines) else None
            if ln and (nxt is None or not nxt):
                ln[-1] = ln[-1] + [PUNCT['.']]
    return lines

COMPARISON = [MATH['=']]            # the only comparison sign the code has


def _close_comparison(toks):
    """A comparison sign takes a space before it and none after.

    The guide prints this six times out of six, in every worked sum it shows:
    `8 + 9 = 17` is set as three groups, the last of them the equals sign and
    the 17 together, and the same holds for the other four sums and for the two
    bracketed examples.  Riaz Hussain Memon said the same thing on 15 August
    2026, independently and before this was checked against the book.

    This software wrote a space on both sides until August 2026.  The check
    that was supposed to catch it compared cells and recorded the grouping from
    our own output rather than from the page, so it agreed with itself.  The
    grouping is the spacing: `to_brf` writes one space between groups.
    """
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        if any(t == c for c in COMPARISON) and i + 1 < len(toks):
            out.append(list(t) + list(toks[i + 1])); i += 2; continue
        out.append(t); i += 1
    return out


def _merge_foreign(toks):
    """The guide wraps a whole foreign word or sentence in one pair of marks
    (p.46), not each word separately.  Join neighbouring runs into one."""
    fo, fc = list(FOREIGN_OPEN), list(FOREIGN_CLOSE)
    def isf(t): return len(t) > 4 and t[:2] == fo and t[-2:] == fc
    out, k = [], 0
    while k < len(toks):
        if not isf(toks[k]):
            out.append(toks[k]); k += 1; continue
        j = k
        while j + 1 < len(toks) and isf(toks[j+1]): j += 1
        run = toks[k:j+1]
        for m, t in enumerate(run):
            body = t[2:-2]
            out.append((fo if m == 0 else []) + body +
                       (fc if m == len(run)-1 else []))
        k = j + 1
    return out

# ---------------------------------------------------------------- backward ---
# Four cells carry both a letter and a punctuation mark (256 ڍ/full stop,
# 235 ڦ/exclamation, 236 ھ/question, 2 zabar/comma). A trained reader resolves
# these from context; a machine needs help. If a word list is available we try
# the letter reading first and keep it when it yields a known word.
WORDS = set()
def load_words(path=None):
    import os
    path = path or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'sindhi_words.txt')
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or not line.strip(): continue
                WORDS.add(line.split('\t')[0].strip())
    except OSError:
        pass
    return len(WORDS)

CELL2LET = {}
for L, cs in LETTER.items():
    if len(cs) == 1 and cs[0] not in CELL2LET: CELL2LET[cs[0]] = L
CELL2LET['236'] = 'ھ'
LOW2DIG = {v: k for k, v in LOWDIGIT.items()}
LAT2 = {}
for _k, _v in LATIN.items(): LAT2.setdefault(_v, _k)
MATH2   = {tuple(v): k for k, v in MATH.items()
           if k in '+\u2212\u00d7\u00f7=%'}
ROM2    = {}
for _k, _v in ROMAN.items(): ROM2.setdefault(_v, _k)
# The abbreviations of guide p.54 read back to the phrase they stand for.  ع is
# the one that needs context: after a year it is عيسوي, otherwise عليه السلام.
ABB2 = {}
for _ph, _cs in ABBREV: ABB2.setdefault(tuple(_cs), _ph)

# The two Sindhi signs are written out in full - ۾ as مين, ۽ as اَئين - so read
# back letter by letter they came out spelled, not as the sign.  ۽ in particular
# came back as اءين, which is the stray ا Riaz Hussain Memon spotted in a bait on
# 15 August 2026.  Reverse the spelling at the level of the whole word, which is
# exact: only a token whose every cell matches is turned back into the sign.
SIGN2 = {}
for _sg, _sp in SPELLOUT.items(): SIGN2.setdefault(tuple(word_to_cells(_sp)), _sg)

PUNCT_BACK = {'256':'.', '236':'؟', '235':'!', '2':'،', '23':'؛', '25':':'}
DIG2 = {v: k for k, v in DIGIT.items()}
ASPIRATE = {'ج':'جھ', 'گ':'گھ', 'ڪ':'ک'}
MB_OPEN  = {MATHBRACKET['('][0]: '(', MATHBRACKET['{'][0]: '{'}
MB_CLOSE = {MATHBRACKET[')'][0]: ')', MATHBRACKET['}'][0]: '}',
            MATHBRACKET[']'][0]: ']'}
# Word-final 236 is ambiguous: the letter he (aspirate) or the question mark.
# Sindhi forms aspirates by writing he after a consonant, and many common words
# end that way (پڙھ، ڏوھ، اولھ، تھ، بھ). The question mark is far rarer, so the
# letter is the default reading and the mark is taken only after a plain vowel
# sign or when a word list settles it. NOTE: the printed guide does not say how
# a reader distinguishes these; this is our reading and is pending Riaz's
# confirmation. See docs/OPEN-QUESTIONS.md.
VOWEL_ONLY = ''

_TAILMARK = frozenset(PUNCT.values())

def _degrade2(cells):
    """A contracted token -> the Sindhi it stands for, or None.

    Whole token first, because a contraction stands for a whole word; then the
    ڳانڊڙا groups, which are written inside a word and never at its start."""
    if not G2BACK: return None
    body, tail = list(cells), ''
    while body and body[-1] in _TAILMARK and tuple(body) not in G2BACK:
        c = body.pop()
        tail = {v: k for k, v in PUNCT.items()}.get(c, '') + tail
    hit = G2BACK.get(tuple(body))
    if hit is not None: return hit + tail
    if not G2GBACK: return None
    out, i, used = '', 0, False
    while i < len(body):
        g = G2GBACK.get(tuple(body[i:i+2])) if i > 0 else None
        if g: out += g; i += 2; used = True; continue
        letter = CELL2LET.get(body[i])
        if letter is None: return None
        out += letter; i += 1
    return out + tail if used else None

def back(lines, poetry=False, grade2=False):
    """cells -> Sindhi text, applying the shared-cell rules.

    poetry=True strips the verse marks.  It has to be asked for: 12356 is also
    the letter ع and dot 2 is also the zabar and the comma, so in prose those
    cells must be left exactly where they are.

    grade2=True expands the contractions.  It also has to be asked for: every
    contraction is a perfectly ordinary Grade 1 spelling of something else, so
    a Grade 1 book read with grade2=True would come out as nonsense."""
    out = []
    foreign = False          # a foreign run is closed by its own mark, so it
    for toks in lines:       # survives the line break an embosser file puts in
        words = []
        toks = [list(t) for t in toks]
        if poetry and toks:
            if toks[0] == list(POETRY): toks = toks[1:]        # its own token
            elif toks[0][:2] == list(POETRY): toks[0] = toks[0][2:]
            last = toks[-1]
            if last[-1:] == [PUNCT['.']] and last[-2:-1] == [POETRY[0]]:
                toks[-1] = last[:-2] + [PUNCT['.']]
            elif last[-1:] == [POETRY[0]]:
                toks[-1] = last[:-1]
            for j, t in enumerate(toks):
                if t[:1] == [TAKHALLUS] and len(t) > 1:
                    toks[j] = t[1:]                    # the pen-name mark
        for cells in toks:
            # a run of Arabic, Urdu or English is opened by 56-236 and closed by
            # 356-23, once around the whole run (guide p.46)
            if cells[:2] == FOREIGN_OPEN and len(cells) > 2:
                foreign = True; cells = cells[2:]
            closing = cells[-2:] == FOREIGN_CLOSE
            if closing: cells = cells[:-2]
            if foreign:
                t, j = '', 0
                while j < len(cells):
                    if cells[j] == LATINCAP and cells[j+1:j+2] and cells[j+1] in LAT2:
                        t += LAT2[cells[j+1]].upper(); j += 2; continue
                    if cells[j] in LAT2:  t += LAT2[cells[j]]; j += 1; continue
                    if cells[j] in PUNCT.values():
                        t += {v: k for k, v in PUNCT.items()}.get(cells[j], ''); j += 1; continue
                    j += 1
                words.append(t)
                if closing: foreign = False
                continue
            if grade2:
                g2 = _degrade2(cells)
                if g2 is not None:
                    words.append(g2); continue

            s, i = '', 0
            while i < len(cells):
                c = cells[i]
                if (i == 0 and c in MB_OPEN
                        and cells[i+1:i+2] == [NUMSIGN]):
                    s += MB_OPEN[c]; i += 1; continue
                if (i == len(cells)-1 and c in MB_CLOSE
                        and s[-1:].isdigit()):
                    s += MB_CLOSE[c]; i += 1; continue
                if cells[i:i+2] == MATH['%']:
                    s += '%'; i += 2; continue
                if c == LETTERSIGN and tuple(cells[i:i+2]) in MATH2:
                    s += MATH2[tuple(cells[i:i+2])]; i += 2; continue
                if (c == LETTERSIGN and len(cells) == 3 and i == 0
                        and cells[1] in CELL2LET and cells[2] == PUNCT['.']):
                    s += CELL2LET[cells[1]] + '.'; i += 3; continue
                if c == LETTERSIGN and i + 1 < len(cells) and \
                        cells[i+1] in ROM2:
                    i += 1
                    while i < len(cells) and cells[i] in ROM2:
                        s += ROM2[cells[i]]; i += 1
                    continue
                if (c == NUMSIGN and i + 1 < len(cells)
                        and cells[i+1] in LOW2DIG and (i == 0 or s[-1:] in ':%({')):
                    s += '1/'                        # numerator 1 is not written
                    i += 1
                    while i < len(cells) and cells[i] in LOW2DIG:
                        s += LOW2DIG[cells[i]]; i += 1
                    continue
                if (c == NUMSIGN and (i == 0 or s[-1:] in ':%({=')
                        and i + 1 < len(cells) and cells[i+1] in DIG2):
                    i += 1                                  # number sign: digits must follow
                    while i < len(cells) and cells[i] in DIG2:
                        s += DIG2[cells[i]]; i += 1
                        if i < len(cells) and cells[i] == DECPT and \
                                cells[i+1:i+2] and cells[i+1] in DIG2:
                            s += '.'; i += 1
                        elif i < len(cells) and cells[i] == NUMCOMMA and \
                                cells[i+1:i+2] and cells[i+1] in DIG2:
                            s += ','; i += 1
                    # 25 is both the ratio colon and the lower 3; a ratio is
                    # followed by a fresh number sign, a denominator never is.
                    if (i < len(cells) and cells[i] == RATIO
                            and cells[i+1:i+2] == [NUMSIGN]):
                        s += ':'; i += 1; continue
                    if i < len(cells) and cells[i] in LOW2DIG:
                        s += '/'
                        while i < len(cells) and cells[i] in LOW2DIG:
                            s += LOW2DIG[cells[i]]; i += 1
                        continue
                    if i < len(cells) and cells[i] == NUMEND: i += 1
                    continue
                if c == '236' and s and s[-1] in ASPIRATE:  # aspirate digraph
                    s = s[:-1] + ASPIRATE[s[-1]]; i += 1; continue
                last = (i == len(cells)-1)
                if last:                                    # word-final: letter or punctuation?
                    mark = {'256':'.', '236':'؟', '235':'!', '2':'،',
                            '23':'؛', '25':':'}.get(c)
                    letter = CELL2LET.get(c, '')
                    if not mark:
                        s += letter
                    elif not s:
                        s += letter or mark                 # a mark cannot stand alone
                    elif WORDS and letter and (s + letter) in WORDS:
                        s += letter                         # letter reading gives a real word
                    elif c == '236' and len(s) == 1:
                        s += letter                         # ڙھ, لھ — a letter pair, not a question
                    elif WORDS and s in WORDS:
                        s += mark                           # word ends here; this is the mark
                    elif c == '236':
                        s += letter                         # unknown: he is far commoner
                    else:
                        s += mark
                    i += 1; continue
                if cells[i:i+2] == DOUBLING:                # repeat the word
                    s = s + ' ' + s; i += 2; continue
                if c == WAW_ATF: s += ' و '; i += 1; continue
                s += CELL2LET.get(c, ''); i += 1
            m = re.match(r'^%([0-9][0-9.,]*)$', s)
            if m: s = m.group(1) + '%'          # the guide prints % first (p.51)
            words.append(s)
        for j, cs in enumerate(toks):
            key = tuple(cs)
            # The sign wins unless the spelled-out reading is a real word in
            # its own right - the cells of ۽ followed by 236 also read as a word
            # ending in ھ, and only the word list can tell those apart.
            if key in SIGN2 and not (WORDS and words[j] in WORDS):
                words[j] = SIGN2[key]; continue
            if (len(cs) > 1 and tuple(cs[:-1]) in SIGN2 and cs[-1] in PUNCT_BACK
                    and not (WORDS and words[j] in WORDS)):
                words[j] = SIGN2[tuple(cs[:-1])] + PUNCT_BACK[cs[-1]]; continue
            if key in ABB2:
                if key == ('12356', '256'):
                    prev = words[j-1] if j else ''
                    words[j] = 'عيسوي' if prev[-1:].isdigit() else 'عليه السلام'
                else:
                    words[j] = ABB2[key]
        out.append(' '.join(words))
    return '\n'.join(out)

# ------------------------------------------------------------- page layout ---
def to_brf(lines, width=40, height=25):
    pages, cur = [], []
    for toks in lines:
        row = ''
        for cells in toks:
            piece = ''.join(cell_to_ascii(c) for c in cells)
            while len(piece) > width:                       # break with a hyphen
                cut = width - len(row) - (1 if row else 0) - 1
                if cut > 2:
                    row = (row + ' ' if row else '') + piece[:cut] + cell_to_ascii(HYPHEN)
                    cur.append(row); row = ''; piece = piece[cut:]
                else:
                    if row: cur.append(row); row = ''
                    cur.append(piece[:width-1] + cell_to_ascii(HYPHEN)); piece = piece[width-1:]
            if not row: row = piece
            elif len(row) + 1 + len(piece) <= width: row += ' ' + piece
            else: cur.append(row); row = piece
        cur.append(row)
        while len(cur) >= height:
            pages.append(cur[:height]); cur = cur[height:]
    if cur: pages.append(cur)
    return '\f'.join('\r\n'.join(p) for p in pages) + '\r\n\f'

def from_brf(brf):
    lines = []
    for raw in brf.replace('\f', '\n').replace('\r\n', '\n').split('\n'):
        if not raw.strip(): continue
        lines.append([[ascii_to_cell(ch) for ch in w] for w in raw.split(' ') if w])
    return lines

# ------------------------------------------------------------------- tests ---
TESTS = [
 'سنڌي ٻولي هڪ شاهوڪار ٻولي آهي.',
 'واه واه گھوڙو ڏاڍو ڀلو آهي.',
 'ڪبوتر جھرڪي ڳيرو وغيره.',
 'سنڌ جي عظيم اڳواڻ ذوالفقار ڀٽي جو تعلق لاڙڪاڻي ضلعي سان آهي.',
 'اسان جي صوبي جو نالو ڇا آهي؟',
 'لاڙڪاڻي جي وڏي کان وڏي پبلڪ لائبريري آهي.',
 'هن ڊڄندي ڊڄندي ورندي ڏني.',
 'ٿورو ٿورو پاڻي.',
 'رات و ڏينهن محنت.',
 'ڪتاب جو قيمت 250 روپيا آهي.',
 'صفحو 4.',
 'اڄ 7 نومبر 2016 آهي.',
 'ڇا اهو صحيح آهي؟ ها!',
 'لاڙڪاڻي جي پبلڪ لائبريري.',
 'اسين سنڌ ۾ رهون ٿا.',
 'رات ۽ ڏينهن.',
]
def normalised(t):
    """The spelling the braille can actually represent. Applying this to the
    source is what a fair round-trip test compares against — the differences
    are losses in the CODE, not in this program."""
    t = ''.join(SPELLOUT.get(c, c) for c in t)
    t = ''.join(NORMALISE.get(c, c) for c in t)
    return ' '.join(t.replace('َ','').split())

def selftest(verbose=True):
    n = load_words()
    if n: print(f'  (word list loaded: {n} words)')
    exact = equiv = bad = 0
    for t in TESTS:
        got = back(from_brf(to_brf(translate(t))))
        flat, want = ' '.join(got.split()), ' '.join(t.split())
        if flat == want:                       tag, exact = 'exact', exact+1
        elif ' '.join(got.replace('َ','').split()) == normalised(t):
                                               tag, equiv = 'equiv', equiv+1
        else:                                  tag, bad   = 'FAIL ', bad+1
        if verbose:
            print(f'  {tag}  {t}')
            if tag=='FAIL ': print('         got: ' + got)
    print(f'\n  {exact} exact   {equiv} equivalent spelling   {bad} wrong'
          f'   ({exact+equiv}/{exact+equiv+bad} faithful)')
    if equiv: print('  "equivalent" = the braille cannot represent that spelling; see LOSSY below.')
    return bad == 0

LOSSY = """Characters the code cannot round-trip, with the evidence:
  ئ ؤ  -> ء     his book writes لائبريري as la/brere (carrier dropped)
  أ إ  -> ا
  ۾     -> مين   his book writes ۾ as men
  ۽     -> ائين  his book writes ۽ as aQ/en
  ة ہ  -> ه   |  ی -> ي   |  ك -> ڪ      (orthographic normalisation)
These are properties of the braille code, not of this program. Text -> braille
is exact; braille -> text returns the normalised spelling."""

def main():
    load_words()
    ap = argparse.ArgumentParser(description='Sindhi <-> braille (Riaz Hussain Memon code, SLA 2016)')
    ap.add_argument('infile', nargs='?')
    ap.add_argument('-o', '--out')
    ap.add_argument('--back', action='store_true', help='braille file -> Sindhi text')
    ap.add_argument('--grade2', action='store_true',
                    help='use the Grade 2 contractions, both directions')
    ap.add_argument('--diacritics', action='store_true', help='write zer/zabar/pesh (beginner level)')
    ap.add_argument('--no-doubling', action='store_true')
    ap.add_argument('--no-waw', action='store_true')
    ap.add_argument('--poetry', action='store_true',
                    help='every line is one hemistich of a bait (guide pp.40-41)')
    ap.add_argument('--takhallus', metavar='NAME',
                    help="the poet's pen-name; dot 2 is written before it (p.41)")
    ap.add_argument('--width', type=int, default=40)
    ap.add_argument('--height', type=int, default=25)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.grade2:
        n = load_grade2()
        print('grade 2: %d contractions loaded' % n, file=sys.stderr)
    if a.selftest: sys.exit(0 if selftest() else 1)
    if not a.infile: ap.error('give a file, or --selftest')
    raw = open(a.infile, encoding='utf-8-sig').read()
    if a.back:
        res = back(from_brf(raw), poetry=a.poetry, grade2=a.grade2)
    else:
        text = unicodedata.normalize('NFC', raw)
        res = to_brf(translate(text, a.diacritics, not a.no_doubling, not a.no_waw,
                               a.poetry, a.takhallus, a.grade2),
                     a.width, a.height)
    if a.out:
        open(a.out, 'w', encoding='utf-8' if a.back else 'ascii', newline='').write(res)
        print(f'wrote {a.out}')
    else:
        sys.stdout.write(res)

if __name__ == '__main__':
    main()
