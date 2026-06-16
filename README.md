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

## Render the Website

To render the website HTML:

```bash
quarto render --to html
```

Output is written to the `docs/` directory. For GitHub Pages, configure your repository to serve the site from the `docs/` folder (Settings → Pages → Source: Deploy from a branch → Branch: main, folder: /docs).

## Render Public PDFs

The GitHub Action renders the public PDFs after the HTML site. To reproduce that locally, render the same selected targets:

```bash
LC_ALL=C LANG=C quarto render course-outline.md --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec1.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec2.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec3.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec4.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec5.qmd --to pdf
LC_ALL=C LANG=C quarto render lecture_notes/lec6.qmd --to pdf
LC_ALL=C LANG=C quarto render assignments/assignment1/assignment-1-questions.qmd --to pdf
```

PDF output requires a LaTeX distribution such as TinyTeX or full TeX Live. The CI workflow renders each public PDF as a separate matrix job so one LaTeX or notebook failure identifies the specific source file and does not block the HTML render.

## Structure

- `lecture_notes/` — Lecture content (`.qmd` files)
- `slides/` — Presentation slides
- `assignments/` — Public assignment questions; drafts and data files are local-only
- `problem_sets/` — Problem sets
- `labs/` — Lab exercises
- `exams/` — Local-only exam materials
- `assets/` — Images, figures, PDFs, and data files
- `docs/` — Rendered website output (for GitHub Pages)
