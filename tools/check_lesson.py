# -*- coding: utf-8 -*-
"""
Check a lesson before it goes in the book.

    python tools/check_lesson.py lesson.txt --taught 7

Two questions, and they are the two a person cannot answer reliably by eye.

**Does it use a letter the book has not taught yet?** With --taught N, N is the
lesson number in the alphabet part, and the letters are those taught up to and
including it. Leave it out and the whole alphabet is allowed.

**Does every word survive the round trip?** Sindhi to braille and back. A word
that comes back different is a word the braille edition spells differently from
the printed one, and in a primer that is not a small thing: the child is being
taught a spelling their own book contradicts.

Whatever comes back from a person or from a model goes through this first.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sindhi_braille as sb

ORDER = [
 ['ھ','ن','ا','ي'], ['ج','و','ک','ر'], ['ت','ه','ب','ل'], ['ء','م','س','د'],
 ['ع','ڪ','پ','ش'], ['ٿ','ڏ','آ','گ'], ['ڻ','ڌ','ڙ','ق'], ['ٻ','ف','خ','ط'],
 ['ح','ص','ظ','ٽ'], ['ڳ','ٺ','چ','ز'], ['ڊ','ض','غ','ڇ'], ['ڀ','ث','ذ','ڄ'],
 ['ڃ','ڍ','ڦ','ڱ'],
]
# characters the translator rewrites, so a word holding one is spelled two ways
REWRITTEN = dict(sb.NORMALISE)


def taught_upto(n):
    out = set()
    for grp in ORDER[:n]:
        out |= set(grp)
    return out


def check(path, upto=None):
    sb.load_words()
    allowed = taught_upto(upto) if upto else set(sb.LETTER)
    text = io.open(path, encoding='utf-8').read()
    bad_letter, bad_trip, bad_char = [], [], []
    for lineno, line in enumerate(text.split('\n'), 1):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        for w in s.split():
            for c in w:
                if c in REWRITTEN:
                    bad_char.append((lineno, w, c, REWRITTEN[c]))
            used = {c for c in w if c in sb.LETTER}
            early = used - allowed
            if early:
                bad_letter.append((lineno, w, ''.join(sorted(early))))
        rt = sb.back(sb.translate(s))
        if rt != s:
            bad_trip.append((lineno, s, rt))

    n = len([l for l in text.split('\n') if l.strip() and not l.startswith('#')])
    print('%s — %d lines, letters allowed: %d' % (path, n, len(allowed)))
    if bad_char:
        print('\n  characters the translator rewrites (%d):' % len(bad_char))
        for ln, w, c, to in bad_char:
            print('    line %-3d %-14s %s should be written %s' % (ln, w, c, to))
    if bad_letter:
        print('\n  letters not taught yet (%d):' % len(bad_letter))
        for ln, w, e in bad_letter:
            print('    line %-3d %-14s uses %s' % (ln, w, e))
    if bad_trip:
        print('\n  lines that do not survive the round trip (%d):' % len(bad_trip))
        for ln, s, rt in bad_trip:
            print('    line %-3d' % ln)
            print('       written  %s' % s)
            print('       reads as %s' % rt)
    if not (bad_char or bad_letter or bad_trip):
        print('\n  clean. every line uses taught letters and round trips exactly.')
    return 1 if (bad_char or bad_letter or bad_trip) else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        raise SystemExit('usage: check_lesson.py <file> [--taught N]')
    up = int(a[a.index('--taught') + 1]) if '--taught' in a else None
    raise SystemExit(check(a[0], up))
