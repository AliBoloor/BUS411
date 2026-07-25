# Repository guidance for coding agents

## Purpose

This repository contains the BUS 411 Quarto course website and its published output.
Keep changes focused, reproducible, and safe for a public teaching repository.

## Source and output conventions

- Edit course sources in `index.qmd`, `course_outline/`, `lecture_notes/`,
  `assignments/`, `demos/`, and the root documentation files.
- Treat `docs/` as generated public output. Do not hand-edit it; render the relevant
  source instead.
- Keep the `problem_sets/` folder. Do not remove it during cleanup.
- Do not commit transient Quarto, LaTeX, Jupyter, R, IDE, or operating-system files.
- Keep generated HTML/PDF files out of source directories unless explicitly needed.

## Private material

- The entire `exams/` directory is local-only and must never be force-added.
- Assignment solutions, answer keys, drafts, data, and generated answer files are
  local-only. Only explicitly unignored assignment question sources are public.
- Before any commit or push, run `git status --short --ignored` and verify ignored
  exams and solutions are absent from staged changes.

## Editing and validation

- Preserve existing lecture numbering and mathematical notation.
- Numerical examples should show formulas, substitutions, units, and interpretation.
- Keep question text identical between a problem file and its solution file.
- Render every modified Quarto source in each relevant format.
- For layout-sensitive PDF changes, visually inspect the rendered pages.
- Do not modify unrelated files or delete teaching sources without explicit approval.

## Common commands

```bash
quarto preview
quarto render --to html
LC_ALL=C LANG=C quarto render --to pdf --no-clean
git status --short --ignored
```

The public website is served from `docs/` on the `main` branch.
