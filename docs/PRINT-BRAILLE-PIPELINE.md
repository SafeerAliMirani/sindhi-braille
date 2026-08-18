# Making print-braille pages — colour from Katib Press, braille from the Everest

A design for producing pages that a sighted child and a blind child can read
together: colour artwork printed normally, braille embossed on the same sheet.

**The order is fixed: colour first, braille second.** A printer's rollers flatten
dots that are already there.

---

## The one thing to settle before anything else: paper size

Standard Sindhi braille is **40 cells by 25 lines**. That block measures:

| | needed |
|---|---|
| width | 40 cells × 6.2 mm = **246 mm** |
| height | 25 lines × 10 mm = **246 mm** |
| plus margins | about **280 × 292 mm** of paper |

**A4 is 210 × 297 mm. It is too narrow.** On A4 you fit **28 cells**, not 40.

So there is a choice, and it has to be made before Katib Press prints anything:

**Option A — proper braille paper, 280 × 292 mm.** Keeps the full 40-cell line, so
the braille matches every other Sindhi braille book. Katib Press must be able to
feed a sheet slightly wider and shorter than A4. If their press takes A3
(297 × 420 mm) they can print two-up and trim.

**Option B — A4, 28 cells per line.** Much easier for a local press, and A4
braille paper is easier to buy. The cost is that lines are shorter than the
national standard, so the same text takes more pages. Fine for picture books and
worksheets; not right for a textbook that must match others.

*Recommendation: A4 at 28 cells for the first experiments, then braille paper
once the process works.* Our translator takes `--width 28`.

---

## The pipeline

**1. Write the Sindhi text.** Ordinary UTF-8 text file.

**2. Make the braille.**
```
python tools\sindhi_braille.py chapter.txt -o chapter.brf --width 28
```

**3. Make the layout guide.**
```
python tools\braille_layout.py chapter.brf -o guide.pdf --paper 210x297 --cols 28
```
This draws, at true size, exactly where every dot will land, with the ink-free
bands marked in red and the leading edge marked in blue.

**4. Design the colour page on top of the guide.** Give the PDF to Katib Press's
designer as a background layer. They place pictures and print text in the empty
space between the red bands. Rules for them:

- **nothing printed inside a red band** — ink stiffens paper and the dots crack
- keep heavy solid colour away from the braille area generally
- the blue arrow edge must stay the top of the sheet

**5. Katib Press prints** on braille paper we supply, single-sided.

**6. Feed the printed sheets into the Everest** and emboss the `.brf`. Leading
edge first, same orientation every time.

**7. Check** — see the test below.

---

## First test: one sheet, not a book

Do not start with a chapter. Print **20 copies of one page**: a picture at the
top, and a braille caption in the lower third.

That single sheet tests everything at once:

| what it tests | what failure looks like |
|---|---|
| paper weight | dots collapse, or the sheet tears |
| feeding | the Everest jams or skews |
| registration | braille drifts off its band |
| ink and embossing | dots crack where they cross printed colour |
| readability | Riaz cannot read the caption cleanly |

**Riaz reads it. He is the test.** If he reads the caption without hesitating,
the pipeline works.

Twenty sheets is enough to see whether drift accumulates and cheap enough to
throw away.

---

## Questions for Katib Press

- Can you print on paper we bring, at 280 × 292 mm — or must we use A4?
- Can you keep the top and left margins accurate to about a millimetre?
- Single-sided, and can you keep the sheets flat and unfolded afterwards?
- Price for 20 sheets, and for 500?

---

## What not to ask them for

**Do not let the press make the braille.** They will probably offer — they emboss
wedding cards, and it sounds like the same job. It is not. Readable braille has
fixed geometry: 2.5 mm between dots, 6.2 mm between cells, 10 mm between lines,
and a specific dot height and roundness. A press die produces decorative relief
that looks like braille in a photograph and cannot be read by a finger.

The press does colour. The Everest does braille. Keep that line clean.

---

## Later: tactile pictures

The raised outlines around shapes in the books Riaz showed you are a different
thing again — a picture you can feel, not text. A press with blind-embossing
dies can make those beautifully, better than an embosser can, but each design
needs its own die.

So the eventual division of labour is probably:

- **Katib Press** — colour, and raised picture outlines
- **The Everest** — braille text

That is a decision for a real book, not a test page.
