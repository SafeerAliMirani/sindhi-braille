# -*- coding: utf-8 -*-
"""
Sheet 4 — the three things that are still decisions, set so they can be read.

    python make_decision_sheet.py

Writes test-sheets/print-4-decisions.brf and DECISION-KEY.md.

Nothing on this sheet is asserted. Lines 1 to 3 are the same sum written three
different ways, because the standard guide and Riaz Hussain Memon do not agree
about the spacing and the modern international code agrees with neither exactly.
He reads the three and says which one is right; only then does the software
change. Lines 5 and 6 are الله written with its obligatory marks, which is new.
Lines 8 to 10 are a bait with the opening pair standing on its own, which is his
own correction and needs confirming by touch.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

W = 28
NUM, EQ = sb.NUMSIGN, sb.MATH['=']
PLUS = sb.MATH['+']
D = sb.DIGIT


def label(letter):
    """الف.  ب.  ج. — the guide's own way of numbering an exercise (p.44)."""
    return [sb.LETTERSIGN] + sb.LETTER[letter] + [sb.PUNCT['.']]


def num(s):
    return [NUM] + [D[c] for c in s]


# The arithmetic question, as it now stands -------------------------------
#
# The equals sign is settled.  The guide closes it up to the number after it in
# every one of the six it prints, and Riaz Hussain Memon said the same on
# 15 August 2026.  Both engines now do that and it is not on this sheet.
#
# What is left is the operation signs, where the guide disagrees with itself:
# it closes `+` up to the 9 and spaces `-`, `x` and division.  Two sums, each
# written both ways, so he can hear the difference without being told which is
# which.
MINUS = sb.MATH['-']

CLOSED_PLUS  = [num('8'),  list(PLUS)  + num('9'),  list(EQ) + num('17')]
SPACED_PLUS  = [num('8'),  list(PLUS),  num('9'),   list(EQ) + num('17')]
CLOSED_MINUS = [num('20'), list(MINUS) + num('13'), list(EQ) + num('7')]
SPACED_MINUS = [num('20'), list(MINUS), num('13'),  list(EQ) + num('7')]

lines = [
    [label('ا')] + CLOSED_PLUS,
    [label('ب')] + SPACED_PLUS,
    [],
    [label('ج')] + CLOSED_MINUS,
    [label('د')] + SPACED_MINUS,
    [],
    sb.translate('الله')[0],
    sb.translate('بسم الله الرحمن الرحيم')[0],
    [],
]
lines += sb.translate('سنڌ ڀٽائي جي ڀونءِ\nهتي امن ۽ محبت آهي\nلطيف چوي ٿو سچ',
                      poetry=True, takhallus='لطيف')

brf = sb.to_brf(lines, width=W, height=25)
out = os.path.join(ROOT, 'test-sheets', 'print-4-decisions.brf')
io.open(out, 'w', encoding='ascii', newline='').write(brf)

widest = max(len(r) for r in brf.replace('\f', '').split('\r\n'))
print('print-4-decisions.brf  %d lines, widest %d cells' %
      (len([r for r in brf.replace('\f', '').split('\r\n') if r]), widest))

KEY = """# Sheet 4 — the decision sheet

**Read these to him without saying which is which.**

## Lines 1 to 4 — one question, asked twice

The equals sign is no longer in question. The guide closes it up to the number
that follows in every one of the six it prints, and he said the same on
15 August 2026. Both engines do that now.

What is left is the **operation signs**, where the guide disagrees with itself.
It prints the addition with the plus closed up to the 9, and the subtraction,
multiplication and division with the sign spaced on both sides. He says they all
close up. The software currently spaces them, following the three.

| line | label | what it prints | who writes it this way |
|---|---|---|---|
| 1 | الف. | `8 +9 =17` | the guide's own addition example, and him |
| 2 | ب. | `8 + 9 =17` | the guide's other three sums, and the software today |
| 4 | ج. | `20 −13 =7` | him |
| 5 | د. | `20 − 13 =7` | the guide's own subtraction example, and the software today |

Ask which of 1 and 2 reads correctly, then which of 4 and 5, **before** telling
him that the book prints 1 and 5. If he picks 1 and 4, the software changes and
the guide is inconsistent in one more place than we have recorded. If he picks
2 and 5, the software is already right and his August remark applied only to the
equals sign, which is now implemented.

## Lines 7 and 8 — الله with its marks

- line 7: **الله** alone
- line 8: **بسم الله الرحمن الرحيم**

Written as ا ل shadd ل khari-zabar ه — the shadda between the two lams, which is
his own instruction and agrees with the Arabic braille convention of writing the
shadda before the letter it doubles. Ask whether that is complete and in the
right order.

## Lines 10 to 12 — a bait, with the opening pair standing alone

- سنڌ ڀٽائي جي ڀونءِ
- هتي امن ۽ محبت آهي
- لطيف چوي ٿو سچ

The two 12356 stand as their own cell-group with a space after them, which is
his correction. The mark at the end of each hemistich is still attached to the
last word. Ask whether the end of the line is right as well as the start.

Line 11 also carries **۽**, which used to be read back as اءين. Ask whether the
cells for ۽ read cleanly here.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
io.open(os.path.join(ROOT, 'test-sheets', 'DECISION-KEY.md'), 'w',
        encoding='utf-8', newline='\n').write(KEY)
print('DECISION-KEY.md written')
