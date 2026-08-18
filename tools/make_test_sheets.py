# -*- coding: utf-8 -*-
"""
Build the print sheets — the pages that get embossed and read by touch.

    python make_test_sheets.py            # writes ../test-sheets/*.brf

Sheet 1 is Grade 1, sheet 2 is Grade 2, sheet 3 is verse, arithmetic and the
other languages.  All three are 28 cells wide so they fit A4.

Every line tests one thing; the line-by-line answer key is ANSWER-KEY.md, and
the two must be changed together.

Letter lists are translated with the repeated-word and واؤ عطف rules switched
off: those rules are right for prose and wrong for a list of bare letters.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindhi_braille as sb

W = 28

# (text, plain)  plain=True -> a bare list of letters, not prose
SHEET1 = [
    ('ا ب ٻ ڀ ت ٿ ٽ ٺ ث پ ج ڄ ڃ چ ڇ ح خ د ڌ ڏ ڊ ڍ ذ ر ڙ ز', True),
    ('س ش ص ض ط ظ ع غ ف ڦ ق ڪ ک گ ڳ ڱ ل م ن ڻ و ه ھ ي ء آ', True),
    ('0 1 2 3 4 5 6 7 8 9', True),
    ('دم. دم، دم؟ دم! دم؛ دم:', False),
    ('سنڌي ٻولي هڪ شاهوڪار ٻولي آهي.', False),
    ('اسان جي صوبي جو نالو ڇا آهي؟', False),
    ('جھ گھ ڙھ لھ مھ نھ ڻھ', True),
    ('پڙھ تھ بھ ڏوھ اولھ ڳالھ', True),
    ('ک کير کٽ لکو دوکو', True),
    ('ٿورو ٿورو پاڻي.', False),
    ('ڪتاب جو قيمت 250 روپيا آهي.', False),
    ('3/7 1/2 13/44', False),
    ('8 + 9 = 17', False),
    ('VIII IX X', False),
    ('ا. ب. ج. د.', False),
    ('حضرت آدم عليه السلام', False),
    ('پاڪستان 14 آگسٽ 1947 عيسوي', False),
]

SHEET2 = [
    'اسين به ٻه ڀلو توهان ٿو',
    'پر جو چيو ڇو دوست',
    'آهي اوهان بيهن ٻاهر ڀلائي',
    'اڳتي بابت پاڻ',
    'شروع جنهن صورت خراب اڳواڻ',
    'تيئن ته ڇاڪاڻ ته مطلب ته',
    'البته اتفاق امڪان بعد',
    'آباد آزارا',
    'اسين ٿو وڃون. البته توهان ڀلو آهي.',
]

# Sheet 3 — the three areas that had never been checked.
SHEET3_MATHS = [
    '8 + 9 = 17',
    '20 − 13 = 7',
    '12 × 8 = 96',
    '91 ÷ 7 = 13',
    '3/7 1/2 13/44',
    '1.75 1,000 2:3',
    '50% 1%',
    '(8 + 9) = 17',
    '{12 + 3} = 15',
    'VIII IX X',
]
SHEET3_FOREIGN = [
    'هي Thanks لفظ آهي.',
    'اسڪول جو نالو City School آهي.',
    'مان Computer Science پڙهان ٿو.',
    'هن ۾ اردو لفظ کتاب آهي.',
]
SHEET3_POEM = ['سنڌ ڀٽائي جي ڀونءِ',
               'هتي امن ۽ محبت آهي',
               'لطيف چوي ٿو سچ']
TAKHALLUS = 'لطيف'


def wrap(cellrows):
    """cells -> ASCII braille rows of at most W characters"""
    rows = []
    for toks in cellrows:
        row = ''
        for cs in toks:
            piece = ''.join(sb.cell_to_ascii(c) for c in cs)
            if not row:                          row = piece
            elif len(row) + 1 + len(piece) <= W: row += ' ' + piece
            else:                                rows.append(row); row = piece
        if row: rows.append(row)
    return rows


def write(path, rows):
    io.open(path, 'w', encoding='ascii', newline='').write(
        '\r\n'.join(rows) + '\r\n\f')
    print('%-34s %2d lines' % (os.path.basename(path), len(rows)))


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', 'test-sheets')
    sb.load_words()

    rows = []
    for text, plain in SHEET1:
        kw = dict(doubling=False, waw=False) if plain else {}
        rows += wrap(sb.translate(text, **kw))
    write(os.path.join(out, 'print-1-grade1.brf'), rows)

    rows = []
    for text in SHEET3_MATHS + SHEET3_FOREIGN:
        rows += wrap(sb.translate(text))
    rows += wrap(sb.translate('\n'.join(SHEET3_POEM),
                              poetry=True, takhallus=TAKHALLUS))
    write(os.path.join(out, 'print-3-poetry-maths-foreign.brf'), rows)

    sb.load_grade2()
    rows = []
    for text in SHEET2:
        rows += wrap(sb.translate(text, grade2=True))
    write(os.path.join(out, 'print-2-grade2.brf'), rows)


if __name__ == '__main__':
    main()
