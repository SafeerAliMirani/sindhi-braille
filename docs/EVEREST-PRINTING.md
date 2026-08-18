# Writing braille on a computer, and printing it on the Everest-D V5

Two separate questions. Answering them in the wrong order is the usual mistake:
**you do not need to know braille to produce braille.**

---

## Part 1 — How people write braille on a computer

There are three ways, for three different people. All three end in the same
place: a `.brf` file.

### A. Type Sindhi normally, let the software translate — *the main path*

This is what a sighted teacher, a composer at the press, or you will do. Nobody
types braille. You type Sindhi in an ordinary Sindhi keyboard layout, and the
translator turns it into braille.

- **Windows:** Settings → Time & Language → Language → Add a language → **Sindhi
  (Pakistan)**. That gives a proper Sindhi keyboard. Phonetic layouts also exist
  if the standard one is unfamiliar.
- **Then:** paste the text into our translator (the website, or
  `python tools/sindhi_braille.py book.txt -o book.brf`) and download the `.brf`.

This is exactly what the DEPD Braille Press composer does today with Duxbury —
except Duxbury has no Sindhi table, so he has been working around it. Our table
is what removes the workaround.

### B. Six-key (Perkins) entry — *for someone who knows braille*

A blind user who reads braille does not want to type Sindhi letters; they want to
type **dots**. The standard way is to turn the ordinary computer keyboard into a
braille writer:

```
   S  D  F        J  K  L
  dot3 dot2 dot1  dot4 dot5 dot6
```

You press the keys for one cell **together, as a chord**, and release. Space bar
is the space. This is how a Perkins Brailler works, and every braille input tool
uses the same six keys.

Software that already does this: Duxbury, BrailleBlaster, and NVDA when a braille
display is attached. **This is the one thing our website does not have yet, and
it is the most valuable feature to add next** — it would let a blind Sindhi
teacher write a worksheet on any ordinary PC, with no special hardware, and get
back both the braille file and the Sindhi text.

### C. A refreshable braille display — *the best experience, if the hardware exists*

The user types on the display's own Perkins keys and reads the result under their
fingers. NVDA drives the display, and NVDA gets its braille from **liblouis** —
which is precisely why getting `sd-pk-g1.utb` accepted upstream matters. Until
Sindhi is in liblouis, a braille display in Pakistan cannot show Sindhi properly.

Realistically, most blind users in Sindh have an ordinary computer and no display.
So the honest near-term answer is **B for writing** and speech for reading.

---

## Part 2 — Printing on the Index Everest-D V5

### What the machine expects

The Everest-D V5 is a double-sided (interpoint) embosser. It reads a **`.brf`**
file — plain ASCII, one character per braille cell, lines ended with CR LF and
pages with a form feed. That is exactly what our translator writes.

Nothing about the file is specific to this machine. A `.brf` is the standard
braille interchange format and every embosser reads it, so the same three files
go to a Braillo, a ViewPlus, a Basic-D or the press's machine unchanged. Only the
menu wording below is Index's.

**The one thing that must be right:** a `.brf` is not dots, it is *letters that
stand for dots*. The embosser converts them using its own table. Index documents
`.brf` as printing with the **MIT legacy braille table**, which is the standard
North American Braille ASCII mapping — the same one our `cell_to_ascii()` uses.
If those two agree, every dot lands where we intend. **If they disagree, every
cell on the page is wrong in the same systematic way.**

Do not assume they agree. Prove it with the test sheet below, before printing
anything that matters.

### Sending a file — five ways, easiest first

1. **USB memory stick.** Copy the `.brf` onto a stick, plug it into the embosser,
   use the arrow keys to select the file, press **OK**. No computer involved.
   This is the most reliable way to make the first test print.
2. **Index-direct-Braille (idB).** Install Index's software on Windows, then
   right-click the file → Print.
3. **The printer driver.** Install it and print from any application.
4. **Network / BrailleApp.** If the embosser is on the wired or Wi-Fi network.
5. **Direct USB port.**

### Paper and page size — decide this first

Braille geometry is fixed, so the paper decides the line length:

| Paper | Max cells per line |
|---|---|
| A4 (210 mm wide) | **28** |
| Letter (216 mm) | 29 |
| 11″ tractor braille paper (280 mm) | 40 — the international page |

Our default output is 40 × 25, the international page. **That does not fit A4.**
For A4 you must set the line width to 28, which is what
`tools/sindhi_braille.py --width 28` does and what the test sheet below uses.

Get proper braille paper if you can — it is heavier (about 120–160 gsm) and holds
the dots. Ordinary photocopy paper will emboss but the dots flatten quickly under
fingers, which will make a good code look bad.

### First run — the order to do it in

1. **Hammer test.** Hold **HELP + ON**. This prints the embosser's own test page
   and proves every pin fires. If a dot is missing here, it is the machine, not
   the file.
2. **Set the layout.** Menu → choose paper size, set characters per line and lines
   per page, and choose single or double sided. Start **single sided** — interpoint
   is harder to read and harder to debug.
3. **Print sheet 1** (`test-sheets/print-1-grade1.brf`), from a USB stick.
   22 lines, 28 cells, one A4 page. Then sheet 2 (`print-2-grade2.brf`) and
   sheet 3 (`print-3-poetry-maths-foreign.brf`). All three are one page each and
   all three already fit A4, so the layout is set once and does not change
   between them.
4. **Have Riaz read them by touch, line by line**, against
   `test-sheets/ANSWER-KEY.md` — and read them to him cold, without telling him
   what a line is meant to say. Do not read the paper yourself: you cannot check
   braille by eye, and the whole point is that a reader confirms it.
5. Only when every line is right, print something real.

### If the test sheet comes back wrong

- **Every line wrong, in the same way** → the ASCII table. The embosser's braille
  table is not the one we assumed. Fix it in the embosser's layout settings, or
  re-map in software; do not touch the code.
- **Lines cut off** → line width is longer than the paper allows. Set 28 for A4.
- **A dot missing in the same position everywhere** → a hammer. Run the hammer test.
- **One line wrong, the rest right** → that is a real finding about the code.
  Write it down and send it to me.

---

## The three test sheets

All three are within 28 cells and fit A4. Each line tests one thing, in increasing
order of difficulty. The full line-by-line answer key is in
**`test-sheets/ANSWER-KEY.md`** — print that for yourself, not for Riaz.

**Sheet 1 — `print-1-grade1.brf`, Grade 1, 22 lines.** The alphabet in two
halves, the digits, the punctuation, a plain sentence, a question, the
aspirates, words ending in ھ, the letter ک, the repeated-word rule, a number in
a sentence, fractions, arithmetic, Roman numerals, exercise labels, a religious
abbreviation, and a year with ع.

**Sheet 2 — `print-2-grade2.brf`, Grade 2, 9 lines.** Contractions from each of
the six series, the phrase abbreviations, and the ڳانڊڙا groups written inside a
word.

**Sheet 3 — `print-3-poetry-maths-foreign.brf`, 19 lines.** The three areas that
had never been checked on paper: arithmetic (the guide's four sums, fractions,
decimals, per cent, brackets and braces, Roman numerals), English and Urdu words
inside Sindhi, and a bait set in verse marks with the pen-name. Line 3 and lines
17-19 are the ones to ask him about; the answer key says why.

Lines 3-4, 12, 13 and 16 of sheet 1 are the ones that matter most — the second
half of the alphabet and line 13 carry **ک**, the one letter written in two
cells (ڪ then ھ); line 12 is the ھ-ending case, which is where a two-cell letter
could be misread; line 16 is the fraction rule.

---

## The honest caveat

The exact menu names above come from Index's own V5 documentation, not from
having stood in front of your machine. The embosser is still unopened. Treat the
sequence as correct in shape and confirm the wording against the printed quick
guide in the box — and if anything differs, tell me and I will correct this file.

Sources: [Index Everest-D V5 quick print guide](https://downloads.indexbraille.com/Manuals/Index%20Everest-D%20V5/English/Quick%20print%20guide%20-%20Index%20Everest-D%20V5%20-%20English%20-%20Type-1366%20-%20FW2.pdf) ·
[Index V5 printer manual](https://www.edvisionservices.org/Manuals/Basic-D_V5.pdf) ·
[Duxbury: importing .brf files](https://www.duxburysystems.com/documentation/dbtmac12.3/Content/miscellaneous/brf_files.htm)
