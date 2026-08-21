# How to type a book for this pipeline

**For the person typing. You do not need to know braille.** Type the Sindhi as
it appears in the printed book, and add a few markers so the software knows what
it is looking at.

Save each lesson as one plain text file in `book/`, UTF-8, named
`01-lesson.txt`, `02-lesson.txt` and so on.

## The markers

Every marker starts with `@` at the beginning of a line.

```
@page 7
```
**The page number in the printed book.** Put one before the text of every printed
page. This is the most important marker in the file and the reason is in
`docs/BOOK-PLAN.md`: it is what lets the figures be added later without
re-typing anything.

```
@heading سبق پهريون
```
A heading. It gets a blank line before it and is not run into the text.

```
@figure ڇوڪري ڪتاب پڙهي رهي آهي
```
**A picture stood here.** Describe it in one short Sindhi phrase, or leave the
description empty if you do not want to describe it. The braille page will carry
a short note in its place, so nobody wonders whether a page is missing.

```
@exercise 3 هيٺين لفظن کي پڙهو
```
An exercise, with its number as printed in the book. Keep the number even if the
exercise cannot be done without the picture, so nothing shifts.

```
@blank
```
A deliberate blank line in the printed book.

```
# anything after a hash is a note to yourself and is ignored
```

## Everything else is text

Any line that does not start with `@` or `#` is Sindhi text. Type it as printed,
including punctuation. Do not try to lay it out: do not add extra spaces to
centre a heading, and do not break a line early. The software decides where the
braille lines end, because that depends on the paper.

## What not to do

- **Do not skip a page.** If a printed page is entirely picture, still write
  `@page 12` and then `@figure ...`, so the count stays right.
- **Do not renumber anything.** Exercise 5 stays exercise 5 even if exercise 4
  was dropped.
- **Do not correct the book.** If the printed book has a mistake, type the
  mistake and put a `#` note beside it. Someone else decides what to do about it.

## A worked example

```
# Sindhi Book 1, lesson 1
@page 7
@heading سبق پهريون
@figure هڪ ٻلي
هي ٻلي آهي.
ٻلي ننڍي آهي.

@page 8
@exercise 1 هيٺيان لفظ پڙهو
ٻلي
ڪتاب
پاڻي
@figure ٽي شيون: ٻلي، ڪتاب، پاڻي
```

## Then

```
python tools/make_book.py book --width 38 --out book/out
```

That writes the `.brf` for the embosser and a teacher's copy in HTML showing the
printed page numbers, the Sindhi, the braille and the dot numbers side by side,
so a sighted teacher who reads no braille can still check the page.
