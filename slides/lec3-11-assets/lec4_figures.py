"""Reproduce Lecture 4 figures using the original note data; lecture notes are read-only."""
from build_figures import *
from cycler import cycler
plt.rcParams["axes.prop_cycle"] = cycler(color=[GREEN, GOLD, BLUE, "#85618b"])
#| label: fig-benchmark-spread
#| fig-cap: "Yield decomposition into a base interest rate and a benchmark spread."
#| echo: false
#| warning: false
#| message: false

import matplotlib.pyplot as plt

base_rate = 3.80
benchmark_spread = 1.25
required_yield = base_rate + benchmark_spread

fig, ax = plt.subplots(figsize=(13,5.4))
labels = ["Treasury benchmark", "Corporate bond"]
yields = [base_rate, required_yield]
colors = [GREEN, GOLD]

ax.scatter(labels, yields, s=160, color=colors, zorder=3)
ax.plot(labels, yields, color="#666666", linewidth=2, alpha=0.6, zorder=2)

for label, yld in zip(labels, yields):
    ax.text(label, yld + 0.14, f"{yld:.2f}%", ha="center", va="bottom", fontsize=18)


ax.axhline(base_rate, color=GREEN, linestyle="--", linewidth=1, alpha=0.7)
ax.set_ylabel("Yield (%)")
ax.set_ylim(0, 5.6)
ax.set_title("Corporate Bond Yield = Benchmark Rate + Spread")
ax.grid(axis="y", alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-benchmark-spread')

#| label: fig-maturity-spreads
#| fig-cap: "Illustrative yields across maturity sectors and the maturity spread."
#| echo: false
#| warning: false
#| message: false

import matplotlib.pyplot as plt

sectors = ["Short term\n(2-year)", "Intermediate\n(10-year)", "Long term\n(20-year)"]
yields = [3.80, 4.35, 4.75]

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(sectors, yields, marker="o", linewidth=2, color=GREEN)

for sector, yld in zip(sectors, yields):
    ax.text(sector, yld + 0.06, f"{yld:.2f}%", ha="center", va="bottom")


ax.set_ylabel("Yield (%)")
ax.set_ylim(3.4, 5.1)
ax.set_title("Yields Often Differ Across Maturity Sectors")
ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-maturity-spreads')

#| label: fig-yield-curves
#| fig-cap: "Common yield curve shapes."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

m = np.array([0.5, 1, 2, 3, 5, 7, 10, 20, 30])
upward = np.array([3.0, 3.2, 3.5, 3.7, 4.0, 4.15, 4.30, 4.50, 4.60])
flat = np.array([4.0, 4.02, 4.03, 4.02, 4.01, 4.00, 4.00, 4.01, 4.02])
inverted = np.array([5.0, 4.9, 4.7, 4.5, 4.25, 4.10, 3.95, 3.80, 3.75])
humped = np.array([3.4, 3.7, 4.1, 4.35, 4.25, 4.10, 3.95, 3.85, 3.80])

fig, ax = plt.subplots(figsize=(13,5.4))
for curve, label in [(upward, "Upward sloping"), (flat, "Flat"), (inverted, "Inverted"), (humped, "Humped")]:
    ax.plot(m, curve, marker="o", label=label)
ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Yield Curve Shapes")
ax.grid(alpha=0.25)
ax.legend()
save(fig, 'lec4-fig-yield-curves')

#| label: fig-bootstrapped-spot-curve
#| fig-cap: "Observed YTMs are smoothed and interpolated into a par curve, then bootstrapped into a spot curve."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

observed_maturities = np.array([0.5, 1, 2, 3, 5, 7, 10])
observed_ytm = np.array([3.58, 3.82, 4.08, 4.38, 4.57, 4.78, 4.88])
par_maturities = np.arange(0.5, 10.5, 0.5)
par_curve = np.array([
    3.600, 3.800, 3.950, 4.100, 4.225,
    4.350, 4.412, 4.475, 4.537, 4.600,
    4.637, 4.675, 4.713, 4.750, 4.775,
    4.800, 4.825, 4.850, 4.875, 4.900,
])
spot_curve = np.array([
    3.600, 3.802, 3.954, 4.108, 4.237,
    4.367, 4.432, 4.497, 4.564, 4.631,
    4.671, 4.711, 4.752, 4.793, 4.820,
    4.848, 4.876, 4.904, 4.933, 4.963,
])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.scatter(observed_maturities, observed_ytm, color="#666666", label="Observed Treasury YTMs", zorder=3)
ax.plot(par_maturities, par_curve, marker="o", markersize=3, color=GREEN, label="Smoothed/interpolated par curve")
ax.plot(par_maturities, spot_curve, marker="s", markersize=3, color=GOLD, label="Bootstrapped spot curve")
ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Rate (%)")
ax.set_title("From Observed YTMs to Semiannual Spot Rates")
ax.set_xticks([0.5, 1, 2, 3, 5, 7, 10])
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-bootstrapped-spot-curve')

#| label: fig-forward-rates
#| fig-cap: "Forward rates implied by an upward-sloping spot curve."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

periods = np.array([1, 2, 3, 4, 5, 6])
spot = np.array([0.018, 0.020, 0.022, 0.024, 0.025, 0.026])
forward = [spot[0]]
for i in range(1, len(spot)):
    f = ((1 + spot[i]) ** (i + 1) / (1 + spot[i - 1]) ** i) - 1
    forward.append(f)
forward = np.array(forward)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(periods / 2, spot * 2 * 100, marker="o", label="Annualized spot rates")
ax.plot(periods / 2, forward * 2 * 100, marker="s", label="Annualized six-month forwards")
ax.set_xlabel("Maturity / forward end date (years)")
ax.set_ylabel("Annualized rate (%)")
ax.set_title("Spot Rates and Implied Forward Rates")
ax.grid(alpha=0.25)
ax.legend()
save(fig, 'lec4-fig-forward-rates')

#| label: fig-curve-drivers
#| fig-cap: "Illustrative effects of rate expectations on the yield curve."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

m = np.array([0.5, 1, 2, 5, 10, 30])
base = np.array([4.2, 4.1, 4.0, 4.1, 4.3, 4.5])
tightening = np.array([5.0, 4.9, 4.7, 4.4, 4.35, 4.45])
easing = np.array([3.2, 3.3, 3.5, 3.9, 4.2, 4.45])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(m, base, marker="o", label="Current curve")
ax.plot(m, tightening, marker="o", label="Tightening priced in")
ax.plot(m, easing, marker="o", label="Easing priced in")
ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Rate Expectations Can Change Curve Shape")
ax.grid(alpha=0.25)
ax.legend()
save(fig, 'lec4-fig-curve-drivers')

#| label: fig-swap-curve
#| fig-cap: "Illustrative Treasury and swap curves."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

m = np.array([1, 2, 3, 5, 7, 10, 20, 30])
treasury = np.array([3.9, 4.0, 4.05, 4.15, 4.22, 4.30, 4.45, 4.55])
swap = treasury + np.array([0.30, 0.34, 0.36, 0.38, 0.39, 0.40, 0.36, 0.32])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(m, treasury, marker="o", label="Treasury curve")
ax.plot(m, swap, marker="s", label="Swap curve")
ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Rate (%)")
ax.set_title("Swap Rate Yield Curve")
ax.grid(alpha=0.25)
ax.legend()
save(fig, 'lec4-fig-swap-curve')

#| label: fig-bull-steepener
#| fig-cap: "Bull steepener: yields fall, with the short end falling more than the long end."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([2, 5, 10, 30])
initial = np.array([4.80, 4.55, 4.20, 4.25])
after = np.array([4.10, 4.15, 3.95, 4.05])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(maturities, initial, marker="o", linewidth=2, label="Initial curve")
ax.plot(maturities, after, marker="o", linewidth=2, label="After bull steepener")


ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Bull Steepener")
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-bull-steepener')

#| label: fig-bear-steepener
#| fig-cap: "Bear steepener: yields rise, with the long end rising more than the short or intermediate sector."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([2, 5, 10, 30])
initial = np.array([3.90, 4.00, 4.20, 4.40])
after = np.array([3.95, 4.10, 4.45, 4.80])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(maturities, initial, marker="o", linewidth=2, label="Initial curve")
ax.plot(maturities, after, marker="o", linewidth=2, label="After bear steepener")


ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Bear Steepener")
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-bear-steepener')

#| label: fig-bull-flattener
#| fig-cap: "Bull flattener: yields fall, with the long end falling more than the short end."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([2, 5, 10, 30])
initial = np.array([4.50, 4.65, 4.90, 5.10])
after = np.array([4.35, 4.35, 4.40, 4.55])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(maturities, initial, marker="o", linewidth=2, label="Initial curve")
ax.plot(maturities, after, marker="o", linewidth=2, label="After bull flattener")


ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Bull Flattener")
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-bull-flattener')

#| label: fig-bear-flattener
#| fig-cap: "Bear flattener: yields rise, with the short end rising more than the long end."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([2, 5, 10, 30])
initial = np.array([3.80, 4.05, 4.30, 4.45])
after = np.array([4.55, 4.60, 4.55, 4.60])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(maturities, initial, marker="o", linewidth=2, label="Initial curve")
ax.plot(maturities, after, marker="o", linewidth=2, label="After bear flattener")


ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("Bear Flattener")
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-bear-flattener')

#| label: fig-butterfly-strategy
#| fig-cap: "Butterfly trade: the intermediate maturity richens relative to the wings."
#| echo: false
#| warning: false
#| message: false

import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([2, 5, 10])
initial = np.array([4.00, 4.50, 4.30])
after = np.array([4.05, 4.15, 4.25])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(maturities, initial, marker="o", linewidth=2, label="Initial curve")
ax.plot(maturities, after, marker="o", linewidth=2, label="After 5-year richens")
ax.vlines(5, after[1], initial[1], color="#333333", linestyle="--", linewidth=1.3)
ax.set_xlabel("Maturity (years)")
ax.set_ylabel("Yield (%)")
ax.set_title("2s5s10s Butterfly")
ax.set_xticks(maturities)
ax.grid(alpha=0.25)
ax.legend()
ax.spines[["top", "right"]].set_visible(False)
save(fig, 'lec4-fig-butterfly-strategy')

