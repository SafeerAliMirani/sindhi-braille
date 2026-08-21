# Sheet 7 — ه or ھ

Six words, each printed twice: once with **ه** (dots 1-2-5) and once with
**ھ** (dots 2-3-6). Same label letter on both lines of a pair.

| pair | first line | second line |
|---|---|---|
| ا. | گهر | گھر |
| ب. | آهي | آھي |
| ج. | پڙهان | پڙھان |
| د. | هي | ھي |
| ه. | ته | تھ |
| و. | پنهنجو | پنھنجو |

**Read him both lines of a pair and ask which one is the word.** Do not tell him
they differ by one cell, and do not tell him which is which.

## What we already know, and what is left

The guide settles the plain case itself, because its worked examples print the
dots beside the word: page 45 sets هن as `125 1345`, page 32 sets هڪ as `125 13`
and آهي as `345 125 24`. So **ه, 1-2-5, is the ordinary he** — pairs د، ه and ب
below are controls, and we expect him to pick the first line each time.

What the guide does not settle is where the **aspirate digraph** starts. Page 30
prints جھ، گھ، ڙھ، لھ، مھ، نھ، ڻھ and the words پڙھ، سمھ، ڳالھيون, all with
2-3-6. That covers گهر/گھر and پڙهان/پڙھان and پنهنجو/پنھنجو, which are pairs
ا، ج and و, and it is the real question on this sheet.

It is not a small number of words. `tools/sindhi_words.txt` carries 262 words in
both spellings with near-identical frequencies, which is one body of text counted
twice under two conventions, and the list cannot be merged until this is
answered. Whichever way it goes, every occurrence in the primer follows.

## What we need from him

1. Which cell belongs in each of the six words.
2. Whether there is a rule, or whether it is word by word. If there is a rule,
   the software can enforce it and the typist never has to think about it again.

---

**Digital implementation by Safeer Ali Mirani, 2026**, in partnership with
Riaz Hussain Memon.
