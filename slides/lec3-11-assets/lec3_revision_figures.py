"""Reproduce the Section 4.2 chart and illustrate the two yield-curve slopes."""
from pathlib import Path
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]

# Execute the existing Section 4.2 figure unchanged, exporting it for the deck.
notes = (ROOT / "lecture_notes/lec3.qmd").read_text()
section = notes.split("## Measuring Convexity")[0]
blocks = re.findall(r"\x60{3}\{python\}\n(.*?)\x60{3}", section, re.S)
code = blocks[-1]
assert "Duration as a Tangent-Line Approximation" in code
code = code.replace("plt.show()", 'plt.savefig(OUT / "lec3-notes-tangent.svg", bbox_inches="tight"); plt.close()')
exec(compile(code, "lecture_notes/lec3.qmd:section-4.2", "exec"))

# Schematic rates illustrate yield differences, rather than live market observations.
plt.rcParams.update({"font.size": 17, "axes.labelsize": 18,
                     "svg.fonttype": "none", "text.color": "#183b32",
                     "axes.labelcolor": "#183b32", "axes.spines.top": False,
                     "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(9, 6))
maturities, yields = [2, 10, 30], [3, 4, 4.5]
ax.plot(maturities, yields, color="#214b3e", lw=3, marker="o", ms=10)
for t, y in zip(maturities, yields):
    ax.annotate(f"{y:.1f}%", (t, y), xytext=(0, 12),
                textcoords="offset points", ha="center")
ax.hlines([3, 4], [2, 10], [10, 30], color="#809586", ls="--", lw=1)
for x, lo, hi, label, color in [
    (10, 3, 4, "Short end\n4.0% − 3.0%\n= 100 bp", "#936724"),
    (30, 4, 4.5, "Long end\n4.5% − 4.0%\n= 50 bp", "#517fa0"),
]:
    ax.annotate("", xy=(x, hi), xytext=(x, lo),
                arrowprops={"arrowstyle": "<->", "color": color, "lw": 2})
    ax.text(x - 1.2, (lo + hi) / 2, label, ha="right", va="center",
            fontsize=16, color=color)
ax.set(xlim=(0, 33), ylim=(2.8, 4.9), xticks=maturities,
       xlabel="Maturity (years)", ylabel="Yield (%)",
       title="Illustrative curve: yield differences")
ax.grid(axis="y", alpha=.18)
fig.tight_layout()
fig.savefig(OUT / "lec3-curve-slopes.svg", bbox_inches="tight")
plt.close(fig)
