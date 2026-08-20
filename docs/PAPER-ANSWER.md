# The paper: the answer, and the one thing still to measure

**22 × 28 inch sheet, cut to about 11 × 12, with 4 or 5 cells of binding margin
on the left.** Here is what that gives, and one change worth making.

---

## 1. Cut 11 × 14, not 11 × 12

**22 × 28 divides exactly into four pieces of 11 × 14 inches, with nothing left
over.** They are cutting 11 × 12 today, which leaves a 22 × 4 inch strip as
waste on every sheet.

The width is the same either way, so **no line gets shorter**. The gain is in
the height:

| cut | cells per line (4-cell binding) | lines per page |
|---|---|---|
| 11 × 12 in, as now | 38 | 28 |
| **11 × 14 in, true quarter** | **38** | **33** |

Five more lines on every page, and no offcut. Over a book that is roughly one
page in six saved, on paper they had already bought.

**This is a suggestion, not a correction.** There may be a reason they cut 12:
an existing binding size, a folder or shelf it has to fit, or simply what the
cutter is set to. Riaz and the press know that and I do not. The point is only
that 14 costs nothing at the machine and saves the strip, so it is worth asking
the question before the next batch is cut.

---

### It fits the machine, which I checked rather than assumed

The Everest-D V5 takes cut sheets of **130 to 297 mm wide** and **120 to 590 mm
long**. Both cuts are inside that:

| cut | as the machine sees it | in spec? |
|---|---|---|
| 11 × 12 in | 279 mm wide × 305 mm long | yes |
| **11 × 14 in** | **279 mm wide × 356 mm long** | **yes** |

So changing from 12 to 14 costs nothing at the machine. It is the same width
being fed, only a longer sheet, and 356 mm is well inside the 590 mm the feeder
takes.

It also confirms 11 inches is the right way round. Cutting the sheet the other
way would give pieces 14 inches wide, and 14 in is 356 mm, which is over the
297 mm the machine can accept. The 22 inch dimension has to be the one that is
halved.

**This assumes the press's machine is the Everest-D V5.** If it is a different
model, send me the name and I will check its limits before anyone cuts anything.

---

## 2. The numbers at 11 inches wide

| binding margin | cells per line |
|---|---|
| none | 42 |
| 3 cells | 39 |
| **4 cells** | **38** |
| 5 cells | 37 |

So the file for this press should be built at **38 cells**, with the machine's
left margin set to 4.

His instinct to specify the margin in cells rather than millimetres is the right
one. A binding margin in cells is a whole number the press simply does not use,
and it survives being handed to a different machine. A margin in millimetres has
to be converted, and conversions are where the August fault came from.

---

## 3. Do not take my word for the 38

**These numbers rest on an assumption I made up: that the machine cannot emboss
within 8 mm of the paper edge.** That border belongs to the embosser, not to the
braille standard, and I have never seen their machine.

So there is a new sheet: **`test-sheets/print-0-ruler.brf`**. Emboss it once, on
the paper they have actually cut, with the binding margin already set.

It prints eight bars of solid cells, one per line, at 44, 42, 40, 38, 36, 34, 32
and 30 cells. **The answer is the widest bar that comes out as a single line.**
A bar too wide for the paper does not run off the edge, it wraps, and the
leftover cells land underneath as a short stub. One long line with a stub under
it means too wide. A clean line with nothing under it means it fits.

Then two lines that count in fives, four solid cells and a gap, so a blind reader
can count the cells directly rather than being told.

`test-sheets/RULER-KEY.md` explains it in full. It also asks two other things off
the same sheet: how many lines fit before the page breaks, and whether the dots
survive being pressed firmly. 150 gsm should hold them, but that is worth
knowing on one sheet rather than on a hundred.

**Send me the widest bar that fits and the line count, and I will rebuild every
test sheet at exactly that size.**

---

## 4. Why this matters more than it sounds

A `.brf` file has no page size inside it. It is a fixed number of cells per line,
and nothing else. If that number is larger than the paper allows, the machine
breaks the lines itself, wherever they happen to fall, in the middle of words.

That is exactly what happened on 15 August. The braille was correct and the page
was unreadable, and no amount of checking the code would have found it. It was
found by a man holding the paper.

So the order is: emboss the ruler, get the number, build at that number, and only
then print the ten-page test.

---

**Digital implementation and verification by Safeer Ali Mirani, 2026**, in
partnership with **Riaz Hussain Memon**.
