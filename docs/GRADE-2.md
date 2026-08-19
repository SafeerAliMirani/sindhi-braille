# Grade 2 — the contractions, implemented

**13 August 2026.**

Grade 2 is contracted braille: common words written short. It is what real
Sindhi braille books use, and until now this project only had Grade 1.

## What the source is

Everything here comes from **مڪمل سنڌي بريل درجو II**, Riaz Hussain Memon's Grade 2
book, in the manuscript he supplied. Each table in it has three columns — نقطو
(the braille), اکر (the letter), لفظ (the word). The braille column did not
survive in the file, but the letter and the word did, and the braille is
recoverable from them: a contraction is the **series prefix followed by the
ordinary Grade 1 cell for that letter**.

## The system

Six series, plus a group of phrase abbreviations:

| section | prefix | entries |
|---|---|---|
| ڪل لفظي مخفف — a single letter standing alone as a word | none | 44 |
| نقطي پنج سان شروع ٿيندڙ مخفف | dot 5 | 44 |
| نقطي چار پنج سان شروع ٿيندڙ مخفف | dots 4-5 | 19 |
| نقطي چار پنج ڇهه سان شروع ٿيندڙ ڪل ۽ جز لفظي مخفف | dots 4-5-6 | 43 |
| نقطي ٽي چار پنج ڇهه سان شروع ٿيندڙ مخفف | dots 3-4-5-6 | 27 |
| نقطي ڇهه سان شروع ٿيندڙ مخفف | dot 6 | 9 |
| سنڌي اختصار — Sindhi abbreviations | none | 51 |

**237 contractions in total**, of which 32 stand for a phrase rather than a
single word — plus **six ڳانڊڙا groups** (below) that are written inside a word.

Examples:

| written | means | cells |
|---|---|---|
| ا | اسين | 1 |
| ڀ | ڀلو | 23 |
| dot 5 + آ | آهي | 5 · 345 |
| dot 6 + ت | تيئن ته | 6 · 2345 |
| ا ل ت | البته | 1 · 123 · 2345 |

Note the last one: **the six prefix series are Louis Braille's seventh line** —
{4, 5, 6, 45, 46, 56, 456}. Six of those seven head a contraction series here.
That is why those cells never appear in ordinary Grade 1 Sindhi text.

## What is built

- **`official-code/grade2_contractions.csv`** — the full list: series, prefix,
  letter, braille, word, and whether it is a phrase.
- **`official-code/grade2_groups.csv`** — the six ڳانڊڙا groups.
- **`brailleTables/sd-pk-g2.ctb`** — the liblouis table. Includes the Grade 1
  table and adds 205 `word` rules and 6 `midendword` rules. Compiles clean.
- **`tools/sindhi_braille.py --grade2`** — the reference translator, which also
  handles the 32 phrase contractions.

**Cross-checked:** the two implementations agree cell for cell on every
contraction, phrase and group.

```
اسين ٿو وڃون. البته توهان ڀلو آهي.
⠁ ⠳ ⠺⠔⠺⠝⠲ ⠁⠇⠞ ⠞ ⠆ ⠐⠜⠲
```

Thirty-four cells become twelve.

**That line is not from the book and it is not natural Sindhi.** It was built by
chaining together words that happen to have contractions, so that one line could
show several series at once. It demonstrates the mechanism and nothing else. A
sentence somebody would actually write contracts less: *سنڌي ٻولي هڪ شاهوڪار ٻولي
آهي.* goes from 25 cells to 19. **A natural sentence from Riaz Hussain Memon or
Mansoor Ali Kori should replace it**, here and on line 9 of the Grade 2 print
sheet.

## The two questions that were open — both now answered

### 1. Which of the dots 4-5-6 entries are partial-word?

The section is headed «ڪل ۽ جز لفظي» — whole **and** part word — so some entries
should apply inside a longer word. I tested all 42 against a Sindhi corpus of
2,704 word types drawn from the committee's own publications, asking of each: is
this a complete standalone word, or a fragment?

**Every one of the 42 is a complete Sindhi word.** Thirty occur as standalone
tokens in the corpus (شروع، جنهن، صورت، ڇڏي، پيار، دعوت، خراب، اڳواڻ…), and the
other twelve — آڻين، ڀائين، تڪليف، ٿڪاوٽ، ٺهراءُ، ڦيرائين، ڪماءِ، گنجائش، ڳجهه،
منجهه، ويڪر، همدرد — are plainly complete words too. **Not one is a fragment.**

So applying all 42 as whole-word contractions is not a compromise: it is correct
for every entry in the section. The «جز» half of the heading has no entry that
needs it.

### 2. The ڳانڊڙا sections

They are on book pages 15 and 17, and both pages are in hand.
**Both tables are printed almost entirely blank.** Each has around thirty rows
with a braille cell and a letter, and only **three** of them carry a group:

| page | prefix | letter | group |
|---|---|---|---|
| 15 | dots 5-6 | ب | ياب |
| 15 | dots 5-6 | د | يند |
| 15 | dots 5-6 | ر | ارا |
| 17 | dots 4-6 | ب | واب |
| 17 | dots 4-6 | د | باد |
| 17 | dots 4-6 | ر | وڪر |

That is everything the book gives. It was not that the material was missing from
the manuscript — the printed pages themselves were never filled in.

All six are implemented, as **word-medial and word-final only**, which is exactly
what the heading «لفظن جا وچان ۽ پويان ڳانڊڙا» specifies:

```
آباد    → ⠜⠨⠙      آ + [dots 4-6 · باد]        4 cells → 3
آزارا   → ⠜⠵⠰⠗     آ + ز + [dots 5-6 · ارا]    5 cells → 4
وڪر    → ⠺⠅⠗      unchanged — a group is never written word-initially
```

## What is still not settled

**The placement rules for the six series are not stated anywhere in the material.**
Every Grade 2 code has rules about when a contraction may be used, and those rules
are not written down here. Since all 42 dots-4-5-6 entries turned out to be whole
words, and the ڳانڊڙا have their position given in their own heading, the practical
effect of this gap is now small — but it is not zero, and a transcriber reading a
real book may still find a case the tables do not cover.

There is **no longer any divergence** between the two implementations. ۾ used to
be one: it has a Grade 2 contraction (م), but the Grade 1 liblouis table spelled
it out as م ي ن, and a rule an include has already defined cannot be overridden.
The shared rules now live in **`sd-pk-g1-core.uti`**, which both tables include
and which states nothing about ۾ — so `sd-pk-g1.utb` spells it out and
`sd-pk-g2.ctb` contracts it, each saying so for itself. That is also how the
liblouis project organises tables that share a core.

## Reading contracted braille back

Back-translation is implemented, because reading a contracted book back is
exactly what a transcriber needs: `back(cells, grade2=True)`, `--grade2 --back`
on the command line, or the **Grade 2** switch on the website.

It has to be asked for. Every contraction is also a perfectly ordinary Grade 1
spelling of something else — ا is both the letter and the word اسين — so a
Grade 1 book read with `grade2=True` would come out as nonsense.

**238 of 243 contractions, phrases and groups survive the round trip.** The five
that do not are the five places where the book gives one pair of cells to two
different words:

| cells | and it could be |
|---|---|
| 1245 | گرمي · گرم |
| 3456-12346 | صحتمند · صحتمندي |
| 245-134 | جملو · جملي |
| 134-1235-2345 | مرتبو · مرتبا |
| 245-23456 | جهڙي طرح · جنهن طرف |

Reading takes the first of each pair — the book's own order — and every
candidate is kept in `G2AMBIG`, so a transcriber can be shown the collision
instead of a silent guess.

`sd-pk-g2.ctb` still does not back-translate; use the reference translator.

## The collision worth knowing about

Dots 3-4-5-6 now carry three meanings: the letter **ڻ**, the **number sign**, and
one of the Grade 2 series prefixes. The first two are separated by position — no
Sindhi word begins with ڻ, verified over 21,445 words. The third is separated in
practice because a series prefix is followed by a letter and the number sign by a
digit. It is worth confirming with Riaz that this is how a reader resolves it too.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon** — blind teacher, President of
the Pakistan Association of the Blind (Sindh), and a member of the committee that
authored the code. The contractions are his book's; they are not altered here.


With **Mansoor Ali Kori**, who works with Riaz Hussain Memon on the composing and has taken part in the meetings throughout.