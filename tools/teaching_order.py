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


def words():
    out = []
    for line in io.open(os.path.join(HERE, 'sindhi_words.txt'), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        p = line.split('\t')
        w = p[0].strip()
        f = int(p[1]) if len(p) > 1 and p[1].isdigit() else 1
        if w:
            out.append((w, f))
    return out


def letters_of(w):
    """the letters a reader must know, with the diacritics stripped: a beginner
    reads the skeleton, and the marks come later"""
    return {c for c in w if c in sb.LETTER}


def readable(w):
    """a word we can honestly put in a primer: nothing but letters"""
    return bool(w) and all(c in sb.LETTER or c in SKIP for c in w)


def order(n_lessons, per_lesson):
    ws = [(w, f) for w, f in words() if readable(w)]
    known, plan = set(), []
    pool = collections.Counter()
    for w, f in ws:
        for c in letters_of(w):
            pool[c] += f

    for lesson in range(n_lessons):
        picked = []
        for _ in range(per_lesson):
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
    plan, ws = order(n, per)
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
                 '  '.join(w for w, _ in fresh[:8])))
    print()
    print('after %d lessons: %d of %d letters, %d words readable, %.1f%% of the corpus'
          % (len(plan), len(set(sum([p for p, _ in plan], []))), len(sb.LETTER),
             len(seen), 100.0 * sum(f for w, f in ws if w in seen) / total))


if __name__ == '__main__':
    main()
