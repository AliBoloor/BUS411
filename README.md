# BUS 411 — Fixed Income Security Analysis and Valuation

**[View the course website →](https://aliboloor.github.io/BUS411/)**

Course materials and lecture notes for **BUS 411: Fixed Income Security Analysis and Valuation**.

## Overview

This repository contains:

- **Lecture notes** (`.qmd` format) in `lecture_notes/`
- Public assignment questions, plus local-only assignment drafts and exam materials
- A **Quarto website** that builds into `docs/` for GitHub Pages

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) (recommended: latest stable version)

## Preview Locally

To preview the course website locally:

```bash
quarto preview
```

This starts a local server; the site will open in your browser and auto-refresh on changes.

## Render and Publish the Website

The published site is rendered locally and committed to `docs/`. GitHub Pages serves that directory directly; GitHub Actions does not render the site.

First, render the complete website HTML:

```bash
quarto render --to html
```

Output is written to the `docs/` directory. For GitHub Pages, configure your repository to serve the site from the `docs/` folder (Settings → Pages → Source: Deploy from a branch → Branch: main, folder: /docs).

Then render the public PDFs separately:

```bash
LC_ALL=C LANG=C quarto render course-outline.md --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec1.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec2.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec3.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec4.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec5.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec6.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec7.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec8.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec9.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec10.qmd --to pdf
LC_ALL=C LANG=C quarto render assignments/assignment1/assignment-1-questions.qmd --to pdf
LC_ALL=C LANG=C quarto render assignments/assignment2/assignment-2-questions.qmd --to pdf
```

PDF output requires a LaTeX distribution such as TinyTeX or full TeX Live. After checking the generated pages and PDFs, commit the source changes and the updated `docs/` output together, then push to `main`.

## Structure

- `lecture_notes/` — Lecture content (`.qmd` files)
- `slides/` — Presentation slides
- `assignments/` — Public assignment questions; drafts and data files are local-only
- `problem_sets/` — Problem sets
- `labs/` — Lab exercises
- `exams/` — Local-only exam materials
- `assets/` — Images, figures, PDFs, and data files
- `docs/` — Rendered website output (for GitHub Pages)
