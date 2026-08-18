# Sindhi braille against its neighbours

**Run it:** `python tools/compare_codes.py`

## Why this is here

Every other check in this project compares the software with the Sindhi Language
Authority's own book, or with itself. Both were done by one person from one set
of documents. This check is the exception: it uses liblouis's Arabic, Persian and
Urdu tables, written by other people, for other languages, years before this
project existed.

It cannot settle anything. Sindhi braille is defined by the committee, and Urdu
braille has no authority over it. What it can do is corroborate: these scripts
share most of their letters, so where three unrelated codes independently put a
letter in the same cell we do, our reading of the Sindhi book is very unlikely to
be a transcription slip. And where Sindhi differs, there should be a reason
visible in the alphabet itself.

## The result

| against | agree | differ |
|---|---|---|
| Arabic (`ar-ar-g1`) | 29 of 32 shared letters | 3 |
| Persian (`fa-ir-g1`) | 32 of 33 | 1 |
| Urdu (`ur-pk-g1`) | 33 of 34 | 1 |
| **total** | **94 of 99** | **5** |

Every one of the five has a reason.

**پ, چ and گ against Arabic.** Arabic gives them 12, 245 and 13. In Sindhi those
cells are already ب, ج and ڪ. Arabic does not have ڪ at all, and treats پ چ گ as
borrowings; Sindhi treats them as native letters and has to give them cells of
their own. The disagreement is what you would predict from the two alphabets.

**ک against Persian and Urdu.** Both write it 1-3. Sindhi writes it 1-3 then
2-3-6. The reason is the same one: **1-3 in Sindhi is already ڪ**, a letter
neither Persian nor Urdu has. Sindhi cannot reuse it, so it marks the second k by
adding ھ.

That last line matters, because ک is the letter this project got wrong once. The
standard guide's printed dots appeared to show a single cell 4-6; Riaz Hussain
Memon's chart and his Grade 2 book both give two cells. We followed the book.
**Persian and Urdu braille, which neither of us wrote, corroborate the book** —
they agree that 1-3 is the plain k, and Sindhi's second k has to be marked
somehow because 1-3 is taken.

**He confirmed it himself on 15 August 2026**: ک is 1-3 then 2-3-6. Three
independent lines — his chart, his printed book, and two neighbouring codes —
had already agreed, and the author's own word closed it.

## What this changed about dots 4-6

It was listed as an open question in the form *"dots 4-6 carry nothing"*. That
was wrong, and this comparison is what exposed it.

Counting every cell the code assigns to anything — letters, digraphs, diacritics,
punctuation, digits and lower digits, arithmetic, brackets, quotes, the number
and letter signs, the verse and pen-name marks, the foreign marks, and every
Grade 2 contraction and series prefix — **all 63 cells carry something.**

Dots 4-6 is the prefix of the second ڳانڊڙا group series in Riaz Hussain Memon's
own Grade 2 book, page 17: **واب, باد, وڪر**.

That narrowed the question to one he could answer in a sentence, and on
**15 August 2026 he answered it**: dots 4-6 are that group prefix, the same thing
in Grade 1 as in Grade 2, and «وڏو اکر» on his chart is his own label for it. He
confirmed at the same time that **ک is two cells, 1-3 then 2-3-6**.

So this comparison did two things for that cell. It corrected a claim we had
been making, and it turned a vague question into a precise one — which is the
only reason it could be closed by asking rather than by guessing.

One lead it produced did not pan out: **Arabic braille puts إ in that cell**,
hamza below alef, a letter Sindhi folds into ا and never needs. That looked like
it might be what «وڏو اکر» pointed at. It was not.

## What it does not do

- It cannot tell us whether the guide's two self-contradictions should be
  resolved one way or the other. Those are the Authority's decisions.
- It says nothing about Grade 2 contractions, which have no counterpart in the
  neighbouring codes.
- It is still not a blind reader with a page in front of them. That check has not
  happened yet, and this one does not replace it.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon**. The reference tables are
liblouis's own and are included under their own licences in
`brailleTables/reference/`.


With **Mansoor Ali Kori**, who works with Riaz Hussain Memon on the composing and has taken part in the meetings throughout.