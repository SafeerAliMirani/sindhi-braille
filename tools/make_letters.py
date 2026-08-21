# -*- coding: utf-8 -*-
"""
Part one of the primer: the letters, in the order the corpus says to teach them.

    python tools/make_letters.py > book/src/01-letters.txt

Thirteen lessons, four letters each, all fifty-two. The order comes from
teaching_order.py; the words and the one sentence per lesson are chosen here,
and every one of them is checked against the letters taught so far. A primer
that quietly uses an untaught letter is worse than no primer: the child meets a
shape nobody has named and concludes that reading is guessing.

Two letters are pinned out of their greedy position, and the reason is in
teaching_order.order(): آ carries آهي, which ends nearly every Sindhi sentence,
so withholding it until lesson seven withholds sentences until lesson seven.
With آ in lesson two and ڪ in lesson three, the child reads a whole sentence -
هي ڪتاب آهي - on the third page.
"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sindhi_braille as sb
import teaching_order as to

PIN = {2: 'آ', 3: 'ڪت'}

# lesson -> (four words, one for each letter taught) and a sentence, or None
CONTENT = [
    (['هي', 'هن', 'ان', 'ناني'],              None),
    (['آهي', 'جو', 'هو', 'کان'],             None),
    (['هڪ', 'ڪتاب', 'ته', 'بار'],             'هي ڪتاب آهي.'),
    (['مان', 'سان', 'لال', 'ماء'],            'هي لال ڪتاب آهي.'),
    (['در', 'پير', 'شير', 'علي'],            'هي در آهي.'),
    (['گل', 'ڏند', 'پاڻي', 'ٿورو'],           'هي گل آهي.'),
    (['قلم', 'ٻلي', 'ڪپڙا', 'ڌرتي'],         'هي ٻلي آهي.'),
    (['فون', 'خط', 'حال', 'طوطو'],            'هي خط آهي.'),
    (['ٽوپي', 'صاف', 'ڳڻ', 'حافظ'],           'هي ٽوپي آهي.'),
    (['چار', 'زمين', 'ٺيڪ', 'ڊوڙ'],           'هي چار ڪتاب آهن.'),
    (['باغ', 'ڇت', 'ڀيڻ', 'ضرور'],            'هي باغ آهي.'),
    (['ڄاڻ', 'ذات', 'مثال', 'پڃرو'],          'هي پڃرو آهي.'),
    (['ڍڳو', 'سڱ', 'ڦل', 'گھر'],              'هي منهنجو گھر آهي.'),
]

SD_DIGITS = '۰۱۲۳۴۵۶۷۸۹'


def sd_num(n):
    return ''.join(SD_DIGITS[int(d)] for d in str(n))


def main():
    plan, _ = to.order(13, 4, PIN)
    order = [picked for picked, _ in plan]
    known = set()
    out = []
    bad = 0
    for i, (picked, (words, sentence)) in enumerate(zip(order, CONTENT), 1):
        known |= set(picked)
        # ک is written with ڪ's cell and do-chashmi's, so a word containing it
        # needs both; every other letter stands for itself.
        usable = set(known)
        if 'ک' in known:
            usable |= {'ڪ', 'ھ'}
        out.append('@heading سبق %s' % sd_num(i))
        out.append(' '.join(picked))
        for w in words + ([sentence] if sentence else []):
            for ch in w:
                if ch in sb.LETTER and ch not in usable:
                    sys.stderr.write('LESSON %d: %s uses %s, not taught yet\n'
                                     % (i, w, ch))
                    bad += 1
        shown = ' '.join(words + ([sentence] if sentence else []))
        for ch in picked:
            if ch not in shown:
                sys.stderr.write('LESSON %d: teaches %s and never shows it in a '
                                 'word\n' % (i, ch))
                bad += 1
        out.extend(words)
        if sentence:
            out.append(sentence)
    sys.stdout.write('\n'.join(out) + '\n')
    if bad:
        sys.stderr.write('%d words use letters that have not been taught\n' % bad)
        raise SystemExit(1)
    sys.stderr.write('13 lessons, 52 letters, every word inside its lesson\n')


if __name__ == '__main__':
    main()
