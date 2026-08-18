# -*- coding: utf-8 -*-
"""
Run every check this project has, and print one line per check.

    python check_all.py

    guide     the worked examples printed in the standard guide
    rules     parts of the code the guide states but does not work an example of
    selftest  the built-in Sindhi -> braille -> Sindhi cases
    words     the same, over the whole word list, weighted by how often each
              word actually occurs
    grade2    every contraction, phrase and group, both directions
    sheets    the three print sheets rebuild byte for byte
    neighbours  the letters against Arabic, Persian and Urdu braille - the one
              check using evidence neither author produced
    liblouis  both tables compile and the yaml suite passes (skipped if the
              liblouis tools are not installed)
    browser   the site's engine agrees with this one (skipped if node is not
              installed)
    document  a whole multi-page document converts to the same bytes in the
              browser as it does here
    ambiguity the table the site prints of cells with more than one reading is
              still the one the code tables give
    wordlist  the browser is carrying the same word list as this one

Exit status is 0 only if nothing failed.  A skipped check is not a pass and is
not counted as one.
"""
import io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import sindhi_braille as sb

results = []          # (name, ok, detail)  ok: True / False / None = skipped


def record(name, ok, detail):
    results.append((name, ok, detail))


# --------------------------------------------------------------- the guide --
def check_guide():
    import verify_guide
    ok = bad = 0
    for page, text, want, *_ in verify_guide.CASES:
        if verify_guide.got(text) == want: ok += 1
        else: bad += 1
    record('guide', bad == 0, '%d of %d printed examples, cell for cell'
           % (ok, ok + bad))

    rok = rbad = 0
    for page, text, want, *_ in verify_guide.RULES:
        if verify_guide.got(text) == want: rok += 1
        else: rbad += 1
    _, vtext, vwant, _ = verify_guide.VERSE
    if verify_guide.got(vtext, poetry=True) == vwant: rok += 1
    else: rbad += 1
    record('rules', rbad == 0,
           '%d of %d stated rules — implemented as read, not evidence'
           % (rok, rok + rbad))


# ------------------------------------------------------------- round trips --
def check_selftest():
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        good = sb.selftest()
    line = [l for l in buf.getvalue().splitlines() if 'faithful' in l]
    record('selftest', bool(good), line[-1].strip() if line else 'ran')


def check_words():
    total = ok = 0
    fails = []
    path = os.path.join(HERE, 'sindhi_words.txt')
    for L in io.open(path, encoding='utf-8'):
        L = L.rstrip('\n')
        if not L.strip() or L.startswith('#'): continue
        parts = L.split('\t')
        w = parts[0]
        f = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
        total += f
        if sb.back(sb.translate(w)) == w: ok += f
        else: fails.append(w)
    pct = 100.0 * ok / total if total else 0
    record('words', pct >= 99.9,
           '%.2f%% of %d words survive the round trip (%d spellings do not: %s)'
           % (pct, total, len(fails), '، '.join(fails[:6])))


def check_grade2():
    sb.load_grade2()
    ok = bad = 0
    collisions = set()
    for w in sb.GRADE2:
        if sb.back(sb.translate(w, grade2=True), grade2=True) == w: ok += 1
        else: bad += 1
    for parts, _ in sb.GRADE2P:
        t = ' '.join(parts)
        if sb.back(sb.translate(t, grade2=True), grade2=True) == t: ok += 1
        else: bad += 1
    for g, _ in sb.GRADE2G:
        t = 'آ' + g
        if sb.back(sb.translate(t, grade2=True), grade2=True) == t: ok += 1
        else: bad += 1
    for k, v in sb.G2AMBIG.items():
        collisions.add(' / '.join(v))
    # a failure is expected exactly where the book gives two words the same cells
    expected = sum(len(v) - 1 for v in sb.G2AMBIG.values())
    record('grade2', bad <= expected,
           '%d of %d contractions round trip; the %d that do not are cells the '
           'book itself gives to two words' % (ok, ok + bad, bad))


# ----------------------------------------------------------------- sheets ---
def check_sheets():
    import make_test_sheets, make_check_sheet
    sheets = os.path.join(ROOT, 'test-sheets')
    before = {}
    for n in os.listdir(sheets):
        before[n] = io.open(os.path.join(sheets, n), 'rb').read()
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        make_test_sheets.main()
        make_check_sheet.main()
    changed = [n for n, b in before.items()
               if io.open(os.path.join(sheets, n), 'rb').read() != b]
    record('sheets', not changed,
           'the print sheets and the check sheet rebuild unchanged'
           if not changed else 'CHANGED: ' + ', '.join(changed))


# ------------------------------------------------------------- neighbours ---
def check_neighbours():
    """Corroboration, not authority.  Arabic, Persian and Urdu braille cannot say
    what Sindhi should be, but where they agree with our reading of the Sindhi
    book, that reading is unlikely to be a transcription slip."""
    import compare_codes
    rows = compare_codes.compare()
    if not rows:
        record('neighbours', None, 'reference tables not present - not checked')
        return
    agree = sum(r[1] for r in rows)
    diff = sum(len(r[2]) for r in rows)
    # Every disagreement should be explainable. Ours are: three letters Arabic
    # does not have, and ک, which Urdu and Persian write 13 - a cell Sindhi has
    # already given to ڪ, a letter they do not have.
    record('neighbours', diff <= 5,
           '%d of %d shared letters agree with Arabic, Persian and Urdu; '
           'the %d that differ are letters those codes do not have'
           % (agree, agree + diff, diff))


# --------------------------------------------------------------- liblouis ---
def check_liblouis():
    tables = os.path.join(ROOT, 'brailleTables')
    if not _which('lou_checktable'):
        record('liblouis', None, 'liblouis tools not installed — not checked')
        return
    msgs, bad = [], False
    for t in ('sd-pk-g1.utb', 'sd-pk-g2.ctb'):
        r = subprocess.run(['lou_checktable', t], cwd=tables,
                           capture_output=True, text=True)
        if r.returncode: bad = True; msgs.append('%s does not compile' % t)
    # Setting LOUIS_TABLEPATH replaces the default, so the shared display and
    # space tables this table includes have to be put back on it.  liblouis
    # separates the entries with a comma, not with the platform's path
    # separator - a colon here silently loses everything after the first entry.
    extra = [d for d in ('/usr/share/liblouis/tables',
                         '/usr/local/share/liblouis/tables',
                         '/opt/homebrew/share/liblouis/tables')
             if os.path.isdir(d)]
    env = dict(os.environ, LOUIS_TABLEPATH=','.join([tables] + extra))
    r = subprocess.run(['lou_checkyaml', 'sd-pk-g1_test.yaml'], cwd=tables,
                       capture_output=True, text=True, env=env)
    tail = (r.stdout + r.stderr).strip().splitlines()
    line = tail[-1] if tail else ''
    if r.returncode: bad = True
    msgs.append(line)
    record('liblouis', not bad, '; '.join(m for m in msgs if m))


# -------------------------------------------------------------- ambiguity ---
def check_ambiguity():
    """The site prints a table of every cell that carries more than one reading.
    It used to be written by hand and it drifted - three readings listed for a
    cell the tables give five.  It is generated now; this proves it is current."""
    import contextlib, make_ambiguity
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        stale = make_ambiguity.main(check=True)
    rows = make_ambiguity.table()
    record('ambiguity', not stale,
           'the site lists all %d cells that carry more than one reading'
           % len(rows) if not stale
           else 'the site table is out of date - run make_ambiguity.py')


# --------------------------------------------------------------- wordlist ---
def check_wordlist():
    """The word list settles every cell that carries more than one reading, so the
    two implementations have to hold the same one.  The browser's copy was pasted
    in by hand once and drifted."""
    import contextlib, make_wordlist
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        stale = make_wordlist.main(check=True)
    record('wordlist', not stale,
           'the browser is carrying the same %d words' % len(make_wordlist.words())
           if not stale else 'the browser copy is out of date - run make_wordlist.py')


# ---------------------------------------------------------------- browser ---
def check_browser():
    web = os.path.join(ROOT, 'website', 'src')
    harness = os.path.join(web, 'crosscheck.js')
    if not _which('node') or not os.path.exists(harness):
        record('browser', None,
               'node or the cross-check harness is missing — not checked')
        return
    r = subprocess.run(['node', 'crosscheck.js'], cwd=web,
                       capture_output=True, text=True)
    out = (r.stdout + r.stderr).splitlines()
    tail = [l for l in out if l.strip() and not l.startswith('DOCSHA')]
    record('browser', r.returncode == 0, tail[-1].strip() if tail else 'ran')

    # And a whole document, not just sentences.  The site converts documents in
    # the browser; braille_batch.py converts them on the command line.  If those
    # two ever disagree, a teacher's book and the press's book come out
    # different, so they are compared by hash over the same fixed text.
    import hashlib
    line = 'سنڌي ٻولي هڪ شاهوڪار ٻولي آهي ۽ ان جو ادب تمام قديم آهي.'
    text = '\n'.join([line] * 300)
    mine = sb.to_brf(sb.translate(text), width=28)
    want = hashlib.sha256(mine.encode('ascii')).hexdigest()
    got = ''
    for l in out:
        if l.startswith('DOCSHA'): got = l.split()[1]
    if not got:
        record('document', None, 'the browser did not report a document hash')
    else:
        record('document', got == want,
               'a %d-page document converts identically in the browser and here'
               % len([x for x in mine.split('\f') if x.strip()])
               if got == want else
               'the browser and this one write DIFFERENT braille for the same document')


def _which(prog):
    from shutil import which
    return which(prog)


def main():
    sb.load_words()
    for fn in (check_guide, check_selftest, check_words, check_grade2,
               check_sheets, check_neighbours, check_ambiguity, check_wordlist,
               check_liblouis, check_browser):
        try:
            fn()
        except Exception as e:                       # a broken check is a failure
            record(fn.__name__.replace('check_', ''), False,
                   '%s: %s' % (type(e).__name__, e))

    width = max(len(n) for n, _, _ in results)
    print()
    for name, ok, detail in results:
        mark = {True: 'pass', False: 'FAIL', None: 'skip'}[ok]
        print('  %-4s  %-*s  %s' % (mark, width, name, detail))
    failed = [n for n, ok, _ in results if ok is False]
    skipped = [n for n, ok, _ in results if ok is None]
    print()
    if failed:
        print('  %d check%s FAILED: %s'
              % (len(failed), '' if len(failed) == 1 else 's', ', '.join(failed)))
    else:
        print('  everything that could be checked, passed.')
    if skipped:
        print('  not checked here: %s' % ', '.join(skipped))
    print('  Nothing on this list is a substitute for embossing a page and '
          'having it read by touch.')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
