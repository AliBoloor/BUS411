---
title: "Syllabus"
subtitle: "BUS 411 — Fixed Income Security Analysis and Valuation"
date: ""
format:
  html:
    toc: true
    toc-depth: 2
    css: course-outline.css
  pdf:
    geometry:
      - margin=1in
    fontsize: 11pt
    toc: false
    number-sections: false
    # Use block headings so # → LaTeX \section (KOMA styling below).
    block-headings: true
    # Must use `text: |` — a bare `- |` list item is treated as a *filename*, not inline TeX.
    include-in-header:
      - text: |
          % Syllabus PDF styling (see also course-outline-pdf-header.tex for a copy)
          \makeatletter
          \usepackage{enumitem}
          \setlist[enumerate]{itemsep=0.12ex, topsep=0.35ex, parsep=0pt, partopsep=0pt}
          \date{}%
          \AtBeginDocument{%
            \IfFontExistsTF{Arial}{%
              \setmainfont{Arial}[Ligatures=TeX]%
            }{%
              \setmainfont{TeX Gyre Heros}[Ligatures=TeX]%
            }%
          }
          \RedeclareSectionCommand[
            beforeskip=-0.85\baselineskip plus -0.15\baselineskip minus 0.08\baselineskip,
            afterskip=0.12\baselineskip
          ]{section}
          \setkomafont{section}{\normalfont\Large\bfseries\color[HTML]{C00000}}
          \renewcommand{\sectionlinesformat}[4]{%
            \@hangfrom{\hskip #2#3}{#4}%
            \par\nobreak
            \vspace{-0.78\baselineskip}%
            \noindent{\color[HTML]{4472C4}\rule{\linewidth}{0.55pt}}%
            \par
            \vspace{0.03\baselineskip}%
          }
          \makeatother
---
# Course Information

**Instructor:** Ali Boloor\
**Semester:** Summer 2026\
**Email:** [aboloorf@sfu.ca](mailto:aboloorf@sfu.ca)\
**LMS:** [Canvas](https://canvas.sfu.ca/); [course website](https://aliboloor.github.io/BUS411/)\
**Lectures:** Tuesdays, 2:30–5:20 p.m.\
**Office hours:** Tuesdays, 1:30–2:20 p.m. (by appointment only)\
**Office:** WMC 4394

# Course Description

This course introduces the market valuation of fixed income securities. Topics include the history of fixed income markets; valuation methods for fixed and variable annuities, government and corporate bonds, and bonds with contingencies; credit risk modeling; fixed income derivatives; and risk management using duration and convexity.

**Prerequisite:** BUS 315 and BUS 360W, each with a minimum grade of C-; 60 units.

# Required Textbook

Fabozzi, F. J. (2015). *Bond markets, analysis, and strategies* (9th ed.). Pearson. ISBN 978-0-13-379677-3.

# Class Format

Classes are primarily lecture-based; discussion is encouraged. Materials include slides and lecture notes. You are expected to review the assigned readings and textbook chapters before each class.

# Assessment

| Component | Weight |
|:----------|-------:|
| Exam 1 | 35% |
| Exam 2 | 35% |
| Assignment 1 | 15% |
| Assignment 2 | 15% |

# Important Dates
| Item                | Date           |
|---------------------|---------------|
| Exam 1              | June 23, 2026 |
| Exam 2              | August 4, 2026 |
| Assignment 1 Due    | June 23, 2026 |
| Assignment 2 Due    | August 4, 2026 |

# Topics

1. Introduction
2. Bond pricing and yields
3. Bond price volatility
4. Term structure and curve strategies
5. Treasury securities and corporate debt instruments
6. Bond portfolio construction
7. Interest-rate models
8. Embedded options
9. Interest-rate futures
10. Credit spread exposure and credit risk modeling
11. Interest-rate options

# Academic Honesty

Plagiarism is the unacknowledged use of other people’s ideas or work. It is often unintentional and can be avoided through careful habits and familiarity with academic conventions. Whether intentional or not, plagiarism is a serious academic offence. The university’s stance reflects a shared commitment to intellectual honesty; original work by students and faculty sustains the university as a centre of knowledge and research. It is your responsibility to acknowledge and cite all resources you use.

Representative examples of academic dishonesty include:

- Presenting another person’s work as your own (plagiarism).
- Submitting the same work more than once without prior approval.
- Translating a work from one language to another without complete and proper citation.
- Cheating.
- Impersonation (e.g., having someone else write your exam).
- Submitting false records or information (e.g., forged medical notes).
- Stealing or destroying another student’s work.
- Unauthorized or inappropriate use of computers, phones, calculators, or other technology in coursework, assignments, or examinations.
- Falsifying material subject to academic evaluation.
- Any activity intended to circumvent standards of academic honesty, even if not listed here.

You are expected to post comments and to write reports and exams in your own words. Whenever you use an idea or wording from another source, cite it appropriately. If you are struggling with an assignment, contact the instructor or the program office for help.

Ignorance of these standards does not excuse academic dishonesty.

The full SFU policy on academic honesty is available here: [SFU policies — student academic integrity](https://www.sfu.ca/policies/gazette/student.html).
