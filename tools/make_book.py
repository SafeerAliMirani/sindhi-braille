# -*- coding: utf-8 -*-
"""
Build a book: the .brf for the embosser and a teacher's copy for a sighted adult.

    python tools/make_book.py book --width 38 --out book/out

The source format is described in book/FORMAT.md and is meant for a typist who
reads Sindhi and no braille.

Two rules shape everything here.

**The printed page number is carried through.** Braille page 12 says which
printed page it came from, and the teacher's copy shows both. When the figures
are added later, nothing has to be re-typed and nothing has to be re-numbered.

**A picture that was left out says so.** A page that silently drops an exercise
teaches a child that the book does not make sense. A page that says a picture
stood here teaches them that something is missing and can be asked about, which
is true and is survivable.
"""
import io, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

# What stands in the braille where a picture was. Riaz decides the wording; this
# is short on purpose, because it will appear many times in a class 1 book.
FIGURE_MARK = 'تصوير'
PAGE_MARK   = 'صفحو'


def parse(path):
    """one lesson file -> a list of blocks"""
    blocks, page = [], None
    for raw in io.open(path, encoding='utf-8'):
        line = raw.rstrip('\n')
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('@page'):
            page = s[5:].strip()
            blocks.append(('page', page, ''))
        elif s.startswith('@heading'):
            blocks.append(('heading', page, s[8:].strip()))
        elif s.startswith('@figure'):
            blocks.append(('figure', page, s[7:].strip()))
        elif s.startswith('@exercise'):
            m = re.match(r'@exercise\s+(\S+)\s*(.*)', s)
            blocks.append(('exercise', page, (m.group(1), m.group(2)) if m
                           else ('', s[9:].strip())))
        elif s.startswith('@blank'):
            blocks.append(('blank', page, ''))
        else:
            blocks.append(('text', page, s))
    return blocks


def to_sindhi_lines(blocks):
    """blocks -> the Sindhi that will be brailled, one entry per braille
    paragraph, with the printed page each came from"""
    out = []
    for kind, page, val in blocks:
        if kind == 'page':
            out.append((page, '%s %s' % (PAGE_MARK, page), 'pagemark'))
        elif kind == 'heading':
            out.append((page, val, 'heading'))
        elif kind == 'figure':
            txt = '%s: %s' % (FIGURE_MARK, val) if val else FIGURE_MARK
            out.append((page, txt, 'figure'))
        elif kind == 'exercise':
            num, txt = val
            out.append((page, ('%s. %s' % (num, txt)).strip(), 'exercise'))
        elif kind == 'blank':
            out.append((page, '', 'blank'))
        else:
            out.append((page, val, 'text'))
    return out


def build(src_dir, width, out_dir):
    sb.load_words()
    files = sorted(f for f in os.listdir(src_dir) if f.endswith('.txt'))
    if not files:
        raise SystemExit('no .txt lesson files in %s' % src_dir)
    os.makedirs(out_dir, exist_ok=True)

    every = []
    for f in files:
        every += to_sindhi_lines(parse(os.path.join(src_dir, f)))

    # ---- the braille -----------------------------------------------------
    cell_lines = []
    for page, text, kind in every:
        if kind == 'blank' or not text:
            cell_lines.append([])
            continue
        cell_lines += sb.translate(text)
    brf = sb.to_brf(cell_lines, width=width, height=25)
    io.open(os.path.join(out_dir, 'book.brf'), 'w',
            encoding='ascii', newline='').write(brf)

    # ---- the teacher's copy ----------------------------------------------
    rows = []
    for page, text, kind in every:
        if kind == 'blank' or not text:
            continue
        cells = sb.translate(text)[0]
        dots = ' '.join(' '.join(g) for g in cells)
        uni = ''.join(sb.cell_to_unicode(c) if hasattr(sb, 'cell_to_unicode')
                      else '' for g in cells for c in g)
        rows.append((page or '', kind, text, dots, uni))

    doc = ["<!doctype html><meta charset='utf-8'>",
           "<title>Teacher's copy</title>",
           "<style>body{font-family:system-ui,sans-serif;margin:24px;"
           "line-height:1.5;color:#222}"
           "h1{font-size:20px} table{border-collapse:collapse;width:100%}"
           "td,th{border-top:1px solid #ddd;padding:8px 10px;vertical-align:top;"
           "font-size:14px}"
           ".sd{font-size:20px;direction:rtl;text-align:right;font-family:"
           "'Noto Naskh Arabic','Scheherazade New',serif}"
           ".dots{font-family:ui-monospace,monospace;font-size:12px;color:#555;"
           "word-break:break-all}"
           ".pg{color:#888;font-size:12px;white-space:nowrap}"
           ".figure{background:#fff8e1}.heading{background:#f1f5ff;font-weight:600}"
           ".exercise{background:#f6fff1}</style>",
           "<h1>Teacher's copy</h1>",
           "<p>Built at <b>%d cells per line</b>. Each row is one paragraph of "
           "the braille. The page column is the page of the <i>printed</i> book, "
           "so this copy and the printed book can be read side by side.</p>"
           % width,
           "<table><tr><th>printed page</th><th>what it is</th>"
           "<th>Sindhi</th><th>dots</th></tr>"]
    for page, kind, text, dots, _ in rows:
        doc.append("<tr class='%s'><td class='pg'>%s</td><td>%s</td>"
                   "<td class='sd'>%s</td><td class='dots'>%s</td></tr>"
                   % (kind, html.escape(page), kind,
                      html.escape(text), html.escape(dots)))
    doc.append("</table>")
    io.open(os.path.join(out_dir, 'teacher.html'), 'w',
            encoding='utf-8', newline='\n').write('\n'.join(doc))

    pages = len([p for p in brf.split('\f') if p.strip()])
    figs = sum(1 for _, _, k in every if k == 'figure')
    printed = sorted({p for p, _, k in every if p and k == 'pagemark'},
                     key=lambda x: (len(x), x))
    print('book.brf       %d braille pages at %d cells' % (pages, width))
    print('teacher.html   %d paragraphs' % len(rows))
    print('printed pages covered: %d' % len(printed))
    print('pictures marked as left out: %d' % figs)


if __name__ == '__main__':
    a = sys.argv[1:]
    src = a[0] if a and not a[0].startswith('-') else 'book'
    width = int(a[a.index('--width') + 1]) if '--width' in a else 38
    out = a[a.index('--out') + 1] if '--out' in a else os.path.join(src, 'out')
    build(os.path.join(ROOT, src) if not os.path.isabs(src) else src,
          width, os.path.join(ROOT, out) if not os.path.isabs(out) else out)
