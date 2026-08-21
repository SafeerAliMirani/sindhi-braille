# -*- coding: utf-8 -*-
"""
Work out the order to teach the letters in, from the corpus rather than by ear.

    python tools/teaching_order.py --lessons 12

A primer's whole difficulty is sequencing. Teach the letters in alphabet order
and a child spends nine lessons unable to read a single real word. Teach them in
the order that unlocks the most words soonest and they are reading by lesson two.

So the order here is greedy against the committee's own publications: at every
step, add the letter that makes the largest number of *new real words* readable,
weighted by how often those words occur. Nothing is invented. Every word this
prints occurs in the corpus.

The output is the spine of the table of contents: what each lesson teaches, and
which real words it makes available.
"""
import io, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

SKIP = set(' ‌‍')


# The five words the guide prints dots for that contain do-chashmi, p.30.  These
# are the only ھ spellings in the list that are certainly right, because the book
# printed the cells beside them.
GUIDE_DIGRAPH_WORDS = {'جھرڪي', 'گھڙيال', 'ڳالھيون', 'پڙھ', 'سمھ'}

# The seven bases that form a digraph with do-chashmi, guide p.30:
# جھ گھ ڙھ لھ مھ نھ ڻھ.  Five of the seven the guide also prints inside a whole
# word, with the cells beside it, and those five are settled:
#
#     جھ   جھرڪي    245 236 1235 13 24
#     گھ   گھڙيال   1245 236 12456 24 1 123
#     ڙھ   پڙھ      1234 12456 236
#     لھ   ڳالھيون  13456 1 123 236 24 2456 1345
#     مھ   سمھ      234 134 236
#
# So a he after ج، گ، ڙ، ل or م in a native Sindhi word is the second half of a
# single letter and takes 2-3-6.  That covers گھر، گھوڙو، ڊگھو، پڙھو، ڳاڙھو،
# جھاز، ٿيلھو - ordinary words a six-year-old needs on page one.
SETTLED_BASE = set('جگڙلم')

# نھ and ڻھ the guide names as letters but never prints inside a word, so a he
# after ن or ڻ is still open: ڏينهن and مينهن could be either.  Sheet 7.
DIGRAPH_BASE = set('نڻ')

# Arabic and Persian loanwords are the known exception - there the ل or م and
# the ه are two letters that happen to meet, not a digraph.  The primer uses
# child vocabulary, where they do not arise; a general text will need the
# lexicon to tell them apart.

# Filled by words(): canonical forms whose he could be half of a digraph.  They
# are marked in the output and must not be used as a primer example word until
# sheet 7 comes back.  Everything unmarked is safe to print.
FOLDED = set()


def open_he(w):
    """does this word contain a he whose cell is still open?"""
    return any(c == 'ه' and i and w[i-1] in DIGRAPH_BASE for i, c in enumerate(w))


def canonical(w):
    """the spelling to count this word under.

    The list carries 262 words twice, once with ه and once with ھ, at almost
    identical frequencies, because two bodies of text were counted under two
    conventions.  Ranking on that gives ھ the weight of an ordinary he and puts
    it in the first lesson, which is how the primer came to teach a
    digraph-only letter on page 5.

    Nothing is guessed: a ھ is kept only in the five words the guide itself
    prints cells for, and folded into ه everywhere else.  That understates ھ,
    which is the safe direction - it is taught last, from the book's own
    examples, instead of first from a miscount."""
    if w in GUIDE_DIGRAPH_WORDS:
        return w
    return w.replace('ھ', 'ه')


def words():
    out = []
    seen = {}
    for line in io.open(os.path.join(HERE, 'sindhi_words.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        p = line.split('\t')
        w = p[0].strip()
        f = int(p[1]) if len(p) > 1 and p[1].isdigit() else 1
        if not w:
            continue
        c = canonical(w)
        if open_he(c):
            FOLDED.add(c)                     # sheet 7 decides this one
        seen[c] = max(seen.get(c, 0), f)      # max, not sum: it is one word
    return sorted(seen.items(), key=lambda kv: -kv[1])


def letters_of(w):
    """the letters a reader must know, with the diacritics stripped: a beginner
    reads the skeleton, and the marks come later"""
    return {c for c in w if c in sb.LETTER}


def readable(w):
    """a word we can honestly put in a primer: nothing but letters"""
    return bool(w) and all(c in sb.LETTER or c in SKIP for c in w)


def order(n_lessons, per_lesson, pinned=None):
    """pinned: {lesson_number: 'letters'} forced before the greedy runs.

    The greedy maximises words unlocked, and left to itself it puts آ in lesson
    seven, because آ appears in few distinct words. But one of those words is
    آهي, which ends almost every sentence a beginner will ever read, so a primer
    that withholds آ withholds sentences. Pinning آ and ڪ early costs a little
    coverage and buys the child a real sentence in lesson three instead of
    lesson seven. That is a teaching decision, and it is written here rather
    than hidden in a hand-edited table."""
    pinned = pinned or {}
    ws = [(w, f) for w, f in words() if readable(w)]
    known, plan = set(), []
    pool = collections.Counter()
    for w, f in ws:
        for c in letters_of(w):
            pool[c] += f

    for lesson in range(n_lessons):
        picked = [c for c in pinned.get(lesson + 1, '') if c not in known]
        for _ in range(per_lesson - len(picked)):
            best, gain = None, -1
            for c in sb.LETTER:
                if c in known or c in picked:
                    continue
                trial = known | set(picked) | {c}
                g = sum(f for w, f in ws
                        if letters_of(w) <= trial and not letters_of(w) <= (known | set(picked)))
                if g > gain:
                    gain, best = g, c
            if best is None:
                break
            picked.append(best)
        if not picked:
            break
        known |= set(picked)
        now = [(w, f) for w, f in ws if letters_of(w) <= known]
        plan.append((picked, now))
    return plan, ws


def main():
    a = sys.argv[1:]
    n = int(a[a.index('--lessons') + 1]) if '--lessons' in a else 12
    per = int(a[a.index('--per') + 1]) if '--per' in a else 4
    pinned = {}
    if '--pin' in a:
        for part in a[a.index('--pin') + 1].split(','):
            k, v = part.split(':')
            pinned[int(k)] = v
    plan, ws = order(n, per, pinned)
    total = sum(f for _, f in ws)
    seen = set()
    print('%-3s %-22s %6s %8s   %s' % ('#', 'letters taught', 'words', 'corpus', 'new words this lesson'))
    print('-' * 100)
    for i, (picked, now) in enumerate(plan, 1):
        fresh = [(w, f) for w, f in now if w not in seen]
        fresh.sort(key=lambda x: -x[1])
        seen |= {w for w, _ in now}
        cov = 100.0 * sum(f for _, f in now) / total
        print('%-3d %-22s %6d %7.1f%%   %s'
              % (i, ' '.join(picked), len(now), cov,
                 '  '.join(w + ('*' if w in FOLDED else '') for w, _ in fresh[:8])))
    print()
    print('  * its he spelling is still open (sheet 7); not usable as an example word yet')
    print()
    print('after %d lessons: %d of %d letters, %d words readable, %.1f%% of the corpus'
          % (len(plan), len(set(sum([p for p, _ in plan], []))), len(sb.LETTER),
             len(seen), 100.0 * sum(f for w, f in ws if w in seen) / total))


if __name__ == '__main__':
    main()
