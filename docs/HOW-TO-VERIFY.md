# How to verify this work

Four levels, cheapest first. The first two you can do alone in ten minutes. The
third needs Riaz. The fourth is the only one that settles the question, and it
needs the press.

Do not skip to level four. Each level catches a different kind of error, and a
level-one failure would waste a level-four favour.

---

## Level 1 — the machine checks itself (2 minutes, you alone)

```
cd "E:\Sindhi Braille Project\tools"
python check_all.py
```

Eight lines come back. What each one means:

| check | what a pass proves | what it does not prove |
|---|---|---|
| `guide` | the software reproduces **69 examples the standard guide printed**, cell for cell | only that we read those 69 pages right |
| `rules` | **11 rules** the guide states but never works an example of — per cent, the arithmetic brackets, verse — behave as we read them | **nothing about whether our reading is right.** This is a lock against drift, not evidence |
| `selftest` | 16 sentences survive Sindhi → braille → Sindhi | — |
| `words` | 99.94% of 23,434 words survive the same trip | that the software is consistent with itself |
| `grade2` | 238 of 243 contractions survive both ways | the 5 failures are the book's own collisions, not bugs |
| `sheets` | the print files rebuild byte for byte from the source | that nobody edited a `.brf` by hand |
| `liblouis` | both tables compile and 99 tests pass | that a screen reader *could* use them, not that the output is right |
| `browser` | the website's engine and the Python agree on 70 cases | they were written by the same person — see below |

**`skip` is not `pass`.** If liblouis is not installed on the machine you run
this on, that line says `skip` and the summary lists it separately. Install
liblouis if you want that check to count.

**A `FAIL` on any line means stop.** Send me the line.

---

## Level 2 — read the code with your own eyes (10 minutes, you alone)

Open **`test-sheets\CHECK-poetry-maths-foreign.html`** in a browser. Twenty-nine
rows: what you type, the braille, **the dot numbers**, and what comes back.

Then put the printed guide beside it and **compare the dots column against the
book**. That is the only part of this whole document where a person is doing
something a computer cannot: the software can tell you it is self-consistent, it
cannot tell you it matches a page it has never seen.

The rows worth the most attention, because no printed example backs them:

- **50% and 1%** — the guide says the sign goes *before* the number. Check that.
- **(8 + 9)** — arithmetic brackets are 126 and 345, not the prose 2356.
- **the three verse lines** — 12356 twice at the start, once at each line's end,
  dot 2 before the pen-name.

Green edge means the text came back exactly. Amber means something changed —
and only two rows should be amber, both of them spellings braille has no cell
for (۾ → مين, and ئ → ء in the verse). **A third amber row is a finding.**

You can do the same live at any time on the website: type into the translator,
turn on **Grade 2** or **Verse**, and read the panel underneath, which names
every difference and why.

---

## Level 3 — a blind reader reads it cold (Riaz, one sitting)

This is the first check that is not circular. Everything above was written by
one person from one set of documents; a page under someone else's fingers is
not.

**It has been done once, on 15 August 2026**, on a page of ordinary Sindhi news
prose: read complete, by touch, without an error. `docs/READING-2026-08-15.md`
records what was read, what he found and what each finding turned out to be. What
that page did not carry was verse, arithmetic or contractions, which is what the
four sheets below are for.

1. Emboss the four sheets in `test-sheets\`. Follow `docs\EVEREST-PRINTING.md`
   — hammer test first, 28 cells, single-sided. **Write the file at the width of
   the machine.** A `.brf` wider than the paper is re-wrapped by the embosser,
   which breaks lines in the middle of words.
2. Give Riaz the paper. **Do not tell him what any line is meant to say.**
   Do not read the answer key aloud first. Write down what he reads.
3. Compare afterwards against `test-sheets\ANSWER-KEY.md`.

A line he cannot read at all is as useful a result as one he reads wrongly —
note which it was.

Four lines are worth asking him about rather than just marking right or wrong:

- **sheet 1, line 11** ends in ڻھ, which is also readable as ⅛. Ask him how a
  reader tells the number sign from ڻ.
- **sheet 3, line 3** is `12 × 8 = 96`. The × sign is the same two cells that
  open an English word. Ask him how a reader tells those apart.
- **sheet 3, lines 17–19** are verse. Ask him whether that is how a bait looks.
- **dots 4-6** were the last of these, and he answered on 15 August 2026: the
  ڳانڊڙا group prefix, the same in both grades, and ک is two cells. Sheet 1
  line 13 is still the touch test for it.

---

## Level 4 — braille somebody else made (the DEPD Braille Press)

Ask the press for the **Class 6 Sindhi textbook as a `.brf` file** — in Duxbury,
File → Save As → Formatted Braille. Then:

```
python tools\sindhi_braille.py class6.brf --back -o class6-read-back.txt
```

Read the result. If it is Sindhi, the code is right. If it is not, we learn
exactly where and why.

This is the check that matters, because that file was produced by a person and a
program that have never seen this project. Nothing we can run against ourselves
can substitute for it. **It has been requested and is not yet in hand.**

---

## When something disagrees

Write down four things and send them:

1. what you typed, exactly
2. what the software gave — the **dot numbers**, not the braille characters
3. what it should have given, and **where you know that from** — a page number
   in the guide, a page in the Grade 2 book, or Riaz saying so
4. which of the four levels above you were on

The third one is what makes it actionable. A correction that comes with a page
number gets applied; one that does not gets recorded in `docs\OPEN-QUESTIONS.md`
until it has a source. That rule is why the ک error was caught and reverted, and
it is worth keeping.

---

## What "verified" will mean

Not "the checks pass". They pass now. It will mean:

- level 1 clean, **and**
- level 2 compared against the printed guide by a person, **and**
- level 3 read by two blind readers, not one, **and**
- level 4 done with a file from the press.

Three of those four are still open. Until they are closed, the honest phrase is
*"no known errors"* — not *"correct"*.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon** — blind teacher, President of
the Pakistan Association of the Blind (Sindh), and a member of the committee that
authored the code.


With **Mansoor Ali Kori**, who works with Riaz Hussain Memon on the composing and has taken part in the meetings throughout.