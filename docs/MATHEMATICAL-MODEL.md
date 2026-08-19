# How Sindhi braille was made digital — the mathematics

This is the formal description of what the software does. It is written so that
the method can be checked, reproduced, and cited; nothing here is a metaphor.

---

## 1. The cell

A braille cell is six dot positions, each raised or flat. Number them

$$
\begin{matrix}
1 & \cdot & 4\\
2 & \cdot & 5\\
3 & \cdot & 6
\end{matrix}
$$

A cell is therefore a subset of the position set $P=\{1,2,3,4,5,6\}$, or
equivalently a vector in $\mathbb{F}_2^{6}$. Write $\mathcal{B}=2^{P}$ for the set
of all cells, so

$$|\mathcal{B}| = 2^{6} = 64 .$$

The empty cell is the space, so a braille **script** has

$$|\mathcal{B}^{*}| = 63$$

usable symbols. This number is the origin of every difficulty in this project,
and the standard guide says so itself on page 39: *"since braille has only 63
signs … fixing signs for them is necessary; otherwise many ambiguities would
arise everywhere."*

**Encoding.** We write a cell as its raised dot numbers in ascending order —
`1245` for $\{1,2,4,5\}$. The three machine representations are all bijections
of $\mathcal{B}$:

$$
\nu(c) \;=\; \sum_{d\in c} 2^{\,d-1}
\qquad\text{(the dot bitmask, } 0\le\nu\le 63)
$$

$$
\mathrm{unicode}(c) = \mathtt{U+2800} + \nu(c),
\qquad
\mathrm{brf}(c) = \mathrm{BA}\big[\nu(c)\big]
$$

where $\mathrm{BA}$ is the fixed 64-character North-American Braille ASCII
string. Because $\nu$ is a bijection, an embosser file (BRF), a screen display
(Unicode), and our internal dot strings are the same object in three costumes;
no information is created or lost passing between them.

---

## 2. Louis Braille's generative structure

The 63 cells are not an arbitrary list. Braille built them in seven lines from a
ten-element base and two operators, and Sindhi braille inherits this structure
whole. Let

$$
L_1=\{1,\;12,\;14,\;145,\;15,\;124,\;1245,\;125,\;24,\;245\}
$$

be the base line (all subsets of $\{1,2,4,5\}$ that Braille used). Define two
operators on cells:

**Addition** of a fixed dot set $S$:

$$\alpha_S(c) = c \cup S$$

**Lowering**, the shift of every dot down one row:

$$
\sigma(c) = \{\,\pi(d) : d\in c\,\},\qquad
\pi:1\mapsto2,\;2\mapsto3,\;4\mapsto5,\;5\mapsto6
$$

Then the classical lines are

$$
L_2=\alpha_{\{3\}}(L_1),\quad
L_3=\alpha_{\{3,6\}}(L_1),\quad
L_4=\alpha_{\{6\}}(L_1),\quad
L_5=\sigma(L_1)
$$

together with $L_6=\{34,346,3456,345,3,36\}$ and
$L_7=\{4,45,456,5,46,56,6\}$. These seven sets partition the 63 non-empty cells.

**Why this matters here.** Two rules of the Sindhi code are exactly this algebra,
and could not have been read off the page without it:

- **The lower-sign digits are $\sigma$ applied to the digits.** Guide pp.43 and
  52 call the ordinary digits the *Upper Sign* and the fraction denominators the
  *Lower Sign*. Formally, if $\delta(n)\in L_1$ is the cell for digit $n$, the
  denominator cell is $\sigma(\delta(n))$:

  $$\delta(4)=145 \;\Longrightarrow\; \sigma(\delta(4))=256$$

  which is precisely what the guide prints for $\tfrac34$.

- **The prefix signs are $L_7$.** The number sign is in $L_6$; the letter sign
  (dots 5-6), the dagger-alif sign (dot 4) and the numeric terminator (dot 6) are
  all in $L_7$, as are six of the seven Grade 2 series prefixes. That the code's
  "operator" symbols live in one classical line is a structural check we used
  repeatedly — and it is why no ordinary Sindhi letter is written with those
  cells. Every member of $L_7$ carries something: six open a Grade 2 contraction
  series, one is the letter sign, and dots 4-6 is the ڳانڊڙا group prefix.

---

## 3. Translation as a transduction

Let $\Sigma$ be the Sindhi alphabet plus digits and punctuation. Forward
translation is a map

$$T:\Sigma^{*}\longrightarrow \mathcal{B}^{*}$$

built as a **finite-state transducer with a bounded look-around window**. It is
not a character-by-character substitution, because several rules depend on
context. Writing $w=w_1w_2\dots w_n$, the transduction applies, in order:

1. **Normalisation** $\;\eta:\Sigma\to\Sigma$, folding orthographic variants
   ($\text{ئ},\text{ؤ}\mapsto\text{ء}$; $\text{أ},\text{إ},\text{ٱ}\mapsto\text{ا}$;
   $\text{ة},\text{ہ}\mapsto\text{ه}$; $\text{ی}\mapsto\text{ي}$;
   $\text{ك}\mapsto\text{ڪ}$) and expanding the two Sindhi signs that have no
   cell of their own ($\text{۾}\mapsto$ م ي ن, $\text{۽}\mapsto$ ا َ ء ي ن).
2. **Phrase rules** — window $\le 3$ words: the religious abbreviations, the
   repeated-word rule, the واؤ عطف joiner, the foreign-language marks.
3. **Token rules** — window = 1 word: fractions, ratios, decimals, Roman
   numerals, exercise labels, arithmetic operators.
4. **Character rules** — window $\le 2$ characters: letters, aspirated digraphs,
   diacritics.

Each stage is deterministic, so $T$ is a function, and every rule is bounded, so
$T$ is computable in $O(n)$ in the length of the text.

**Two rules are genuinely non-local**, and this is worth stating precisely
because it is why the standard cannot be expressed in liblouis's rule language
alone:

- *The repeated word* (guide p.45): $w_k w_{k+1} \mapsto T(w_k)\cdot(3)(3)$ when
  $w_k=w_{k+1}$. Deciding this requires comparing two adjacent words, which the
  rule language cannot test.
- *The fraction* (guide pp.52–53):
  $$T(a/b) \;=\; (3456)\cdot\big[a\ne 1\big]\,\delta(a)\cdot\sigma\big(\delta(b)\big)$$
  where $[a\ne 1]$ is the Iverson bracket — the numerator is written **only if it
  is not 1**. Deciding that requires looking at both sides of the slash at once.

---

## 4. The shared-cell problem, stated exactly

$T$ is **not injective**. Because the code assigns more meanings than there are
cells, several cells carry more than one reading. Counting only the assignments
in the implemented code:

| | |
|---|---|
| distinct meanings assigned to single cells | **89** |
| cells available | **63** |
| cells carrying three or more meanings | **8** |

Formally, define for each cell $c$ its **reading set** $R(c)\subseteq\Sigma$.
Eight cells have $|R(c)|\ge 3$; the worst are

$$
R(2)=\{\text{zabar},\;\text{،},\;\text{decimal point},\;\text{lower }1,\;\text{pen-name mark}\}
$$
$$
R(236)=\{\text{ھ},\;\text{؟},\;\text{lower }8,\;\text{open quote}\}
$$

Back-translation is therefore not a function but a **choice problem**: given
$\beta\in\mathcal{B}^{*}$, find $w$ with $T(w)=\beta$. The code resolves most of
these by **position**, which we can state as predicates on the index:

$$
c=3456 \;\longmapsto\;
\begin{cases}
\text{number sign} & \text{if } i=0\\[2pt]
\text{ڻ} & \text{otherwise}
\end{cases}
$$

This rule is only sound if no ordinary Sindhi word begins with ڻ. **We tested
that claim rather than assuming it**, and the honest result is not zero. Over
23,432 word tokens of the committee's own publications:

$$N_{\text{initial}}(\text{ڻ}) = 18,
\qquad N_{\text{medial/final}}(\text{ڻ}) = 604 .$$

Seventeen of those eighteen are the **bare letter standing alone**, which is
what a book about the alphabet contains and not what running prose does. The
eighteenth is the aspirate **ڻھ**, and that one is already accounted for: its
two cells are also the fraction 1/8, which is why ڻھ is one of the four
spellings `check_all.py` reports as not surviving the round trip. The rule is
sound for prose and its single exception is counted in the fidelity figure
rather than hidden behind it.

*(An earlier version of this document gave 0 initial and 619 elsewhere over
21,445 tokens. That was measured before the word list was corrected for the ۾
and ۽ signs; the figures above are from the current list.)*

Similarly $256$, $235$ and $2$ resolve by word-final position, and $25$ resolves
by look-ahead (a ratio is followed by a fresh number sign; a fraction denominator
is not).

**One ambiguity survives and cannot be removed by any positional rule.** At the
end of a word, $236$ is either the letter ھ or the question mark ؟, and guide
p.35 places the question mark in exactly the position a final ھ occupies. Here
back-translation is a **maximum-plausibility decision** rather than a rule: given
the stem $s$ and a lexicon $W$,

$$
\hat{x} \;=\;
\begin{cases}
\text{ھ} & \text{if } s\!\cdot\!\text{ھ}\in W\\
\text{؟} & \text{else if } s\in W\\
\text{ھ} & \text{otherwise (the prior: final ھ is far commoner)}
\end{cases}
$$

A human reader resolves it from the sense of the sentence. A machine, lacking
that, uses the lexicon; where the lexicon is silent it falls back on the prior.

---

## 5. How correctness was measured

**Fidelity.** For a corpus of word types $w$ with frequencies $f(w)$,

$$
\rho \;=\; \frac{\sum_{w} f(w)\,\big[\,T^{-1}(T(w))=w\,\big]}{\sum_{w} f(w)}
$$

Measured on 23,434 word tokens (2,704 types) drawn from the committee's own
publications: $\rho = 0.9994$. The residue is the ع abbreviation, whose reading
provably requires sentence context (guide p.55), plus two spelling variants.

A held-out variant, in which the lexicon $W$ is built from one half of the types
and $\rho$ measured on the disjoint other half, is reported separately, because
measuring a lexicon on its own training data is circular and inflates the figure.

**Agreement with the standard.** Fidelity is a self-consistency measure: it
compares the software with itself. The independent measure is agreement with the
Authority's own printed dots. Let $G$ be the set of worked examples printed in
the standard guide whose dots we can read, and $\beta_g$ the dots as printed:

$$
A \;=\; \frac{\big|\{\,g\in G : T(g)=\beta_g\,\}\big|}{|G|}
$$

Currently $|G| = 69$ and $A = 1.000$ — every printed example, including the
fractions, the four arithmetic examples, the Roman numerals, the abbreviations
and the sample sentences, is reproduced cell for cell.

**Attestation.** For each symbol in the code, count how many times its cell occurs
in the printed material available. A symbol with a count of zero is *unattested*:
its value rests on the chart alone rather than on anything printed. This is a
useful weak signal, not a proof — a low count can mean a rare letter as easily as
a wrong one, and a count taken off the guide's typesetting can be wrong in a way
the author's own book is not. It is a prompt to go and ask, never a licence to change a letter.

---

## 6. The page

Embossing is a physical constraint, not a formatting preference. The standard
geometry is

$$
p_{\text{dot}} = 2.5\,\text{mm},\quad
p_{\text{cell}} = 6.2\,\text{mm},\quad
p_{\text{line}} = 10.0\,\text{mm},\quad
\varnothing_{\text{dot}} = 1.5\,\text{mm}
$$

A page of $C$ columns by $R$ rows needs

$$
W = (C-1)\,p_{\text{cell}} + p_{\text{dot}} + \varnothing_{\text{dot}},
\qquad
H = (R-1)\,p_{\text{line}} + 2\,p_{\text{dot}} + \varnothing_{\text{dot}}
$$

The international page, $C=40$, $R=25$, needs $246\times246$ mm. A4 is
$210\times297$ mm, so the international page **does not fit A4**: the widest line
A4 will take is

$$
C_{\max} = \left\lfloor \frac{210 - p_{\text{dot}} - \varnothing_{\text{dot}}}{p_{\text{cell}}} \right\rfloor + 1 = 28 .
$$

This is why the embosser must be fed the correct stock, and why the print-braille
pipeline specifies paper size before anything else.

---

## 7. A note on scope

Everything above is something the software actually does — the encodings are the
functions in `sindhi_braille.py`, the counts are computed from the implemented
tables, and the three measures are the ones `verify_guide.py` and the round-trip
test report. Nothing here is decoration.

What it cannot do is decide what the code *is*. That was settled by the committee
on 7 November 2016. Where the printed guide is ambiguous, the model's job is to
make the ambiguity visible rather than guess past it.
