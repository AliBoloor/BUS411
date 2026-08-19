# BUS 411 — Fixed Income Security Analysis and Valuation

**[View the course website](https://aliboloor.github.io/BUS411/)**

Quarto sources and published materials for BUS 411. The course currently contains
11 lectures covering bond valuation, fixed-income markets, portfolio construction,
interest-rate models, embedded options, futures, credit risk, and interest-rate
options. See [Topics.md](Topics.md) for the lecture-by-lecture map.

## Repository layout

- `lecture_notes/` — source notes for Lectures 1–11 and source appendices
- `course_outline/` — syllabus source, stylesheet, and PDF header reference
- `assignments/` — public assignment questions; answers and working data stay local
- `team_projects/` — repository-only project materials, excluded from the public website
- `problem_sets/` — cumulative practice sets for Lectures 1–6 and 7–11
- `problem_sets/` — public cumulative practice material
- `demos/` — practical, reproducible fixed-income workflows
- `assets/` — shared data, images, figures, and PDFs
- `slides/` — reveal.js lecture-deck sources
- `labs/` — reserved course-material folder
- `exams/` — local-only exams and solutions; ignored by Git
- `docs/` — rendered public website served by GitHub Pages

## Public and local-only material

The repository intentionally publishes assignment questions but not assignment
solutions. The entire `exams/` directory and all non-question files inside assignment
folders are ignored. Before committing, verify this policy with:

```bash
git status --short --ignored
git check-ignore -v exams/exam-2.qmd assignments/assignment2/assignment-2-answers.qmd
```

Do not force-add ignored exams, solutions, answer keys, or private grading material.

## Requirements

- Quarto
- Python packages listed in `requirements.txt`
- A LaTeX distribution such as TinyTeX or TeX Live for PDF output

## Preview locally

```bash
quarto preview
```

## Render the public website

The public site is rendered locally into `docs/` and committed. GitHub Pages serves
the `docs/` directory from `main`.

```bash
quarto render --to html
```

Reveal.js decks use their own format and are rendered separately after the website
build. Copy the resulting self-contained HTML decks into the public site:

```bash
for lecture in {1..11}; do
  quarto render "slides/lec${lecture}-slides.qmd"
done
cp slides/lec*-slides.html docs/slides/
```

Render public PDFs after the HTML build. The `--no-clean` flag is required so the
PDF pass does not remove the HTML website from `docs/`:

```bash
LC_ALL=C LANG=C quarto render --to pdf --no-clean
```

After rendering, inspect the changed HTML/PDF files, confirm ignored private material
is absent from the staged changes, and commit source and `docs/` output together.
