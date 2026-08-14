# BUS 411 Version 2 revision notes

This log records significant source changes made for the Version 2 course revision.
Routine spelling, punctuation, whitespace, and typographic consistency edits are
not listed individually unless they affect interpretation.

## Preservation and working method

- Untouched baseline commit: `42e3d2a` (`end of summer 2026`)
- Backup branch: `backup/bus411-pre-v2-20260813`
- Revision branch: `bus411-v2`
- Published files under `docs/` are generated outputs and are not hand-edited.
- Private exams, solutions, answer keys, and local working data remain excluded.

## Batch 1 — Lecture-source editorial review

Completed for Lectures 1–11, the futures appendix, and the lecture index. Lectures
3 and 9 and the futures appendix required no safe localized changes. Significant
corrections were:

- Lecture 1 now correctly distinguishes inflation-linked bonds from floating-rate
  bonds, and a collapsed foreign-currency carry-trade callout is readable.
- Lecture 2's total-return example now uses a 7% coupon, consistent with the quoted
  $769.40 price and 10% yield, and all return components were recalculated.
- Lecture 7 now states the conditions behind the CIR model's nonnegative-rate
  property and correctly describes a trading-day step as `1/252` of a year.
- Lecture 10's Jarrow–Turnbull, Duffie–Singleton, and incomplete-information
  sections are visible again; they had been unintentionally hidden in HTML comments.
- Other edits standardize local notation and terminology, repair malformed currency
  math, correct example numbering, and improve grammar without changing scope.

All modified lecture sources passed whitespace checks and were rendered successfully
in the course-wide HTML and PDF publication passes.

## Batch 2 — Reveal.js lecture decks

Completed for Lectures 1–11. Each deck follows the corresponding lecture's
sequence and notation while emphasizing key ideas, intuition, equations, figures,
tables, and worked examples. The shared reveal.js metadata and course theme provide
consistent navigation, typography, colors, and slide numbering.

All decks rendered successfully to the ignored `slides/_output/` validation folder
and to `docs/slides/`. The deck index links Lectures 1–11 in order. Structural HTML,
asset, density, and link checks passed. Screenshot-level inspection at 1600 x 900
was not available because the local browser security check did not grant access.

## Batch 3 — Student team projects

Created 22 projects for teams of two or three, with two choices aligned to each
lecture. Every project includes objectives, named accessible data sources, concrete
deliverables, a project-specific 100-point rubric, and a 10–12 minute presentation.
Common standards emphasize financial reasoning, limited coding, reproducibility,
attribution, scope discipline, and the distinction between analysis and investment
advice.

## Batch 4 — Practical demonstrations

Created or improved seven practical workflows covering duration and convexity,
curve bootstrapping and Hull–White calibration, Vasicek scenarios, callable-bond
OAS, Treasury futures hedging, credit-spread risk, and interest-rate options.
The demo index identifies the lecture and workflow for each demonstration.

### Second-pass demo review

- Standardized foldable HTML code and code tools across all seven demos while
  preserving visible results and PDF output.
- Reworked the curve/Hull–White workflow to begin with an embedded January 2, 2025
  U.S. Treasury par-yield snapshot, explicitly separate observed nodes from
  interpolation assumptions, bootstrap and reprice the curve, calibrate model
  dynamics, and use future fitted curves for bond valuation.
- Reworked the Vasicek workflow to estimate parameters from an embedded January
  2023–June 2025 effective-federal-funds-rate history and use the fitted distribution
  for a one-year funding-risk decision.
- Added input/estimate/diagnostic/use maps to the remaining practical cases and an
  HTML yield-shock explorer with a static PDF fallback to the duration demo.

## Course-wide validation

Navigation and render-source inclusion were checked across the home page, lecture
notes, slides, demos, assignments, team projects, and practice problems. All 22
project rubrics sum to 100 points, required project sections are present, configured
source paths exist, and public links resolve to source or generated targets.

Private-material rules continue to ignore the entire `exams/` directory and all
assignment contents except explicitly approved public question files, the assignment
index, and the team-project bank.

Final publication QA completed successfully:

- The 29-source HTML site render completed with every lecture and demo code cell.
- The 29-source PDF pass completed with `--no-clean` and preserved the HTML site.
- All 11 reveal.js decks rendered in their native format and were copied to
  `docs/slides/` as self-contained HTML files.
- Public output checks found 11 slide decks, seven demo HTML pages, seven demo PDFs,
  the team-project catalog, and the cumulative practice set.
- Source whitespace checks, internal-path checks, executable-cell-label checks, and
  private-material ignore checks passed.
