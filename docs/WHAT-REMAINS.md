# What is still open

**Updated 18 August 2026.** One list, ordered by what blocks what. Everything
here is either a decision only Riaz Hussain Memon or the Sindhi Language
Authority can make, or a check that has not been run yet. Nothing on this list is
a bug in the software.

---

## 1. Four things waiting on one sitting with him

All four are on **sheet 4**, `test-sheets/print-4-decisions.brf`, one A4 page.
Read them cold and the four close together. `DECISION-KEY.md` says what each line
is and in what order to ask.

### 1.1 The spacing of arithmetic — lines 1, 2, 3

Three spellings of `8 + 9 = 17`, and three sources disagree.

| | spacing | source |
|---|---|---|
| الف. | space both sides of + and = | the standard guide, pp.49–50, five worked sums |
| ب. | + closed up, = spaced | UEB, the current international code |
| ج. | space before each sign, none after | what he said on 15 August 2026 |

He asked us to follow the modern international rule. UEB's rule is that
**operation signs are unspaced and comparison signs are spaced**, which is line
ب. and matches neither the guide nor what was reported back to us. If he picks
ب. or ج. the guide is wrong in a third place, and that belongs in the paper.

Related and worth telling him: in UEB the decimal point and the full stop are the
same cell, which is why a full stop cannot follow a number there. In this code
they differ — decimal point dot 2 (p.50), full stop 2-5-6 — so that clash does
not exist in Sindhi, and copying UEB wholesale would create it.

### 1.2 Where the shadda sits in الله — lines 5, 6, 7

Three sources, three spellings, and they cannot all be right.

| | spelling | source |
|---|---|---|
| د. | ا ل **shadd** ل khari-zabar ه | what he said on 15 August 2026 — between the two lams. What the software writes today. |
| ه. | ا **shadd** ل khari-zabar ه | Urdu braille, which gives the whole ligature as 1-6-123-4-125 |
| و. | ا ل ل **shadd** khari-zabar ه | his own chart: *a diacritic always follows the letter it belongs to* |

This is bigger than one word. If و. is right, the shadda behaves like every other
diacritic and no special case is needed anywhere. If د. or ه. is right, الله is
an exception to his own rule and the exception has to be written into the
specification. Ask about the khari zabar's position at the same time.

### 1.3 The end of a line of verse — lines 9, 10, 11

The opening pair now stands alone with a space after it, which is his correction
and needs confirming by touch. What is still not settled is the end of a
hemistich: *punctuation if there is any, otherwise a space* is his phrase, and it
needs to be his words before it goes into two engines.

### 1.4 ۽ reads cleanly

Line 10 carries ۽, which used to be read back as اءين. Worth one question while
the paper is in his hands.

---

## 2. Two places the guide contradicts itself

Neither is ours to fix. Both are decisions for the Authority, and both should be
put to them in writing with a version number attached.

**Fractions.** Pages 52–53 state the rule twice and work nine examples:
numerator in the upper digits, denominator in the lower, no bar, and the
numerator dropped when it is 1. Page 50 instead writes fractions with a slash
cell (dots 3-4) between two upper digits, and states no rule. We implement
pp.52–53.

**Brackets.** Page 32 gives the round bracket as 2356 for both open and close.
Page 53 gives an entirely different set for arithmetic, and prints the open
square bracket with the same cell as the open round bracket, which must be a
slip. Prose and arithmetic may legitimately differ; the slip is separate.

Two smaller ones, same category: **page 31 prints dot 6 for both شد and بہ
زبرون**, and **page 54 prints the abbreviation of تعاليٰ with ٽ where ت is
expected**.

---

## 3. One rule that is ours, not the guide's

**Multiplication and the foreign-word mark are the same two cells** — 5-6 then
2-3-6 (pp.46 and 49). The translator separates them by the space: the guide
writes the foreign mark attached to its word, so a bare pair standing between two
numbers is multiplication. That works on everything we have, and it is our
invention. Ask him how a reader tells them apart, and record his answer as the
rule rather than ours. Sheet 3, line 3.

---

## 4. Parts of the standard nobody has seen

**Pages 1–26 and 56 onward of the guide have never been seen with the dots
visible.** Everything implemented comes from pp.27–55 plus his two books. Whatever
is in the unseen pages is not in the software, and we do not know what it is. This
is the largest single unknown in the project and it should be stated plainly in
the paper.

---

## 5. Checks not yet run

**A second reader.** Every confirmation so far has come from one person. Before
publication at least one other Sindhi braille reader should read sheets 1 to 4
cold. One reader agreeing with the software is not independent of the software if
the software was built from his books.

**Sheets 1 to 3 by touch.** The news page he read on 15 August was ordinary prose.
It carried no verse, no arithmetic, no contractions and no Grade 2. Those three
sheets exist to reach what that page did not.

**Braille somebody else made.** The strongest check available and the one still
missing: a `.brf` produced by the DEPD Braille Press, translated back by this
software and compared with their Sindhi. Requested, not yet received.

**liblouis on this machine.** `check_all.py` runs eleven checks here and skips the
twelfth because the liblouis tools are not installed on Windows. The tables
compile and pass 99/99 elsewhere; it should be run here once before the tables go
upstream.

---

## 6. Known limits that are not going to change

**Five Grade 2 cells stand for two words each.** His book gives the same cells to
two different words in five places. No software can separate them; a reader uses
the sentence. Listed in `docs/GRADE-2.md`.

**ھ at the end of a word.** 2-3-6 is the letter ھ, the question mark and the
lower 8. At the end of a word the letter is the default and the word list
recovers the question mark. It never resolves completely.

**ڻھ reads as 1/8.** Its two cells are also the number sign and lower 8. One of
four spellings in the whole list that cannot be read back.

**A PDF is not a source.** Measured on real books: a class-1 Sindhi Reader is 79
pages, 266 images, 874 KB a page — the pages are pictures and there is no text in
the file. The Authority's own printed guide has text but stores letter *shapes*
rather than letters, so its words cannot be recovered either. Both need the
document the book was made from, or OCR.

---

## 7. Not started

- **liblouis upstream.** The tables are written and pass their own suite; they
  have not been submitted.
- **Duxbury.** The press composes in Duxbury and works around it having no Sindhi
  table. Nothing has been sent to them.
- **Six-key entry on a refreshable display.** The site's writer works on an
  ordinary keyboard; nothing has been tested against a braille display.
- **The paper.** Riaz Hussain Memon as an author.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon**, with **Mansoor Ali Kori**.
