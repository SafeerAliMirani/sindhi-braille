# -*- coding: utf-8 -*-
"""
Put the parts of the book in the order a child meets them, and number the
lessons once, here.

    python tools/assemble_book.py > book/src/book.txt

The order is the whole point. The letters come first, because a lesson that
uses a letter nobody has named teaches a child that reading is guessing. Then
the numbers, then the shapes, then sentences about things, then the topics that
make it a book somebody would want rather than a drill.

Lesson numbers are assigned here and nowhere else, so a part can be moved,
lengthened or dropped without renumbering anything by hand.
"""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'book', 'src')
PARTS = ['00-front.txt', '01-letters.txt', '02-numbers.txt', '03-shapes.txt',
         '04-reading.txt', '05-topics.txt']
SD = '۰۱۲۳۴۵۶۷۸۹'


def sd_num(n):
    return ''.join(SD[int(d)] for d in str(n))


def main():
    out, n = [], 0
    for part in PARTS:
        p = os.path.join(SRC, part)
        if not os.path.exists(p):
            sys.stderr.write('missing: %s\n' % part)
            continue
        for line in io.open(p, encoding='utf-8'):
            s = line.rstrip('\n')
            if s.strip().startswith('@title'):
                # front matter: a heading that is not a lesson and takes no
                # number. The title page and the two charts come before سبق ۱.
                out.append('@heading ' + s.strip()[6:].strip())
            elif s.strip().startswith('@heading سبق'):
                n += 1
                out.append('@heading سبق %s' % sd_num(n))
            elif s.strip():
                out.append(s.strip())
    sys.stdout.write('\n'.join(out) + '\n')
    sys.stderr.write('%d lessons across %d parts\n' % (n, len(PARTS)))


if __name__ == '__main__':
    main()
