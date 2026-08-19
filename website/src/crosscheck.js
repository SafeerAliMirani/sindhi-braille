/* The site ships one file, so its engine cannot be imported. This loads
   engine.js exactly as index.html does and runs the same cases the Python
   produced, to prove the two agree. */
const fs = require('fs'), path = require('path'), os = require('os');
const src = fs.readFileSync(path.join(__dirname, 'engine.js'), 'utf8')
  + '\nmodule.exports={T,translate,back,toDots,toUnicode,toBrf};\n';
const tmp = path.join(os.tmpdir(), 'sindhi_engine_under_test.js');
fs.writeFileSync(tmp, src);
delete require.cache[tmp];
const E = require(tmp);

/* The expectations are computed by the Python on this run and handed to us as
   argv[2]. Falling back to the stored file would let a stale file pass as a
   cross-check, which is exactly the failure this replaced. */
const casesPath = process.argv[2];
if (!casesPath) {
  console.error('crosscheck.js needs the path to the expectations the Python '
    + 'just produced; run it through tools/check_all.py');
  process.exit(2);
}
const cases = JSON.parse(fs.readFileSync(casesPath, 'utf8'));
let ok = 0, bad = 0;
for (const [text, want, opts] of cases) {
  const o = opts || {};
  const got = E.back(E.translate(text, o), o.poetry, o.grade2);
  if (got === want) ok++;
  else {
    bad++;
    console.log('MISMATCH ' + JSON.stringify(text));
    console.log('  python:  ' + JSON.stringify(want));
    console.log('  browser: ' + JSON.stringify(got));
  }
}
console.log(`${ok} of ${ok + bad} cases agree between the browser and the Python`);

/* A whole document, not a sentence. The site converts documents in the browser
   and tools/braille_batch.py converts them on the command line; if those two
   ever disagree, a teacher's book and a press's book come out different. The
   text below is fixed on purpose and check_all.py builds the same one, so the
   two sides can be compared by hash rather than by eye. */
const DOCLINE = 'سنڌي ٻولي هڪ شاهوڪار ٻولي آهي ۽ ان جو ادب تمام قديم آهي.';
const DOCTEXT = Array(300).fill(DOCLINE).join('\n');
const docBrf = E.toBrf(E.translate(DOCTEXT, {}), 28);
const sha = require('crypto').createHash('sha256').update(docBrf, 'binary').digest('hex');
console.log('DOCSHA ' + sha + ' ' + docBrf.length);

process.exit(bad ? 1 : 0);
