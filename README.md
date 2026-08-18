# Standard Sindhi Braille — the first digital implementation

Standard Sindhi Braille was given final form on **7 November 2016** under the
**Sindhi Language Authority**, by a committee of six: Prof. Dr Abdul Ghafoor
Memon (Chairman), Shahid Ahmed Memon (Convener), **Riaz Hussain Memon**,
Prof. Mehrab Ali Lakho, Dr Saira Saleem Khan, Shamsuddin Shaikh. Certified by
Haroon Inayat Abbasi, Secretary. The Government of Sindh prints school textbooks
in it through the DEPD Braille Press, Karachi.

It had never been implemented in software. This is that implementation. The code
here is the committee's, letter for letter — nothing has been invented or
changed.

**On 15 August 2026 a blind reader read a page of it from embossed paper, cold,
complete and without an error.** That is the result this repository exists to
report; `docs/READING-2026-08-15.md` records the sitting and what it found.

**Try it:** <https://sindhi-braille.pages.dev> — the translator, a six-key braille
writer that speaks, and the fifty-two letters. One file, no server, works offline.

---

## Quick start

```bash
git clone https://github.com/SafeerAliMirani/sindhi-braille
cd sindhi-braille

# translate something
python tools/sindhi_braille.py "سنڌي ٻولي هڪ شاهوڪار ٻولي آهي." --width 28

# a whole document, or a folder of them
python tools/braille_batch.py INPUT -o OUTDIR --width 28

# run every check
python tools/check_all.py
```

`check_all.py` is the one that matters. It runs twelve checks and tells you which
it could not run rather than quietly passing them. The website needs nothing at
all: open `website/index.html` in a browser.

**Set the width to the machine.** A `.brf` wider than the paper is re-wrapped by
the embosser, and an embosser breaks lines in the middle of words. A4 fits 28.

---

## State of the work

| | |
|---|---|
| **Grade 1** | complete — letters, diacritics, punctuation, numbers, fractions, arithmetic (including per cent and the arithmetic brackets), Roman and abjad numerals, religious abbreviations, verse and pen-name marks, words from other languages |
| **Grade 2** | 237 contractions and 6 word-groups, both directions |
| **Verified** | **69 of 69** worked examples printed in the standard guide, reproduced cell for cell — plus **11 rules** the guide states without a worked example, implemented as we read them and counted separately on purpose |
| **Round trip** | **99.94%** of 23,432 words from the committee's own publications |
| **liblouis** | `sd-pk-g1.utb` compiles clean, **99/99** tests; `sd-pk-g2.ctb` compiles clean. Both include `sd-pk-g1-core.uti` |
| **Cross-check** | the browser engine and the reference translator agree on **70 of 70** cases, contracted braille and verse included |
| **Neighbouring codes** | **94 of 99** shared letters agree with Arabic, Persian and Urdu braille; the five that differ are letters those codes do not have |
| **Grade 2 round trip** | **238 of 243**; the five that fail are cells the book itself gives to two words |
| **Read by touch** | **15 August 2026** — Riaz Hussain Memon read an embossed page of ordinary Sindhi news prose, cold, complete, **without an error**. The one check above that is not a machine checking a machine. `docs/READING-2026-08-15.md` |
| **Still to read** | that page carried no verse, no arithmetic and no contractions. The four sheets in `test-sheets/` reach the parts it did not |

Open questions are in **`docs/OPEN-QUESTIONS.md`**. Read it before publishing
anything.

---

## The folder

| | |
|---|---|
| `website/` | `index.html` — the site. One self-contained file: live translator, six-key braille writer, the alphabet, the evidence. Opens offline. `src/` holds the two sources it is built from and `build.py`. |
| `tools/` | `sindhi_braille.py` — the translator. `check_all.py` — every check, one line each. `verify_guide.py` — checks it against the guide's printed examples. `compare_codes.py` — against Arabic, Persian and Urdu braille. `braille_batch.py` — a folder of documents to `.brf`. `braille_layout.py` — true-size page layout. `make_test_sheets.py`, `make_check_sheet.py`, `make_decision_sheet.py` — the print sheets, the on-screen check sheet, and the sheet of things still to be decided. `make_ambiguity.py` and `make_wordlist.py` — generate the two things the website used to carry by hand. `sindhi_words.txt` — the word list used for back-translation. |
| `brailleTables/` | `sd-pk-g1.utb` and its test suite, `sd-pk-g2.ctb`. `reference/` holds Urdu, Arabic and English tables for comparison. |
| `docs/` | The specification in English and Sindhi, the mathematical model in both, Grade 2, the open questions, the comparison against Arabic, Persian and Urdu braille, how to verify the work, **the record of the first reading**, the Everest printing runbook, the colour-plus-braille print pipeline, the website plan. |
| `official-code/` | The code as data: `sindhi_braille_FINAL.csv`, `grade2_contractions.csv`, `grade2_groups.csv`, provenance, and `source/` — Riaz Hussain Memon's own books. |
| `test-sheets/` | `print-1-grade1.brf`, `print-2-grade2.brf`, `print-3-poetry-maths-foreign.brf`, `print-4-decisions.brf`, their keys (`ANSWER-KEY.md`, `ANSWER-KEY.pdf`, `DECISION-KEY.md`) and `CHECK-poetry-maths-foreign.html` to check on screen. One A4 page each, 28 cells. |
| `photos/` | The books, the approval letter, tactile-graphics examples. |
| `_to_delete/` | Superseded files, kept until you delete the folder yourself. |

---

## Running it

```
python tools/check_all.py                               # every check, one line each
python tools/sindhi_braille.py book.txt -o book.brf     # Sindhi -> braille
python tools/sindhi_braille.py book.brf --back          # braille -> Sindhi
python tools/sindhi_braille.py book.txt --grade2 -o out.brf        # contracted
python tools/sindhi_braille.py poem.txt --poetry --takhallus لطيف  # verse
python tools/braille_batch.py FOLDER -o out --width 28  # a whole folder
```

`check_all.py` is the one to run after any change. It reports twelve checks and
tells you which it could not run, rather than quietly passing them.

How to check the work yourself, step by step: **`docs/HOW-TO-VERIFY.md`**.

Pure standard library. No installation.

Page width matters: **28 cells fits A4**, 40 is the international page and needs
braille paper. See `docs/EVEREST-PRINTING.md`.

---

## Converting a document

Two ways in, and they produce the same bytes — `check_all.py` proves it by hash
over a 36-page document.

| | |
|---|---|
| **In the browser** | *Open a document* on the site. Plain text, Markdown and Word `.docx`. It converts the whole file, shows the first braille page, and writes a `.brf` you save. Nothing is uploaded. |
| **On the command line** | `python tools/braille_batch.py INPUT -o OUTDIR --width 28`. Also reads `.html`, `.odt` and `.pdf`, and takes whole folders. |

**Set the width to the machine.** A `.brf` wider than the paper is re-wrapped by
the embosser, and an embosser breaks lines in the middle of words. A4 fits 28.

### What it will not do, and why

**A PDF is described, not converted.** Open one and the site reports its pages,
its images and its kilobytes per page, then tells you to select the text in your
own PDF reader and paste it in. That is not a workaround — the selecting is the
work. A page of a book carries page numbers, running headings, captions, figure
labels and table cells, all of them text and none of them belonging in the
braille, and only a person can tell which is which.

An earlier version tried to extract the text here and it is worth recording why
it was removed. Reading a PDF's text means resolving every font's own character
map and following the positioning operators to find word boundaries. Done
loosely it returns text that looks right and is not: a CV came back as
`Dr.SafeerAli℧ira♪iPhD`, and a 79-page picture book was reported as having four
thousand letters a page when it has about twenty. Both would have produced
confident nonsense. What the site reports now — page count, image count, bytes
per page — needs no interpretation and cannot be got wrong.

**Kilobytes per page tells you what kind of file it is.** A page of text costs
tens of kilobytes; a scanned or drawn page costs hundreds. A Sindhi Reader for
class 1, measured: 79 pages, 266 images, **874 KB a page** — the pages are
pictures, so there is no text in the file at any price. The Authority's own
printed guide is 7 KB a page, but stores letter *shapes* rather than letters, so
its words cannot be recovered either. Both need the document the book was made
from, or OCR.

**Nothing is dropped silently.** Every character with no braille in the standard
is counted and listed in the report. A silent drop in a schoolbook is the kind of
error nobody notices until a child does.

**Verse is switched off for a document.** The verse option marks *every* line as
a hemistich, which is right for a bait and wrong for a book. Grade 2 stays
available, because real books are contracted.


---

## Next

1. Print `test-sheets/print-1-grade1.brf`, `print-2-grade2.brf` and
   `print-3-poetry-maths-foreign.brf` and have Riaz read them by touch, cold,
   against the answer key.
2. Close what is left of the open questions. The one that had to go to him,
   dots 4-6, he answered on 15 August 2026: it is the ڳانڊڙا group prefix in
   both grades, and ک is two cells, 1-3 then 2-3-6. What remains is the guide's
   own self-contradictions, which are the Authority's to settle.
3. GitHub, then the site.
4. liblouis, then Duxbury.
5. The paper, after a successful print, with Riaz Hussain Memon as an author.

---

## Licence, and what it covers

The software is **MIT** licensed — see `LICENSE`. Use it, change it, ship it in a
commercial product; keep the notice.

**Standard Sindhi Braille itself is not ours to licence.** It was authored and
ratified by a committee of the Sindhi Language Authority, Government of Sindh,
and it belongs to them. The tables in `official-code/` are a machine-readable
record of that standard, published so the software can be checked against it.
Riaz Hussain Memon's books and the Authority's printed guide are **not** in this
repository.

`brailleTables/reference/` holds liblouis tables by other authors under their own
licences — see the NOTICE there.

## Citing this

> Mirani, S. A., and Memon, R. H. (2026). *Standard Sindhi Braille: a digital
> implementation.* https://github.com/SafeerAliMirani/sindhi-braille

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon** — blind teacher, President of
the Pakistan Association of the Blind (Sindh), and a member of the committee that
authored the code, with **Mansoor Ali Kori**. The braille code itself is the
committee's work and is not altered here.


With **Mansoor Ali Kori**, who works with Riaz Hussain Memon on the composing and has taken part in the meetings throughout.