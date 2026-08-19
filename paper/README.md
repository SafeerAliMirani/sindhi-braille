# The paper

`main.tex` is the draft. Everything numeric in it comes from `generated.tex`,
which is written by `make_paper_tables.py` out of the same modules the software
runs on. **Do not edit `generated.tex`.** If a cell changes in
`tools/sindhi_braille.py`, regenerate and the paper changes with it:

```
cd paper
python make_paper_tables.py
```

It prints the figures it wrote, and it runs the full verification suite on the
way past, so a number cannot get into the paper unless the suite produced it.

## Building it

**Compile with XeLaTeX.** On Overleaf: Menu, then Compiler, then XeLaTeX. The
Sindhi will not typeset under pdfLaTeX.

Upload `main.tex` and `generated.tex` together. Nothing else is needed; there is
no bibliography yet.

**The Sindhi face.** The preamble asks for *Noto Naskh Arabic*. If Overleaf does
not have it, change the one line

```latex
\newfontfamily\sdfont{Noto Naskh Arabic}[Script=Arabic]
```

to *Scheherazade New* or *Amiri*, both of which Overleaf carries.

**The braille.** Every cell in the paper is drawn by TikZ from its dot numbers,
using the `\bcell` macro, so it needs no braille font and prints correctly
anywhere. `\bcell{1,3}` is dots 1 and 3. The faint circles are the unraised
positions, which is how the committee's own printed guide shows them.

## Fitting it to a venue

The draft is written neutrally so it can be cut to a conference or extended for
a journal. If it has to lose pages, the order to cut in is:

1. The alphabet table (\S5) becomes an appendix or a reference to the repository.
2. The shared-cell table (\S6) keeps only the rows with three or more readings.
3. \S4.4 and the Grade 2 subsection compress to a paragraph each.

The parts that should not be cut are the shared-cell analysis, the verification
design, and the reading of 15 August 2026, because they are what the paper is
for.

## Still to do

- No related work section yet. It needs a survey of braille codes implemented
  for Perso-Arabic scripts, and of `liblouis` table development practice.
- No bibliography. The standard guide, the two teaching books, the `liblouis`
  tables used for the cross-code comparison and the UEB rules for arithmetic all
  need proper entries.
- The four open questions on the decision sheet should be resolved, or reported
  as still open at the date of submission.
- A second reader would change what the limitations section has to concede.
