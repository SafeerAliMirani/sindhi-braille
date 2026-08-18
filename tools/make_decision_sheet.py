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


# 8 + 9 = 17, three ways --------------------------------------------------
GUIDE = [num('8'), list(PLUS), num('9'), list(EQ), num('17')]
# Closed up, but each number still carries its own number sign - that is this
# code's convention, and the guide re-issues it after every operator.
UEB   = [num('8') + list(PLUS) + num('9'), list(EQ), num('17')]
HIS   = [num('8'), list(PLUS) + num('9'), list(EQ) + num('17')]

# الله, three ways.  His own chart says diacritics always follow their letter;
# he said on 15 August that the shadda in الله falls between the two lams; and
# Urdu braille writes the shadda before the letter it doubles, with one lam.
# Those three are not the same spelling, so all three go on the paper.
A, L, H = sb.LETTER['ا'][0], sb.LETTER['ل'][0], sb.LETTER['ه'][0]
SHADD, KHARI = sb.DIACRITIC['ّ'], sb.DIACRITIC['ٰ']
ALLAH_BETWEEN = [A, L, SHADD, L, KHARI, H]     # what the software writes today
ALLAH_URDU    = [A, SHADD, L, KHARI, H]        # the Urdu braille ligature
ALLAH_FOLLOWS = [A, L, L, SHADD, KHARI, H]     # diacritics always follow

lines = [
    [label('ا')] + GUIDE,
    [label('ب')] + UEB,
    [label('ج')] + HIS,
    [],
    [label('د')] + [ALLAH_BETWEEN],
    [label('ه')] + [ALLAH_URDU],
    [label('و')] + [ALLAH_FOLLOWS],
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

**Read these to him without saying which is which.** Nothing here is settled, and
three of the lines contradict each other on purpose.

## Lines 1 to 3 — the same sum, three ways

The print is `8 + 9 = 17` every time. Only the spacing differs.

| line | label | spacing | where it comes from |
|---|---|---|---|
| 1 | الف. | space on both sides of + and of = | **the standard guide**, pp.49 and 50, five worked examples |
| 2 | ب. | + closed up, = spaced | **UEB**, the current international code: operation signs unspaced, comparison signs spaced |
| 3 | ج. | space before + and before =, none after | **what he said on 15 August 2026** |

Ask which reads correctly, and ask it before telling him that line 1 is the
book's. If he picks 3, the guide is wrong in a third place and that belongs in
the paper. If he picks 2, the software follows UEB. If he picks 1, nothing
changes and the earlier remark was about something else.

## Lines 5, 6 and 7 — الله, three ways

All three are the same word. Only where the shadda sits differs, and three
sources say three different things.

| line | label | spelling | where it comes from |
|---|---|---|---|
| 5 | د. | ا ل **shadd** ل khari-zabar ه | **what he said on 15 August 2026** — the shadda between the two lams. This is what the software writes today. |
| 6 | ه. | ا **shadd** ل khari-zabar ه | **Urdu braille**, which gives the whole ligature as 1-6-123-4-125: the shadda before the lam, and one lam, because the shadda is the doubling |
| 7 | و. | ا ل ل **shadd** khari-zabar ه | **his own chart**, which records that a diacritic is always written after the letter it belongs to |

Read all three and ask which is الله. This one matters more than it looks: if
the answer is line 7, then the shadda follows its letter everywhere and nothing
special is needed; if it is line 5 or 6, then الله is an exception to his own
rule and the exception has to be written down.

Also worth asking while the paper is in his hands: is the khari zabar in the
right place in whichever he picks?

## Lines 8 to 10 — a bait, with the opening pair standing alone

- سنڌ ڀٽائي جي ڀونءِ
- هتي امن ۽ محبت آهي
- لطيف چوي ٿو سچ

The two 12356 now stand as their own cell-group with a space after them, which is
his correction. The mark at the end of each hemistich is still attached to the
last word. Ask whether the end of the line is right as well as the start.

Line 9 also carries **۽**, which used to be read back as اءين. Ask him whether
the cells for ۽ read cleanly here.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
"""
io.open(os.path.join(ROOT, 'test-sheets', 'DECISION-KEY.md'), 'w',
        encoding='utf-8', newline='\n').write(KEY)
print('DECISION-KEY.md written')
