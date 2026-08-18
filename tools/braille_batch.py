# -*- coding: utf-8 -*-
"""
Turn a folder of documents into embosser-ready Sindhi braille.

    python braille_batch.py INPUT [INPUT ...] -o OUTDIR [--width 28] [--height 25]

INPUT may be a file or a folder (searched recursively).  Every document it can
read becomes one `.brf` beside a short report saying what was translated, what
was dropped, and how many braille pages it came to.

Formats read with no extra software:
    .txt .md .html .htm .xhtml .docx .odt .brf (passed through)
Formats that need one extra tool:
    .pdf   -> `pdftotext` (poppler-utils) if it is on the PATH, otherwise `pypdf`
              (`pip install pypdf`).  On Windows, pypdf is the easy one.
Formats that cannot be read:
    .inp   -> InPage.  See the note printed for the file.

Nothing here guesses.  If a character has no braille in the standard, it is
counted and listed rather than silently dropped, because a silent drop in a
schoolbook is the kind of error nobody notices until a child does.
"""
import argparse, collections, io, os, re, shutil, subprocess, sys, zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindhi_braille as sb

READABLE = {'.txt', '.md', '.html', '.htm', '.xhtml', '.docx', '.odt', '.pdf', '.brf'}

# ------------------------------------------------------------------ readers --
def read_txt(p):
    for enc in ('utf-8-sig', 'utf-8', 'cp1256', 'utf-16'):
        try:
            with io.open(p, encoding=enc) as f: return f.read()
        except (UnicodeDecodeError, UnicodeError): continue
    raise ValueError('could not decode this file in UTF-8, UTF-16 or Windows-1256')

def _xml_text(data, tagnames, brk):
    """pull text out of an office XML part, keeping paragraph breaks"""
    root = ET.fromstring(data)
    out, buf = [], []
    for el in root.iter():
        tag = el.tag.rsplit('}', 1)[-1]
        if tag in tagnames and el.text:
            buf.append(el.text)
        if tag in brk:
            if buf: out.append(''.join(buf)); buf = []
            else:   out.append('')
    if buf: out.append(''.join(buf))
    return '\n'.join(x for x in out)

def read_docx(p):
    with zipfile.ZipFile(p) as z:
        return _xml_text(z.read('word/document.xml'), {'t'}, {'p'})

def read_odt(p):
    with zipfile.ZipFile(p) as z:
        return _xml_text(z.read('content.xml'), {'p', 'h', 'span'}, {'p', 'h'})

class _Strip(__import__('html.parser', fromlist=['HTMLParser']).HTMLParser):
    SKIP = {'script', 'style', 'head'}
    BLOCK = {'p','div','br','li','tr','h1','h2','h3','h4','h5','h6','section','article'}
    def __init__(self):
        super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self, t, a):
        if t in self.SKIP: self.skip += 1
        elif t in self.BLOCK: self.out.append('\n')
    def handle_endtag(self, t):
        if t in self.SKIP and self.skip: self.skip -= 1
        elif t in self.BLOCK: self.out.append('\n')
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

def read_html(p):
    s = _Strip(); s.feed(read_txt(p))
    return re.sub(r'\n{3,}', '\n\n', ''.join(s.out))

def read_pdf(p):
    """Two ways in, because neither is available everywhere.

    `pdftotext` (poppler) is the better extractor and is normal on Linux and mac.
    On Windows it usually is not there, so `pypdf` is tried second: one
    `pip install pypdf` and PDFs work, with no system package to find.
    """
    txt = ''
    if shutil.which('pdftotext'):
        r = subprocess.run(['pdftotext', '-layout', '-enc', 'UTF-8', p, '-'],
                           capture_output=True)
        if not r.returncode:
            txt = r.stdout.decode('utf-8', 'replace')
    if len(txt.strip()) < 20:
        try:
            import pypdf
        except ImportError:
            pypdf = None
        if pypdf is not None:
            try:
                pages = [pg.extract_text() or '' for pg in pypdf.PdfReader(p).pages]
                txt = '\n\n'.join(pages)
            except Exception as e:
                raise ValueError('pypdf could not read this PDF: %s' % e)
    if not txt.strip():
        raise ValueError('no text could be read from this PDF. Install one of them '
                         '- `pip install pypdf`, or poppler for `pdftotext` - or '
                         'save the document as .docx or .txt first')
    if len(txt.strip()) < 20:
        raise ValueError('this PDF has no text layer - it is a scan. It needs OCR '
                         'before it can be brailled.')
    return txt

READERS = {'.txt':read_txt, '.md':read_txt, '.html':read_html, '.htm':read_html,
           '.xhtml':read_html, '.docx':read_docx, '.odt':read_odt, '.pdf':read_pdf}

# ------------------------------------------------------------------- checks --
def unknown_chars(text):
    """characters the standard has no braille for — reported, never hidden"""
    known = set(sb.LETTER) | set(sb.NORMALISE) | set(sb.SPELLOUT) | set(sb.DIACRITIC)
    known |= set(sb.PUNCT) | set(sb.ARABIC_DIGIT) | set('0123456789') | set(' \n\t')
    known |= set(sb.QUOTE) | set(sb.BRACKET) | set(sb.MATH) | set('/:')
    known |= set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    # the religious abbreviations are whole phrases, and ﷺ is a single character
    # that has a braille of its own.  Leaving them out of this set reported them
    # as dropped when they had in fact been written.
    for _phrase, _cells in sb.ABBREV: known |= set(_phrase)
    bad = collections.Counter(c for c in text if c not in known)
    for c in list(bad):
        if c in '\r‎‏‌‍ـ': del bad[c]
    return bad

def paginate(lines, width, height):
    rows = []
    for toks in lines:
        row = ''
        for cs in toks:
            piece = ''.join(sb.cell_to_ascii(c) for c in cs)
            while len(piece) > width:
                rows.append(piece[:width-1] + sb.cell_to_ascii(sb.HYPHEN))
                piece = piece[width-1:]
            if not row: row = piece
            elif len(row) + 1 + len(piece) <= width: row += ' ' + piece
            else: rows.append(row); row = piece
        rows.append(row)
    pages = [rows[i:i+height] for i in range(0, len(rows), height)] or [[]]
    return '\f'.join('\r\n'.join(p) for p in pages) + '\r\n\f', len(pages), len(rows)

# --------------------------------------------------------------------- main --
def gather(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in sorted(names): files.append(os.path.join(root, n))
        else: files.append(p)
    return files

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('-o', '--out', default='braille-out')
    ap.add_argument('--width', type=int, default=28,
                    help='cells per line (28 fits A4, 40 is the international page)')
    ap.add_argument('--height', type=int, default=25, help='lines per page')
    ap.add_argument('--diacritics', action='store_true',
                    help='write zer, zabar and pesh (beginner level only)')
    a = ap.parse_args()

    os.makedirs(a.out, exist_ok=True)
    sb.load_words()
    report, done, skipped = [], 0, 0

    for path in gather(a.inputs):
        ext = os.path.splitext(path)[1].lower()
        name = os.path.basename(path)
        if ext == '.inp':
            report.append((name, 'SKIPPED', 'InPage file. InPage does not export '
                'Unicode cleanly. Open it in InPage and "Export to Unicode text", or '
                'retype the text in Word, then run this again.'))
            skipped += 1; continue
        if ext not in READABLE:
            continue
        if ext == '.brf':
            shutil.copy2(path, os.path.join(a.out, name))
            report.append((name, 'COPIED', 'already braille — passed through unchanged'))
            done += 1; continue
        try:
            text = READERS[ext](path)
        except Exception as e:
            report.append((name, 'FAILED', str(e))); skipped += 1; continue

        bad = unknown_chars(text)
        lines = sb.translate(text, diacritics=a.diacritics)
        brf, pages, rows = paginate(lines, a.width, a.height)
        outp = os.path.join(a.out, os.path.splitext(name)[0] + '.brf')
        io.open(outp, 'w', encoding='ascii', newline='').write(brf)
        words = len(text.split())
        note = '%d words, %d braille lines, %d page%s' % (
            words, rows, pages, '' if pages == 1 else 's')
        if bad:
            top = ', '.join('%r x%d' % (c, n) for c, n in bad.most_common(8))
            note += '  |  NOT TRANSLATED: ' + top
        report.append((name, 'OK', note)); done += 1

    w = max([len(r[0]) for r in report] + [12])
    print()
    for n, st, msg in report:
        print('%-*s  %-8s %s' % (w, n, st, msg))
    print('\n%d file%s written to %s/   %d skipped'
          % (done, '' if done == 1 else 's', a.out, skipped))
    if any(r[1] == 'OK' and 'NOT TRANSLATED' in r[2] for r in report):
        print('\nCharacters listed as NOT TRANSLATED have no cell in the standard.')
        print('They were left out. Check them before embossing.')
    print('Page size: %d cells x %d lines. %s'
          % (a.width, a.height,
             'Fits A4.' if a.width <= 28 else 'Needs braille paper wider than A4.'))

if __name__ == '__main__':
    main()
