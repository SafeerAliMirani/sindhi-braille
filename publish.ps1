# Publish the project: GitHub, then Cloudflare Pages.
#
#   1. Make the empty repository first, in a browser:
#        https://github.com/new
#        Name:        sindhi-braille
#        Visibility:  Public
#        Do NOT tick "Add a README", ".gitignore" or "licence" — they are here already.
#
#   2. Then run this file from the project folder, in PowerShell:
#        cd "E:\Sindhi Braille Project"
#        .\publish.ps1
#
# It will not publish Riaz's books, the Authority's guide or the photographs.
# .gitignore keeps those out; the script checks before pushing and stops if any
# of them are staged.

$ErrorActionPreference = "Stop"
$repo = "sindhi-braille"
$user = "SafeerAliMirani"

Write-Host "`n== checking git ==" -ForegroundColor Cyan
git --version
if ($LASTEXITCODE -ne 0) {
  Write-Host "git is not installed. Get it from https://git-scm.com/download/win and run this again." -ForegroundColor Red
  exit 1
}

Write-Host "`n== running the checks before anything is published ==" -ForegroundColor Cyan
python tools\check_all.py
if ($LASTEXITCODE -ne 0) {
  Write-Host "A check failed. Nothing has been pushed. Fix it first." -ForegroundColor Red
  exit 1
}

if (-not (Test-Path .git)) {
  Write-Host "`n== first time: creating the repository ==" -ForegroundColor Cyan
  git init
  git branch -M main
  git remote add origin "https://github.com/$user/$repo.git"
} else {
  Write-Host "`n== repository already exists here ==" -ForegroundColor Cyan
}

git add -A

Write-Host "`n== what would be published ==" -ForegroundColor Cyan
$staged = git diff --cached --name-only
$count  = ($staged | Measure-Object).Count
Write-Host "$count files"

# nothing of his, nothing of theirs
$forbidden = $staged | Where-Object { $_ -like "official-code/source/*" -or $_ -like "photos/*" -or $_ -like "_to_delete/*" }
if ($forbidden) {
  Write-Host "`nSTOPPED. These are not ours to publish:" -ForegroundColor Red
  $forbidden | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
  Write-Host "Check .gitignore, then run: git reset" -ForegroundColor Red
  exit 1
}
Write-Host "No books, no photographs, nothing of the Authority's. Good." -ForegroundColor Green

$msg = Read-Host "`nCommit message (Enter for the default)"
if (-not $msg) { $msg = "Standard Sindhi Braille: translator, liblouis tables, specification and site" }

git commit -m "$msg"
Write-Host "`n== pushing ==" -ForegroundColor Cyan
git push -u origin main

Write-Host "`nDone. https://github.com/$user/$repo" -ForegroundColor Green
Write-Host @"

NEXT — Cloudflare Pages, in a browser, once:

  1. https://dash.cloudflare.com  ->  Workers & Pages  ->  Create  ->  Pages
  2. Connect to Git, pick $repo
  3. Framework preset:          None
     Build command:             (leave empty)
     Build output directory:    website
  4. Save and Deploy

  It will be live at https://$repo.pages.dev and will rebuild on every push.
  The _headers file in website/ is picked up automatically.
"@ -ForegroundColor Yellow
