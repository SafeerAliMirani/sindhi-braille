# Standard Sindhi Braille — the complete code, as implemented

**13 August 2026.**

The mathematics of the implementation — the cell algebra, the transduction, the
ambiguity analysis and the measures used below — is in
`docs/MATHEMATICAL-MODEL.md`.

This document states every rule of the code that our software implements, gives
the page of the standard guide it comes from, and says how the rule was
verified. Where the printed guide is ambiguous or contradicts itself, this
document says so rather than choosing silently.

---

## 0. Two rules settled from the sources, 20 August 2026

### ه and ھ

**Sindhi writes ھ (U+06BE, dots 2-3-6). Not ه (U+0647, dots 1-2-5).** Counted in
the two primary sources:

| word | with ه | with ھ |
|---|---|---|
| آهي / آھي | 0 | 149 |
| ته / تھ | 0 | 234 |
| گهر / گھر | 0 | 19 |
| پڙهڻ / پڙھڻ | 0 | 18 |
| the standard guide, whole | 80 | **2251** |
| Riaz Hussain Memon's Grade 2 book, whole | 8 | **127** |

Every instance of ه in those sources is an Arabic or Persian loanword or a name
that ends in it: علاوه، وغيره، رحمه، عليه، الله، فھميده، سائره، سنجيده, and the
guide's own title ربهر.

This is not a spelling preference. The two are different cells, so text written
with ه for a native word embosses 1-2-5 where 2-3-6 belongs.

`tools/sindhi_words.txt` writes the ھ form and carries the ه form at frequency
zero, so the back-translator can still read documents other people wrote.

### ڪ followed by ھ is the same two cells as ک

ک is 1-3 then 2-3-6. ڪ is 1-3 and ھ is 2-3-6. **The sequence is identical**, so
back-translation has to choose, and it was choosing greedily: ڪھڙو, an ordinary
Sindhi word, came back as کڙو, which is not a word at all.

Resolved the way the word-final 2-3-6 already was, by asking the lexicon: the
aspirate reading is taken unless the two-letter reading completes a known word
and the aspirate reading does not. This is ours, not the guide's, and the guide
does not say how a reader tells them apart.

---

## 1. Where the code comes from

Standard Sindhi Braille was given final form on **7 November 2016** under the
patronage of the **Sindhi Language Authority**, an autonomous institution of the
Government of Sindh established under the Use of Sindhi Language Act 1972 and
the Teaching, Promotion and Use of Sindhi Language (Amendment) Act 1990. It was
agreed unanimously by a committee of six:

| | |
|---|---|
| Prof. Dr Abdul Ghafoor Memon | Chairman, Sindhi Language Authority |
| Shahid Ahmed Memon | Convener |
| **Riaz Hussain Memon** | Member — blind teacher; President, Pakistan Association of the Blind, Sindh |
| Prof. Mehrab Ali Lakho | Member |
| Dr Saira Saleem Khan | Member |
| Shamsuddin Shaikh | Member |

Certified by Haroon Inayat Abbasi, Secretary. The certificate is printed on
page 23 of the committee's book *ﻣﮑﻤﻞ ﺳﻨﮉﻱ ﺑﺮﻳﻞ ﺩﺭﺟﻮ II*.

The Government of Sindh has printed school textbooks in this code through the
DEPD Braille Press, Karachi.

**Sources used here**

| Source | What it is | Pages we can read |
|---|---|---|
| معياري سنڌي بريل رھبر | the standard guide, printed with visible dots | 27–55 (29 of 47+) |
| ڪامل سنڌي بريل درجو II | the Grade 2 book | the manuscript, supplied by the author |
| Class 6 Sindhi textbook | printed by the Government of Sindh in this code | 9 pp. |
| Riaz Hussain Memon | committee member, read our output by touch | in person, 12 Aug 2026 |

**Scope.** This is Sindhi in its **Perso-Arabic** orthography, the script used in
Pakistan. It is not the same code as the Devanagari Sindhi table of the Braille
Council of India: about a dozen Arabic-origin letters (ث ذ ص ض ط ظ ع غ ح خ ق)
have no Devanagari counterpart, and the two cannot substitute for one another.

---

## 2. The alphabet

52 letters. Written left to right, even though the print runs right to left.

| | | | | | | |
|---|---|---|---|---|---|---|
| ا 1 | ب 12 | ٻ 26 | ڀ 23 | ت 2345 | ٿ 1256 | ٽ 246 |
| ٺ 135 | ث 1456 | پ 1234 | ج 245 | ڄ 356 | ڃ 35 | چ 14 |
| ڇ 16 | ح 156 | خ 1346 | د 145 | ڌ 1236 | ڏ 34 | ڊ 346 |
| ڍ 256 | ذ 2346 | ر 1235 | ڙ 12456 | ز 1356 | س 234 | ش 146 |
| ص 12346 | ض 1246 | ط 23456 | ظ 123456 | ع 12356 | غ 126 | ف 124 |
| ڦ 235 | ق 12345 | ڪ 13 | **ک 13-236** | گ 1245 | ڳ 13456 | ڱ 2356 |
| ل 123 | م 134 | ن 1345 | ڻ 3456 | و 2456 | ه 125 | ھ 236 |
| ي 24 | ء 3 | آ 345 | | | | |

**ک is two cells — ڪ (13) followed by ھ (236).** This is what Riaz Hussain
Memon's chart gives and what his printed Grade 2 book uses. Both are primary
sources, and they agree.

An earlier revision of this document changed ک to the single cell 4-6, because
the standard guide's own printed dots appear to show 4-6 on several pages where
ک was expected. **That was wrong and has been reverted.** Where the guide's
typesetting and the author's own book disagree, the author's book decides.

Dots 4-6 are settled too. **Riaz Hussain Memon confirmed on 15 August 2026 that
they are the ڳانڊڙا group prefix, the same in Grade 1 as in Grade 2**, and that
«وڏو اکر» on his chart is his label for that prefix rather than a second
function. Grade 1 therefore writes nothing for the cell, which is what this
specification has always described, and the guide's printed 4-6 on pp.31, 41, 42
and 44 is a typesetting fault.

**Borrowed words do not change a letter's value.** Sindhi ک and Urdu ک are one
Unicode character, U+06A9, worth 1-3 2-3-6 in Sindhi and 1-3 in Urdu. Riaz
Hussain Memon ruled on 15 August 2026 that this needs no special handling:
Sindhi shares many letters with Urdu, and a reader reads that letter the same way
whichever language the word came from. **The code is one script with one value
per letter, and the software never branches on the language of a word.**

**The two h's.** Guide p.30 states the reason for them:

> "In braille, dots 1-2-5 have been fixed for ه. If only 1-2-5 were used for ھ as
> well, countless word ambiguities would arise; it was therefore considered
> necessary to fix a second form of ھ, for which dots 2-3-6 were assigned."

So ه = 125 and ھ = 236, and 236 is what forms an aspirate after a consonant.

**Aspirated digraphs** (guide p.30, printed with dots): جھ 245-236, گھ 1245-236,
ڙھ 12456-236, لھ 123-236, مھ 134-236, نھ 1345-236, ڻھ 3456-236. The rule is
general: any consonant followed by ھ.

**Folded forms.** ئ ؤ → ء · أ إ ٱ → ا · ة ہ → ه · ی → ي · ك → ڪ.
The two Sindhi signs have no cell of their own and are spelled out as the
committee's own book spells them: ۾ → م ي ن, ۽ → ا َ ء ي ن.

---

## 3. Diacritics

Written only at beginner level (classes 1–3); ordinary Sindhi braille omits
them.

| sign | dots | | sign | dots |
|---|---|---|---|---|
| زبر (fatha) | 2 | | بہ زيرون (tanwīn kasr) | 35 |
| زير (kasra) | 15 | | بہ زبرون (tanwīn fath) | 6 |
| پيش (damma) | 136 | | بہ پيش (tanwīn damm) | 26 |
| شد (shadda) | 6 | | ڪڙا زبر (dagger alif) | 4 |
| جزم (sukūn) | 25 | | | |

**Placement (guide p.31) — two different rules:**

> "in braille, write the letter and then write the zer, zabar or pesh in the cell
> **after** it."
>
> "But if shadda is used in a word, the shadda is placed **before** the letter
> that carries it."

Confirmed in print: السَّلام = ا ل **شد** س ز ب ر ل ا م.

**Known problem.** The guide prints the same cell, dot 6, for both شد and
بہ زبرون. Either the two really share a cell, or one of the two table entries is
a misprint. Unresolved.

---

## 4. Punctuation, brackets and quotation marks

Guide p.32. All are attached to the word with **no space before them**.

| mark | dots | | mark | dots |
|---|---|---|---|---|
| ، comma | 2 | | ( ) round bracket | 2356 (both) |
| ؛ semicolon | 23 | | [ open square | 6-2356 |
| : colon | 25 | | ] close square | 2356-3 |
| . full stop | 256 | | " open double quote | 236 |
| ! exclamation | 235 | | " close double quote | 356 |
| ؟ question | 236 | | ' open single quote | 6-236 |
| - hyphen | 36 | | ' close single quote | 356-3 |
| :- heading dash | 25-36-36 | | ___ short blank | 36-36 |
| = (in words) | 25-25 | | ______ long blank | 36-36-36-36 |

Note: the semicolon is **23**. Dots 25 are the colon, and the same cell also
carries jazam and, after a number sign, the lower 3.

**Brackets differ between prose and arithmetic.** In arithmetic (guide p.53) the
brackets are entirely different cells: ( = 126, ) = 345, { = 246, } = 135,
] = 123456. The guide prints the open square bracket there with the *same* cell
as the open round bracket, which must be a misprint. **Unresolved.**

---

## 5. Numbers

**The number sign is 3456**, placed before the digits.

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 14 | 145 | 15 | 124 | 1245 | 125 | 24 | 245 |

These are the "**Upper Sign**" digits of guide p.43 — the top of Louis Braille's
first line. The same ten cells dropped one row are the "**Lower Sign**" digits:

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |
|---|---|---|---|---|---|---|---|---|---|
| 2 | 23 | 25 | 256 | 26 | 235 | 2356 | 236 | 35 | 356 |

**Dot 6 closes a number before punctuation** (guide pp.43, 52):

> "If you write ¾ in braille and then give it a full stop, the reader will read
> it as 3/44 … so before the mark, give dot six, and after that write the
> punctuation mark."

**Decimal point = dot 2. Thousands comma = dot 3** (guide p.51):

> "When writing prose or poetry in braille, dot 2 is used for the comma. But
> when sums are written in braille and a comma is used, dot 3 is used, because
> dot 2 is used in sums as the decimal-point sign."

**Ratio = 25**, with a fresh number sign on each side: 14:7 → 3456 1 145 · 25 ·
3456 1245.

**Ordinals** (guide p.47) are written exactly like the plain cardinal — number
sign plus digit, nothing more. The Sindhi ending (ـون / ـين) is not written in
braille at all; the reader supplies it.

---

## 6. Fractions

Guide pp.52–53, stated as a rule twice and shown in nine worked examples:

> "the numerator's digit must be written in the upper sign and the denominator's
> digit in the lower sign."
>
> "whenever a 1 is present in the numerator and any digit is written in the
> denominator, then in braille the numerator's 1 is **not** written, and the
> digit in the denominator is written directly in the lower sign."

There is **no fraction bar**. One number sign covers the whole fraction.

| | braille |
|---|---|
| 3/7 | 3456 · 14 · 2356 |
| 3/4 | 3456 · 14 · 256 |
| 13/44 | 3456 · 1 · 14 · 256 · 256 |
| 25/88 | 3456 · 12 · 15 · 236 · 236 |
| 1/2 | 3456 · 23 |
| 1/8 | 3456 · 236 |
| 1/10 | 3456 · 2 · 356 |

A mixed number repeats the number sign: 5/4 = 1¼ → 3456 15 256 · 56 2356 ·
3456 1 · 3456 256.

**A contradiction inside the guide.** Page 50 writes fractions a *different* way
— with a slash cell, dots 34, between two upper digits: 1/4 = 3456 1 34 145.
Pages 52 and 53 use the lower-digit rule and state it explicitly; page 50 does
not state any rule. We implement the pp.52–53 rule, because it is stated as a
rule and has nine examples against page 50's two. **This should be put to the
Authority: the standard contradicts itself here.**

---

## 7. The letter sign, dots 5-6

Guide p.42:

> "in ordinary writing, when a detailed essay is written it is divided into parts
> such as ا، ب، ج، د etc. In braille, the letter sign 5-6 is prescribed for
> identifying such letters."

It marks any letter that is standing in for a number or a symbol.

**Exercise labels:** ا. → 56 1 256 · ب. → 56 12 256 · ج. → 56 245 256.

**Abjad numerals** (guide p.48): 56 + letter + 256.

**Roman numerals** (guide p.48), one letter sign per numeral, then the English
letters: I = 24, V = 1236, X = 1346, L = 123, C = 14, D = 145, M = 134. So
VIII → 56 1236 24 24 24.

> "Before writing those Roman numerals it is necessary to give the 'Roman or
> letter sign' in braille, because braille is a form of writing with a limited
> set of signs."

**Arithmetic signs** (guide pp.49–51), each carrying the letter sign:

| + | − | × | ÷ | = | % |
|---|---|---|---|---|---|
| 56-235 | 56-36 | 56-236 | 56-256 | 56-2356 | 25-1234 |

Worked examples from the guide, which our translator reproduces exactly:
8+9 = 17 · 20−13 = 7 · 12×8 = 96 · 91÷7 = 13.

The percent sign is printed **before** the number: 1% → 25 1234 3456 1. It is
the one arithmetic sign that does *not* carry the letter sign.

**The multiplication sign is dots 5-6 2-3-6 — the same two cells that open a
foreign word** (p.46). Nothing in the cells separates them. What separates them
is the space: the foreign mark is written *attached* to the word it opens, so a
bare two-cell 5-6 2-3-6 standing alone between two numbers is multiplication.
That is how the translator decides, and it is worth confirming with a reader.

---

## 8. Religious abbreviations

Guide p.54. The abbreviation is the initial letter or letters, followed by the
full-stop cell 256, **with no space**:

> "whenever any religious abbreviation is written, it is necessary to place the
> punctuation mark — the full stop — after it without a space."

| phrase | braille |
|---|---|
| حضرت | 156 · 1246 · 256 |
| تعاليٰ | 2345 · 12356 · 256 |
| هجري | 125 · 256 |
| قبل مسيح | 12345 · 134 · 256 |
| عيسوي | 12356 · 256 |
| رحمة الله عليه | 1235 · 156 · 256 |
| رضي الله عنه | 1235 · 1246 · 256 |
| ڪرم الله وجه | 13 · 1235 · 134 · 256 |
| صلعم / ﷺ | 12346 · 256 |

**The ع rule** (guide p.55), which no reader could guess:

> "The abbreviation ع is used for two purposes: for عليه السلام, and secondly for
> عيسوي. Whenever ع comes after the name of a prophet it is written and read as
> عليه السلام; but if ع is written after a year, it is read as عيسوي."

So `1947 ع.` is 1947 AD, and `حضرت آدم ع.` is Adam, peace be upon him — the same
two cells, decided by what stands before them.

**A misprint in the guide.** The تعاليٰ entry is printed with ٽ (246) where ت
(2345) is meant. We implement ت.

---

## 9. Marks that span more than one word

| what | braille | source |
|---|---|---|
| a word repeated | write it once, then 3 3 with no space | p.45 |
| a fill-in-the-blank | 3 3 3 | p.44 |
| footnote / star | 35 35 | p.44 |
| verse or poem | 12356 12356 at the start; once more, unspaced, at the end of each hemistich; full stop at the end of the stanza | pp.40–41 |
| poet's pen-name | dot 2 immediately before the word | p.41 |

Verse cannot be detected from the text, so it is asked for:
`translate(..., poetry=True, takhallus='لطيف')`, or `--poetry --takhallus لطيف`
on the command line, or the **Verse** switch on the website. Each input line is
treated as one hemistich; a blank line ends the stanza.
| واؤ عطف joiner | 36 | Riaz |

On the repeated word (guide p.45):

> "if such a word must be written twice, write the word once and, with no space,
> write dot 3-3 joined to the word; its meaning is that the same word is written
> a second time too."

This is the rule Riaz described to us before we had ever seen it in print.

---

## 10. Words from other languages

Guide pp.45–46. Arabic, Urdu and English inside Sindhi are wrapped in a pair of
marks:

> "give the sign dots 5-6 and 2-3-6 and write the word or sentence with no space
> after it. Where it ends, if there is a punctuation mark it is used with no
> space, and after it, with no space, the language sign 3-5-6, 2-3 closes it."

Open **56 236** … close **356 23**, once around the whole run, not around each
word. English inside is written in ordinary English braille, with **dot 6** for a
capital: the guide's own example prints "Thanks" as 6 2345 125 1 1345 13 234.

---

## 11. Cells that carry more than one meaning

Braille has 63 cells and Sindhi needs more than 63 things. The guide says so
itself (p.39): *"since braille has only 63 signs … fixing signs for them is
necessary; otherwise many ambiguities would arise everywhere."* Six cells do
double duty:

| cell | readings | how it is decided |
|---|---|---|
| 3456 | number sign · ڻ | number sign at the start of a word, ڻ everywhere else. **Verified: no Sindhi word begins with ڻ** — 0 in 21,445 words of the committee's own books, against 619 occurrences inside words |
| 256 | full stop · ڍ · lower 4 | letter inside a word, mark at the end, lower digit after a number sign |
| 236 | ھ · ؟ · lower 8 · open quote | ھ is by far the commonest at the end of a word; see below |
| 2 | zabar · comma · decimal point · lower 1 · pen-name mark | diacritic after a letter, comma after a completed word, decimal point inside a number |
| 235 | ڦ · ! | letter inside a word, mark at the end |
| 25 | colon · jazam · ratio · lower 3 | a ratio is followed by a fresh number sign; a denominator is not |

**The one genuine ambiguity we cannot resolve by rule** is 236 at the end of a
word: ھ or ؟. Guide p.35 says only that the question mark is written *"at the end
of the sentence, without a space"* — the same position as a final ھ. Sindhi forms
aspirates with ھ and a great many ordinary words end that way (پڙھ، تھ، بھ، ڏوھ،
اولھ، ڳالھ), so the letter is the default reading; our translator uses a Sindhi
word list to recover the question mark. A human reader resolves it from the
sense of the sentence, and so must a machine.

**New collision found.** `3456 236` is both ڻھ (guide p.30's own example) and the
fraction 1/8. Harmless in practice, because no Sindhi word begins with ڻ, but it
is real and belongs in the record.

---

## 12. What was verified, and how

| claim | evidence |
|---|---|
| the 52 letters | Riaz's chart; measured off the printed Grade 2 book (27 of 28 rows); embossed on an Index Everest-D V5 and read by touch without error, 12 Aug 2026 |
| every rule in §§3–10 | read off the printed dots of the guide, decoded by size, cross-checked visually at 5–16× magnification |
| the translator | **69 of 69** worked examples printed in the guide reproduced cell for cell |
| forward translation | agrees cell for cell with an independent implementation written separately from the same sources |
| round trip | **99.94%** of 23,434 word tokens from the committee's own publications |
| the liblouis table | compiles clean; **95 of 95** tests pass |

**What "99.94%" leaves out.** The residue is the ع abbreviation, which needs
sentence context, plus two spelling variants. Nothing else fails.

**What this does NOT prove.** Both implementations were written by the same
author from the same documents, and the tests were written by that author too.
Their agreement proves consistency, not correctness. The single thing that would
break that circle is a braille file produced by somebody else — the Class 6
textbook as a `.brf` from the DEPD Braille Press — which we have requested and
do not yet have.

---

## 13. Still open

1. **Pages 1–26 and 56 onward** of the guide have never been seen with the dots
   visible.
2. **The guide contradicts itself on fractions** (p.50 vs pp.52–53) and on
   **brackets** (p.32 vs p.53). Both need the Authority, not us.
3. **شد and بہ زبرون** are printed with the same cell on p.31.
4. **Grade 2 contractions** are implemented and checked both ways. What is open
   there is the five cells his book gives to two words each — see
   `docs/GRADE-2.md`.
5. **One reader.** Every confirmation has come from one person. Before
   publication at least one other Sindhi braille reader should read our test
   sheets cold.
6. **Authority.** Where we believe the guide is wrong, we do not get to fix it.
   A change to this code is a change to a standard ratified by a committee of the
   Sindhi Language Authority. Any deviation must be written down, taken to Riaz,
   and endorsed in writing, with a version number attached. It is not a bug fix.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon** — blind teacher, President of
the Pakistan Association of the Blind (Sindh), and a member of the committee that
authored the code. The braille code itself is the work of the Sindhi Language
Authority committee and is not altered here.


With **Mansoor Ali Kori**, who works with Riaz Hussain Memon on the composing and has taken part in the meetings throughout.