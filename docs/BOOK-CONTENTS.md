# سنڌي بريل: پهريون ڪتاب
# Sindhi Braille: the first book

**A twin-vision primer for grade 1. Every page carries the same thing twice:
in print for the sighted reader, in braille for the blind one. Two people, one
book, at the same time.**

Draft table of contents. **48 pages.**

---

## Read this before the rest

Two kinds of content are mixed below, and they are not equally reliable.

**The braille cells are exact.** Every dot pattern printed here comes from the
implemented tables and has been checked against the committee's book. Do not
change them.

**The Sindhi words are my drafts and must be checked.** I am not a native
speaker. Every word below has been machine-checked for two things — that it uses
no letter the book has not yet taught, and that it survives translation to
braille and back unchanged — but that says nothing about whether it is the right
word for a six-year-old, or whether it is spelled as Sindhi schools spell it.
**Give the word lists and sentences to Gemini and then to Riaz.** Three of my
first drafts were already wrong and the checker caught them.

---

## How the letter order was chosen

Not alphabetically. Teach the alphabet in its traditional order and a child
spends nine lessons unable to read a single word.

The order below is **greedy against a real corpus**: at each step, the letter
added is the one that makes the largest number of real Sindhi words readable.
After four lessons a child can read words covering **49% of running Sindhi**;
after seven, **79%**; after twelve, **99%**.

The corpus is the Sindhi Language Authority's own publications, so it decides the
*letter order* well and the *example words* badly — its commonest words are
بريل، نشان، لفظ. So the letter order is kept and the words are written fresh for
children.

---

# Front matter — pages 1 to 4

| page | what is on it |
|---|---|
| 1 | **Title.** سنڌي بريل: پهريون ڪتاب — in print and in braille. Your name, Riaz's name, the date. |
| 2 | **A note for the teacher and the parent.** What a twin-vision book is, and that you do not need to know braille to teach from it. |
| 3 | **The cell.** The six dots and their numbers, large, in print. The same cell embossed beside it so a finger and an eye meet on the same object. |
| 4 | **How to read a line.** Left to right, always, in Sindhi as in every language. Where to put the finger, how to find the next line. |

---

# Part 1 — The letters. Pages 5 to 30

Thirteen lessons, two pages each. **All 52 letters.**

Page A of each lesson teaches four letters: the letter large in print, its cells
embossed, and one word for each. Page B is words and one sentence, using **only
letters already taught**.

The order is greedy against `tools/sindhi_words.txt`: at each step the letter
that makes the most new real words readable. Re-derived 21 August 2026 after the
ه/ھ correction, on a list that no longer counts the same word twice under two
spellings. ه is now first, where its frequency puts it, and ھ last, where a
letter that occurs only inside digraphs belongs.

| lesson | pages | letters | cells | words |
|---|---|---|---|---|
| 1 | 5–6 | ه ن ا ي | 125 · 1345 · 1 · 24 | هي · هن · نانا · ان |
| 2 | 7–8 | ج و ک ر | 245 · 2456 · 13-236 · 1235 | کير · اک · نو · هو |
| 3 | 9–10 | ت ب ل ء | 2345 · 12 · 123 · 3 | بابا · تارا · لال · رات |
| 4 | 11–12 | م س د ڪ | 134 · 234 · 145 · 13 | امان · ڪتاب · در · ڪرسي |
| 5 | 13–14 | ع پ ش ٿ | 12356 · 1234 · 146 · 1256 | پن · هٿ · پير · شهر |
| 6 | 15–16 | ڌ ڏ گ ڻ | 1236 · 34 · 1245 · 3456 | گل · وڻ · ڏند · پاڻي |
| 7 | 17–18 | ق ٻ ڙ آ | 12345 · 26 · 12456 · 345 | قلم · ٻلي · آسمان · ڪپڙا |
| 8 | 19–20 | ف خ ط ح | 124 · 1346 · 23456 · 156 | خوش · فرش · طوطو · حال |
| 9 | 21–22 | ص ٽ ظ ڳ | 12346 · 246 · 123456 · 13456 | ٽوپي · صاف · ڳوٺ · روٽي |
| 10 | 23–24 | چ ڊ ز ٺ | 14 · 346 · 1356 · 135 | چنڊ · ميز · اٺ · چار |
| 11 | 25–26 | غ ض ڇ ڀ | 126 · 1246 · 16 · 23 | ڀيڻ · باغ · ڇت · مڇي |
| 12 | 27–28 | ث ڄ ذ ڃ | 1456 · 356 · 2346 · 35 | وڃو · ڄاڻ · ذات · مثال |
| 13 | 29–30 | ڍ ڱ ڦ ھ | 256 · 2356 · 235 · 236 | ڍڳو · آڱر · ڦل · گھر |

**Coverage.** After lesson 2 a child can read 22% of the corpus by frequency,
after lesson 4 half of it, after lesson 7 four fifths. All 52 letters by
lesson 13.

**Why ھ is last, and what it costs.** ھ is not an ordinary letter. It occurs
only as the second half of a digraph — جھ گھ ڙھ لھ مھ نھ ڻھ, guide p.30 — so it
is taught last, and lesson 13 teaches it as what it is: the cell that turns گ
into گھ. The guide prints five of those seven inside whole words with the cells
beside them (جھرڪي، گھڙيال، پڙھ، ڳالھيون، سمھ), and those five are the lesson's
examples, which means the last page of Part 1 is backed by the committee's own
printed page.

The cost is that گھر، پڙھو، گھوڙو، جھاز، ڳاڙھو cannot appear before lesson 13,
which is why the reading lessons that use them come after Part 1 rather than
alongside it.

**Two words are still held back entirely.** ڏينهن and مينهن turn on نھ, the one
digraph the guide names but never prints inside a word. They wait for sheet 7.

# Part 2 — بارکڙي, the letters with their marks. Pages 31 to 34

The vowel marks, and the systematic table every Sindhi child learns.

| page | content |
|---|---|
| 31 | زبر، زير، پيش — the three marks, each its own cell |
| 32 | The table: a consonant against each mark, in a row a finger can follow |
| 33 | The same for a second and third consonant |
| 34 | Words that change meaning with the mark |

---

# Part 3 — Numbers. Pages 35 to 37

| page | content |
|---|---|
| 35 | **The number sign**, 3456. Why numbers need a sign and letters do not. |
| 36 | 1 to 9 and 0. The same cells as the first ten letters, which is the point. |
| 37 | Counting sentences, and things a child counts |

---

# Part 4 — The marks. Pages 38 to 39

| page | content |
|---|---|
| 38 | ٽِڪ (full stop) 256 · ڪاما (comma) 2 · سواليہ (question) 236 |
| 39 | **The one that never fully resolves.** At the end of a word, 236 is either the letter ھ or a question mark. Even the software cannot always tell. A child should be told this early, and told that guessing from the sentence is the right thing to do, not a failure. |

---

# Part 5 — Shapes. Pages 40 to 44

Embossed outlines a finger can follow, with the same shape printed in ink beside
it. **Already built and testable today**: `test-sheets/print-5-shapes.brf`.

| page | shape | name |
|---|---|---|
| 40 | square | چورس |
| 41 | triangle | ٽڪنڊو |
| 42 | circle | گول |
| 43 | rectangle | مستطيل |
| 44 | all four together, to compare | — |

Each page: the shape, its name, and one sentence using it.

---

# Part 6 — Reading. Pages 45 to 46

Two short passages using only letters taught, in the style of the grade 1 reader:
short sentences, concrete nouns, a thing that happens.

**These are the pages Riaz should read cold.** Everything before is drill;
these are reading.

---

# Back matter — pages 47 to 48

| page | content |
|---|---|
| 47 | **The whole alphabet**, all 52 letters with their cells, as a reference chart |
| 48 | Who made it, when, and from what. The 2016 committee, the Authority, and that the braille code is theirs and unaltered. |

---

## What I need from you

1. **The word lists checked** — all 52 words above, for spelling and for whether
   they suit a six-year-old.
2. **The sentences.** One per lesson, thirteen of them, plus the two reading
   passages. I will draft them against the letters-taught rule; they need the
   same checking.
3. **Riaz on the order.** He has taught blind children and I have not. If he
   wants ڪتاب earlier or ٻلي sooner, the order bends to him — the software
   recomputes what is readable and tells us what breaks.

## What I will build once those come back

- the source files, one per lesson
- the **PDF for your HP**, ink kept out of the braille zone
- the **`.brf` for the embosser**, dots kept out of the ink zone
- both from one source, on one grid, so they cannot drift apart
- the untaught-letter check, refusing any page that breaks the rule

---

**Digital implementation and verification by Safeer Ali Mirani, 2026**, in
partnership with **Riaz Hussain Memon**, member of the committee that authored
Standard Sindhi Braille, with **Mansoor Ali Kori**.
