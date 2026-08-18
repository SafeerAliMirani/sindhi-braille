# The website — plan, and what the prototype already does

**13 August 2026.**

## What it is for

Three different audiences, one site. Getting this straight decides the layout.

| Who | What they need in the first 30 seconds |
|---|---|
| A Sindhi teacher or parent | Type Sindhi, get braille, download a file the embosser will print |
| The liblouis / Duxbury maintainers | Is this the code the community actually uses, and can I see the evidence? |
| A reviewer of the paper | Provenance, method, measured results, and an honest statement of limits |

The prototype puts the translator first because the first audience is the one the
work is *for*. The evidence sections sit under it, in the order the other two
audiences will read them.

## Prior art we looked at

- **liblouis.io** — the reference for how an open braille project presents itself:
  a "Try it" page, tables, documentation, downloads. Plain, technical, credible.
- **brailleblaster.org** (American Printing House) — the production tool: a full
  transcription application, not a demo.
- **braille-translator.com**, **text2braille.com**, **dcode.fr/braille-alphabet** —
  consumer converters. Fast, no provenance, no evidence. Useful as a warning:
  a converter with no stated authority is not something a school will trust.

What none of them do, and what this site must do, is show *whose* code it is and
*how it was checked*. That is the whole argument for adopting it.

---

## The prototype — built, working

One self-contained HTML file, no build step, no server, no network. Open it and
it runs. The translator is a direct port of `tools/sindhi_braille.py`, with the
tables generated from that file so the two cannot drift apart.

**Verified:** the browser engine reproduces the same **69 of 69** worked examples
printed in the standard guide as the Python does.

Sections, in order:

1. **Try it.** Sindhi in, braille out — live. Output shown three ways: Unicode
   braille, dot numbers, and a downloadable `.brf` for the Everest. Seven sample
   sentences covering prose, a question, a number, a fraction, a sum, a religious
   abbreviation and a repeated word. A back-translation pane underneath.
2. **The 52 letters**, each drawn as a real braille cell — raised dots solid,
   unraised faint, exactly as the committee's own printed font shows them.
3. **How a fraction is written** — the upper/lower digit rule, drawn.
4. **63 cells, 89 things to say** — every cell that carries more than one meaning,
   with its readings and the rule that decides between them.
5. **How we know it is right** — 69/69, 99.94%, 51/52, and the paragraph saying
   what that does *not* prove.
6. **What is not settled** — the ک question, the guide's two self-contradictions,
   Grade 2, one reader.

English and Sindhi throughout, with a toggle. Light and dark.

---

## What the prototype does not do yet

| Gap | Why it matters | Effort |
|---|---|---|
| Back-translation is simplified in the browser | The full word-list disambiguation is not loaded, so a final ھ/؟ can read wrong | small — ship `sindhi_words.txt` compressed |
| No page layout control | The `.brf` is not paginated to 40×25 | small |
| No screen-reader pass | The primary audience includes blind users; the page must be navigable by NVDA | **do before launch** |
| No Grade 2 | Contractions are decoded but unimplemented | large |
| No audio | eSpeak NG Sindhi is poor; a separate problem | out of scope for launch |
| Not hosted | | trivial — GitHub Pages |

**The screen-reader pass is not optional.** A site about braille that a blind
teacher cannot use would be an embarrassment. Before launch: test with NVDA end
to end, label every control, make the braille output readable as text, and make
the whole translator usable from the keyboard alone.

---

## Sequence to launch

**Now → printing (next week).** The site stays private. Printing is the priority;
nothing on the site changes the print run.

**After a successful print.** Add a short page showing the printed sheets and what
Riaz reported reading. That is the proof that turns a demo into a result.

**Then, in order:**

1. **GitHub.** Public repository: the translator, the liblouis table and its test
   suite, `verify_guide.py`, the specification in English and Sindhi. Licence
   LGPL for the table (to match liblouis) and a permissive licence for the tools.
   Credit the committee on the front page, Riaz first among the collaborators.
2. **The site,** on GitHub Pages, from the same repository.
3. **liblouis.** A pull request adding `sd-pk-g1.utb`. Do this only once the open
   questions are closed — the maintainers will ask whether the community uses this
   code, and the answer must be a printed textbook and a committee member, not a
   claim.
4. **Duxbury.** Approach with the table and the printed evidence. Duxbury is what
   the DEPD Braille Press already uses, so a Sindhi table there reaches the actual
   production chain faster than anything else we can do.
5. **The paper.** Only after a successful print. Riaz Hussain Memon as first or
   joint author — he is a member of the committee that made the code, and the work
   is not ours alone. Venue order: ASSETS → TACCESS → LREC.

---

## The one thing to decide before building further

Whether the site is **a demo of our software** or **the reference page for Standard
Sindhi Braille**. They look similar and are not the same thing. The second is more
useful and more responsible — it means the specification, the tables and the open
questions are the point, and the translator is the proof — but it also means the
Sindhi Language Authority should be told it exists, and ideally should bless it.

The prototype is built as the second. That should be confirmed with Riaz before
the site goes public under his name and the committee's.

---

**Digital implementation, verification and documentation by Safeer Ali Mirani,
2026**, in partnership with **Riaz Hussain Memon** — blind teacher, President of
the Pakistan Association of the Blind (Sindh), and a member of the committee that
authored the code. The braille code itself is the work of the Sindhi Language
Authority committee and is not altered here.
