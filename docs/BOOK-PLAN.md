# The text-only Book 1: my suggestion for tomorrow

**Short answer: yes, do it. One decision inside it matters more than all the
rest, and it costs nothing today.**

---

## 1. Keep the printed book's page numbers. This is the whole thing.

If the braille edition carries the printed book's page numbers, then when the
figures are added later, **nothing is re-typed and nothing is re-numbered**. The
colour edition drops the pictures into pages that already exist.

If it does not, the second edition is a second book, and all the typing is done
twice.

So every page of the braille says which printed page it is, and the teacher's
copy shows both. This is already built. It costs three cells a page.

That single decision is why Riaz's plan works. Without it, a text-only edition is
a dead end; with it, it is the first half of the finished book.

---

## 2. Say what the book is, accurately

It is **the reading text of Sindhi Book 1**, not *Sindhi Book 1 in braille*.

If it goes to the Education Department described as the class 1 textbook, someone
will open it, find an exercise that cannot be done, and doubt everything else in
it. Described accurately, it is a strong first volume and nobody is surprised by
anything.

The title page should say so plainly, in Sindhi, and give the date and the print
edition it was made from.

---

## 3. Mark every picture where it stood. Never drop one silently.

A page that quietly leaves out exercise 4 teaches a child that the book does not
make sense, and they have no way to find out otherwise. A page that says
**تصوير** in place of the picture tells the truth: something is here that I
cannot reach, and I can ask about it.

Three cells. It also keeps the page shaped like the printed page, which is what
makes point 1 work.

**And exercises keep their numbers.** If exercise 4 needs a picture and exercise
5 does not, exercise 5 is still called 5. A blind child and a sighted child then
sit in the same classroom, on the same exercise number, out of two different
books. That is worth more than a tidy sequence.

---

## 4. What we already know about the book

From the file itself, counted rather than guessed:

| | |
|---|---|
| pages | 79 |
| pictures | 265 |
| **pages carrying no picture at all** | **21** |

**Those 21 pages need no decision from anybody.** They are pure text and they
convert exactly. If tomorrow needs a demonstration rather than a debate, those
are the pages to type first.

---

## 5. The colour-then-emboss edition: one thing to settle now

It is later, but it constrains the layout today, so it is worth five minutes
tomorrow.

- **Emboss after printing, never before.** A dot is displaced paper. Run an
  embossed sheet through a press and the rollers flatten it. Ink first, dots
  last, always.
- **Reserve a braille zone on the page.** The braille needs fixed lines it can
  rely on. The figures go where the braille is not. If that is decided now, the
  text-only edition is already laid out correctly for the colour one.
- **Single-sided braille for the combined edition.** Double-sided braille with
  double-sided colour has to align on both faces at once, and the katib press is
  not going to hit that reliably. Single-sided doubles the paper and removes the
  problem.

---

## 6. What actually blocks it: the typing

Unchanged, and it is the only thing on the critical path. The pages of the file
we have are pictures of pages, so the Sindhi has to be keyed in by someone who
reads Sindhi.

**The format is ready and a typist can start tomorrow.** `book/FORMAT.md` is
written for someone who reads Sindhi and knows no braille. It is plain text with
five markers: the page number, a heading, a figure, an exercise, a blank. Nothing
else to learn.

**Ask for it lesson by lesson, not all at once.** Each lesson gets built and
checked as it arrives. A format mistake found in lesson 2 costs ten minutes; the
same mistake found after 79 pages costs the whole book.

---

## 7. The order I would go in

1. **Emboss the ruler sheet.** Settles the width. One page, tomorrow.
2. **Type lesson 1.** One lesson, by one person, in the format.
3. **Build and emboss it.** `python tools/make_book.py book --width N`
4. **Riaz reads that one page cold.** Any problem with the format shows up here,
   while it costs nothing.
5. **Then the other 78 pages**, lesson by lesson.

Steps 1 to 4 could be done inside a week. **The first embossed page of a real
Sindhi book, from this software, is days away, not months.**

---

## 8. On the Department

Do not send the book alone, and do not send the test alone.

The book shows they can produce one. The ten-page test with a score shows the
code underneath it is right. Together they answer the only two questions a
department actually has: does it work, and can you do it at scale.

---

**Digital implementation and verification by Safeer Ali Mirani, 2026**, in
partnership with **Riaz Hussain Memon**, with **Mansoor Ali Kori**.
