# Open questions — what is not settled yet

**Updated 13 August 2026.** Most of the earlier list has been closed by reading
the printed guide properly rather than by asking anyone. What remains is short.

---

## A. Closed — answered by the author

**A1 — does dots 4-6 carry anything in Grade 1? — CLOSED, 15 August 2026.**

**Answered by Riaz Hussain Memon on 15 August 2026.** Dots 4-6 are the ڳانڊڙا
group prefix, and they are the same thing in Grade 1 as in Grade 2. The gloss
«وڏو اکر» on his Grade 1 chart is his own label for that prefix. It is not a
second function, and it is not ک.

**ک is two cells: ڪ (1-3) then ھ (2-3-6)**, confirmed by the author directly, in
addition to his chart and his printed Grade 2 book. This is what the translator,
the liblouis tables and the website have always written.

It follows that the dots printed as 4-6 in the standard guide on pages 31, 41, 42
and 44, where ک was expected, are a fault in that book's typesetting and not a
rule. The five guide-derived ک examples stay out of the evidence suite for that
reason, and nothing in the software changes.

**How it was asked.** He was given the question in two halves and in this order:
first the cell, without being told what we had implemented, then the letter. The
touch test on sheet 1 line 13 (ک کير کٽ لکو دوکو, written ڪ then ھ) stands as the
independent confirmation.

---

**A2 — the ک in a borrowed Urdu word. — CLOSED, 15 August 2026.**

The letter ک is a single character to a computer: Sindhi ک and Urdu ک share one
Unicode codepoint, U+06A9. In Sindhi that letter is two cells, 1-3 then 2-3-6.
In Urdu it is one cell, 1-3 — which in Sindhi is ڪ. So on paper the same written
letter has two possible values, and nothing in the text says which language the
word came from. Reading sheet 3 line 16, «هن ۾ اردو لفظ کتاب آهي», he noticed
this himself.

**His ruling: it is not a problem, and nothing should change.** Sindhi already
uses a great many letters it shares with Urdu, and a Sindhi braille reader reads
that letter the same way whichever language the word came from. The code is
therefore one script with one value per letter, and the software does not branch
on the language of a word.

That is worth recording as a decision and not only as an answer, because the
alternative — inferring a word's language in order to choose a cell — is
something software cannot do reliably, and he has ruled that it does not need
to try.

---

## A3 — the spacing of arithmetic. OPEN, and on sheet 4.

He said on 15 August 2026 that `8 + 9 = 17` should be written `8 +9 =17` — a
space before each sign and none after — and that the international rules have
changed and we should follow them. **We checked what they now say, and they
support him in substance but not in detail.**

**UEB, the current international code** (ICEB; *Guidelines for Technical
Material*, section 1.1.2) draws a line this code does not draw:

- **operation signs — + − × ÷ — are unspaced on both sides**
- **comparison signs — = ≠ < > — are spaced on both sides**

Its own worked example is `8 + 9 = 17` embossed as **`8+9 = 17`**. So the modern
rule is neither the guide's (spaces everywhere) nor `8 +9 =17` as it reached us.
The distinction it makes — an operation binds its two numbers into one expression,
a comparison separates two expressions — is a real one, and it may be exactly what
he meant.

**The guide is on the other side.** Pages 49 and 50 print five worked sums, every
one with a space on both sides of every sign, and those five are part of the 69
printed examples this software reproduces cell for cell. Nothing has been changed
in the software.

**Sheet 4 settles it by touch.** Lines 1, 2 and 3 are the same sum in the three
spacings, labelled الف. ب. ج., in that order. He reads them without being told
which is which and says which is right. See `test-sheets/DECISION-KEY.md`.

**His remark about the full stop is true of UEB and not of Sindhi.** In UEB the
decimal point and the full stop are the same cell, so a full stop after a number
reads as a decimal point. In this code they are different: the guide gives the
decimal point as **dot 2** (p.50) and the full stop as **2-5-6**. The clash he is
warning about does not exist here, and moving the decimal point to 2-5-6 to match
UEB would create it. Worth telling him.

---

## A4 — where the shadda sits. OPEN, and on sheet 4.

Three sources say three different things about الله, and they cannot all be
right.

| spelling | source |
|---|---|
| ا ل **shadd** ل khari-zabar ه | what he said on 15 August 2026: the shadda between the two lams. This is what the software writes today. |
| ا **shadd** ل khari-zabar ه | Urdu braille, which gives the whole ligature U+FDFA as **1-6-123-4-125** — shadda before the lam, one lam, because the shadda *is* the doubling |
| ا ل ل **shadd** khari-zabar ه | his own chart, recorded in `official-code/sindhi_braille_FINAL.csv`: *"a letter written first and then zer, zabar or pesh"* — a diacritic always follows the letter it belongs to |

This is worth more than one word. If the third is right, the shadda behaves like
every other diacritic and nothing special is needed anywhere. If the first or
second is right, الله is an exception to his own stated rule, and the exception
has to be written into the specification.

Sheet 4 lines 5, 6 and 7 carry all three, labelled د. ه. و. Read them cold.

---

## B. Places where the guide contradicts itself

Neither is ours to fix. Both are decisions for the Sindhi Language Authority.

**B1 — fractions.** Pages 52 and 53 state the rule twice and show nine examples:
numerator in the upper digits, denominator in the lower digits, no bar, and the
numerator dropped entirely when it is 1. Page 50 instead writes fractions with a
slash cell (dots 34) between two upper digits, and states no rule. We implement
the pp.52–53 rule.

**B2 — brackets.** Page 32 gives the round bracket as 2356 for both open and
close, the square bracket as 6-2356 and 2356-3. Page 53 gives an entirely
different set for arithmetic: ( = 126, ) = 345, { = 246, } = 135, ] = 123456 —
and prints the open square bracket with the same cell as the open round bracket,
which must be a slip. Prose and arithmetic may legitimately differ; the slip is
separate.

**B3 — one cell, two signs.** Page 31 prints dot 6 for both شد and بہ زبرون.

**B5 — × and the foreign mark are the same two cells.** Multiplication is
dots 5-6 2-3-6 (p.49) and a foreign word is opened by dots 5-6 2-3-6 (p.46).
The translator separates them by the space — the foreign mark is written
attached to its word, so a bare two-cell 5-6 2-3-6 between two numbers is
multiplication. That rule works on everything we have, but it is ours, not the
guide's. **Ask Riaz how a reader tells them apart.**

**B4 — a misprint.** Page 54 prints the abbreviation of تعاليٰ with ٽ (246) where
ت (2345) is meant. Page 55 of the same book proves both values.

---

## C. Evidence we still do not have

**C1 — the Class 6 textbook as a `.brf` file** from the DEPD Braille Press
(in Duxbury: File → Save As → Formatted braille). This is the single most
valuable thing still missing. Everything we have built, we built ourselves from
the same documents; our two implementations agreeing proves consistency, not
correctness. A large body of braille produced by somebody else is what breaks
that circle.

**C2 — pages 1–26 and 56 onward of the guide.** Pages 1–26 hold the guide's own
alphabet table; 56 onward we have not seen at all and do not know what is on
them.

**C3 — a second reader.** Every confirmation in this project has come from one
person. Before publication at least one other Sindhi braille reader, ideally a
teacher at a different school, should read our test sheets cold and tell us what
they say.

---

## D. Not built yet

- **Placement rules for the Grade 2 series.** The contractions themselves are
  implemented — 237 of them and the six ڳانڊڙا groups, in `sd-pk-g2.ctb`, in the
  reference translator and on the website, both directions — but the material
  nowhere states *when* a contraction may be used. See `docs/GRADE-2.md`.
- **Ordinal endings.** The guide writes ordinals as plain numbers and leaves the
  ending to the reader, so there is nothing to build; noted so it is not
  mistaken for an omission.

---

## D2. Five contractions the book gives the same cells to

Not ours to fix, and not a defect in the software — the book assigns one pair of
cells to two different words in five places:

| cells | and it could be |
|---|---|
| 1245 | گرمي · گرم |
| 3456-12346 | صحتمند · صحتمندي |
| 245-134 | جملو · جملي |
| 134-1235-2345 | مرتبو · مرتبا |
| 245-23456 | جهڙي طرح · جنهن طرف |

Writing is unaffected. Reading takes the first of each pair, which is the book's
own order, and `sindhi_braille.G2AMBIG` holds every candidate so the collision
can be shown rather than hidden. Whether a reader resolves these from the
sentence, or whether one of the five is a misprint, is worth asking.

---

## The test for "finished"

One complete pass over everything — guide, both books, both implementations, the
liblouis table — that finds **no new errors**. The last pass found the ک
correction, so the count is still running. Until a pass comes back clean, the
work is not done.

`python tools/check_all.py` runs every check at once. Everything on that list
passing is the floor, not the finish. On **15 August 2026** the floor was finally
left behind: Riaz Hussain Memon read an embossed page of ordinary Sindhi news
prose by touch, complete and without an error — see `docs/READING-2026-08-15.md`.
That was one reader and one page of prose, carrying no verse, no arithmetic and
no contractions, which is what sheets 1 to 4 are for.
