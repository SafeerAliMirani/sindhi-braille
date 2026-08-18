# Third-party tables

The files in this folder are **not part of this project**. They are braille
tables from [liblouis](https://github.com/liblouis/liblouis), written by other
people for other languages, and each carries its own copyright notice and
licence inside the file.

They are here for one reason: `tools/compare_codes.py` checks the Sindhi letters
against Arabic, Persian and Urdu braille. That check is the only one in the
project that uses evidence neither author produced, and it is the reason the ک
finding could be corroborated independently.

| file | language | copyright |
|---|---|---|
| `ar-ar-g1-core.uti`, `ar-ar-g1.utb` | Arabic | see the header of each file |
| `fa-ir-g1.utb` | Persian | see the header of each file |
| `ur-pk-g1.utb` | Urdu | Compass Braille, 2018–2023 |
| `en-ueb-g1.ctb`, `en-us-g1.ctb` | English | see the header of each file |

liblouis is distributed under the LGPL. If you would rather not carry these
copies, delete the folder — `check_all.py` will report the `neighbours` check as
skipped rather than failing, and everything else runs unchanged.
