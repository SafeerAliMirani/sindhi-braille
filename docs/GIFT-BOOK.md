# The guide book: what I think

**This is a better idea than the textbook, and I would drop the textbook route
for now and do this.** Here is why, what it needs, and the two facts about laser
printers that decide the layout.

---

## 1. Why this beats the Book 1 route

Everything that was blocking the textbook stops mattering:

| the textbook | your book |
|---|---|
| someone else's copyright, needs a letter | yours |
| 79 pages must be typed from pictures of pages | you write it; the software sets it |
| 265 pictures need a decision each | you choose figures that work by touch |
| what a syllabus decided in some other decade | what a beginner actually needs |

The critical path disappears. There is no waiting on the Textbook Board, no
typist, and no meeting to decide what happens to a picture of a goat.

And it is a better first book. A first book should be one you can finish, revise
and hand over. A textbook is a thing you inherit.

---

## 2. The part of your idea that is better than it looks

**Geometric shapes are the one kind of figure that survives braille.**

A photograph reduced to dots is noise under a finger. A square, a triangle, a
circle is *already* an outline, so nothing is lost by drawing it in dots. Your
instinct to put geometry in the book is the correct instinct, and it is not a
compromise.

**It is already built and it needs no special software.** `test-sheets/print-5-shapes.brf`
has four shapes with their Sindhi names underneath: چورس، ٽڪنڊو، گول، مستطيل.
Plain braille cells, so it prints on any embosser that reads a `.brf`.

The Everest-D V5 does have a real graphics mode, 500 dpi with dots placed to
0.05 mm, but reaching it needs Index's own software. Drawing on the braille grid
instead is coarser and works everywhere, today, with what you have.

**Emboss that sheet and give it to him without saying what is on it.** If he
names the four shapes unprompted, the book can have figures. `SHAPES-KEY.md`
asks the follow-up questions that matter: is the circle round or an egg, are the
corners sharp, does the sloping side feel like a line or like steps.

---

## 3. The laser printer: two facts that decide the layout

**Toner cracks when you emboss through it.** Laser toner is fused plastic on the
surface. Embossing deforms the paper sharply, and the toner splits along every
dot. So: **never emboss on top of a printed area.** Ink and dots get separate
zones on the page. Do that and there is no problem at all.

**The order is one-way and unforgiving.** Print first, emboss last. A sheet that
has been embossed must **never** go back through the laser printer: the fuser is
heat and pressure, which is exactly what flattens braille. If you print side one,
emboss, then print side two, you will destroy the braille and not find out until
you touch it.

So the sequence is fixed:

1. print **both** ink sides
2. emboss **once**, on one side only
3. bind

**Emboss one side, not both.** Dots raised on side A leave dimples on side B.
Double-sided braille has to interleave the two sets, and doing that under
double-sided ink means aligning four layers. For a book you are giving to
someone, single-sided braille is the robust choice. It costs paper and buys
certainty.

---

## 4. Paper, which is the fiddly part

Braille needs roughly **120 to 160 gsm** to hold dots. Ordinary 80 gsm will
emboss and then flatten under a reading finger, which makes good work look bad.

Heavy stock in a laser printer almost always means the **manual or bypass tray,
one sheet at a time**, and the automatic duplexer usually refuses it. Check your
model's media specification for the bypass tray before buying a ream.

Realistically, for one gift copy: heavy paper, bypass tray, **manual duplex** —
print the odd pages, flip the stack, print the even ones. For 40 pages that is
two passes of hand-feeding. Tedious for one evening, and completely fine.

**Test one sheet first**: print it, emboss it, press a finger firmly across the
dots, read it again. That tells you about the paper in five minutes rather than
after forty.

---

## 5. On the size: start smaller than 50

Thirty to fifty pages of original content is a real writing job, and a gift that
is finished beats one that is ambitious. **Sixteen to twenty pages, complete and
properly made**, is a better first edition, and the making of it will tell you
what the second should contain.

You can always add. You cannot easily rescue a half-finished book.

---

## 6. A shape for it, which you should overrule freely

You are the author. This is only to argue with:

1. **The cell** — the six dots and their numbers. One page.
2. **The alphabet** — the letters, a few to a page, each with its cells.
3. **بارکڙي** — the letters against the vowel marks, the systematic table.
4. **Numbers** — the number sign, the digits, then the lower digits.
5. **Punctuation** — and the cells that carry more than one meaning, which is
   where a learner gets confused and where this project has most to say.
6. **Shapes** — square, triangle, circle, rectangle, by touch, with their names.
7. **Words** — built only from letters already taught.
8. **Sentences** — the same rule.
9. **A short passage to finish on** — so the last page is reading, not drilling.

**One rule worth enforcing by software: never use a letter the book has not yet
taught.** That is the one thing a person cannot reliably keep across forty pages
and a machine can check in a second. I can build that check.

---

## 7. What I will build

**One source, two outputs, on the same grid.** That is the difference between a
book and a craft project with pages that do not line up:

- you write each page once, in the plain format
- it emits the **PDF for the HP**, with the ink kept out of the braille zone
- and the **`.brf` for the embosser**, with the dots kept out of the ink zone
- both from the same page model, so they cannot drift

Plus the untaught-letter check, and a teacher's copy showing Sindhi, braille and
dot numbers side by side.

**What I need from you: the outline, and the first page.** Once one page goes all
the way through — written, printed, embossed, read — the rest is repetition.

---

**A last thought.** A gift from you, in a code that had no software a month ago,
printed on a machine in Larkana on paper cut from a chart sheet. Put your name
and his in it, and the date. That book is the evidence, more than any test sheet.

---

**Digital implementation and verification by Safeer Ali Mirani, 2026**, in
partnership with **Riaz Hussain Memon**.
