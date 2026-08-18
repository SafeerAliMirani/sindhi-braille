# -*- coding: utf-8 -*-
"""
Write the browser's copy of the word list from tools/sindhi_words.txt.

    python make_wordlist.py            # rewrite website/src/engine.js
    python make_wordlist.py --check    # fail if the copy is out of date

The word list is what settles the cells that carry more than one reading, so the
browser needs the same list the Python has. It used to be pasted in by hand, and
it drifted: the browser was still carrying مين and اءين after those two entries
were corrected to ۾ and ۽, and it had picked up two mojibake entries on the way.
Generating it means the two lists cannot disagree again.

Order is preserved, because the file is ordered by how often each word occurs and
that order is worth keeping for anyone reading it.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, 'website', 'src', 'engine.js')
WORDS = os.path.join(HERE, 'sindhi_words.txt')
OPEN, CLOSE = 'const WORDLIST = ', ';\n'


def words():
    out, seen = [], set()
    for line in io.open(WORDS, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.startswith('#'):
            continue
        w = line.split('\t')[0]
        if w and w not in seen:
            seen.add(w); out.append(w)
    return out


def block(ws):
    return OPEN + json.dumps('\n'.join(ws), ensure_ascii=False) + CLOSE


def main(check=False):
    ws = words()
    src = io.open(ENGINE, encoding='utf-8').read()
    a = src.index(OPEN)
    b = src.index(CLOSE, a) + len(CLOSE)
    out = src[:a] + block(ws) + src[b:]
    if check:
        ok = out == src
        print('the browser word list is %s' % ('up to date' if ok else 'OUT OF DATE'))
        return 0 if ok else 1
    io.open(ENGINE, 'w', encoding='utf-8', newline='\n').write(out)
    print('%d words written to the browser engine' % len(ws))
    return 0


if __name__ == '__main__':
    raise SystemExit(main('--check' in sys.argv))
