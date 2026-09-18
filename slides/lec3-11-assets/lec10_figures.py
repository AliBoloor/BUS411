"""Lecture 10 figures reproduce the source examples and simulation seeds."""

from build_figures import *

#| label: fig-credit-risk-map
#| fig-cap: "Corporate bond risk combines Treasury-rate exposure, spread exposure, and default exposure"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13,5.4))
ax.set_axis_off()

boxes = [
    ("Corporate\nbond price", 2.7, 1.65, "#E8F1FA"),
    ("Treasury\nrates", 0.35, 0.55, "#F6E8C3"),
    ("Credit\nspreads", 2.7, 0.55, "#E6F2E6"),
    ("Default and\nrecovery risk", 5.05, 0.55, "#F8D7DA"),
]

for text, x, y, color in boxes:
    box = FancyBboxPatch(
        (x, y), 1.45, 0.72,
        boxstyle="round,pad=0.08",
        linewidth=1.1,
        edgecolor="black",
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(x + 0.725, y + 0.36, text, ha="center", va="center", fontsize=17)

for start, end in [((1.8, 0.92), (2.8, 1.68)), ((3.45, 1.27), (3.45, 1.65)), ((5.1, 0.92), (4.05, 1.68))]:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.3))

ax.text(0.2, 0.16, "Duration", fontsize=17, color="#444444")
ax.text(2.48, 0.16, "Spread duration, DTS", fontsize=17, color="#444444")
ax.text(4.72, 0.16, "Credit risk models", fontsize=17, color="#444444")
ax.set_xlim(0, 6.8)
ax.set_ylim(0, 2.65)
plt.tight_layout()
save(plt.gcf(),"lec10-fig-credit-risk-map")


#| label: fig-absolute-relative-spreads
#| fig-cap: "The same absolute spread move can be a very different relative spread shock"
import numpy as np
import matplotlib.pyplot as plt

spreads_bps = np.array([50, 150, 300, 500])
move_bps = 25
relative_move = move_bps / spreads_bps

fig, axes = plt.subplots(1, 2, figsize=(13,5.4))
axes[0].bar(spreads_bps.astype(str), np.repeat(move_bps, len(spreads_bps)), color="#4C78A8", edgecolor="black")
axes[0].set_title("Absolute move")
axes[0].set_ylabel("Basis points")
axes[0].set_xlabel("Starting spread (bps)")
axes[0].set_ylim(0, 32)

axes[1].bar(spreads_bps.astype(str), relative_move * 100, color="#F58518", edgecolor="black")
axes[1].set_title("Relative move")
axes[1].set_ylabel("Percent of starting spread")
axes[1].set_xlabel("Starting spread (bps)")
axes[1].set_ylim(0, 60)

for ax in axes:
    ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
save(plt.gcf(),"lec10-fig-absolute-relative-spreads")


#| label: fig-portfolio-dts
#| fig-cap: "Market value weights can hide where credit spread risk is concentrated"
import numpy as np
import matplotlib.pyplot as plt

sectors = ["A industrials", "BBB financials", "High yield"]
weights = np.array([0.50, 0.30, 0.20])
dts = np.array([0.072, 0.10, 0.15])
contrib = weights * dts

x = np.arange(len(sectors))
width = 0.36

fig, ax = plt.subplots(figsize=(13,5.4))
ax.bar(x - width / 2, weights * 100, width, label="Market weight", color="#4C78A8", edgecolor="black")
ax.bar(x + width / 2, contrib * 100, width, label="Contribution to DTS", color="#F58518", edgecolor="black")
ax.set_xticks(x)
ax.set_xticklabels(sectors)
ax.set_ylabel("Percent")
ax.set_title("Portfolio weights versus contribution to DTS")
ax.grid(axis="y", alpha=0.3)
ax.legend()
plt.tight_layout()
save(plt.gcf(),"lec10-fig-portfolio-dts")


#| label: fig-empirical-duration-regression
#| fig-cap: "Stylized empirical duration regressions: investment-grade bonds usually have steeper Treasury-rate sensitivity than high-yield bonds"
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(411)
dy_bps = np.linspace(-40, 40, 41)
dy_decimal = dy_bps / 10000

duration_ig = 6.0
duration_hy = 1.8

ig_returns = -duration_ig * dy_decimal + rng.normal(0, 0.0015, size=dy_decimal.size)
hy_returns = -duration_hy * dy_decimal + rng.normal(0, 0.0040, size=dy_decimal.size)

ig_fit = np.polyfit(dy_bps, ig_returns * 100, 1)
hy_fit = np.polyfit(dy_bps, hy_returns * 100, 1)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.scatter(dy_bps, ig_returns * 100, color="#4C78A8", alpha=0.75, label="Investment grade")
ax.scatter(dy_bps, hy_returns * 100, color="#F58518", alpha=0.75, label="High yield")
ax.plot(dy_bps, np.polyval(ig_fit, dy_bps), color="#4C78A8", linewidth=2.0)
ax.plot(dy_bps, np.polyval(hy_fit, dy_bps), color="#F58518", linewidth=2.0)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Change in Treasury yield (bps)")
ax.set_ylabel("Corporate bond return (%)")
ax.set_title("Convert the regression slope to consistent rate units")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
save(plt.gcf(),"lec10-fig-empirical-duration-regression")


#| label: fig-estimating-duration-multiplier
#| fig-cap: "Estimating duration multipliers across many bonds"
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(411)
ink = "#17324D"
blue = "#2F78B7"
gold = "#D79B28"
grey = "#68727D"
grid = "#D9DEE3"

fig, axes = plt.subplots(1, 3, figsize=(23,6))

# Create a cross-section of illustrative bonds.
number_of_bonds = 18
spreads = np.linspace(55, 560, number_of_bonds) + rng.normal(
    0, 12, number_of_bonds
)
analytical_durations = rng.uniform(4.2, 7.0, number_of_bonds)
multipliers = np.clip(
    0.98 - 0.00165 * spreads + rng.normal(0, 0.045, number_of_bonds),
    0.02,
    0.95,
)
empirical_durations = analytical_durations * multipliers

# Step 1: repeat the time-series regression for every bond.
yield_changes = np.linspace(-0.0075, 0.0075, 18)
sample_bonds = [1, 8, 15]
sample_styles = [
    ("#9CC3E2", "Bond A"),
    (blue, "Bond B"),
    (ink, "Bond C"),
]

for bond_index, (color, label) in zip(sample_bonds, sample_styles):
    bond_returns = (
        -empirical_durations[bond_index] * yield_changes
        + rng.normal(0, 0.0015, yield_changes.size)
    )
    axes[0].scatter(
        yield_changes * 100,
        bond_returns * 100,
        s=15,
        facecolor="white",
        edgecolor=color,
        linewidth=0.7,
        alpha=0.8,
    )
    axes[0].plot(
        yield_changes * 100,
        -empirical_durations[bond_index] * yield_changes * 100,
        color=color,
        linewidth=2,
        label=label + rf": $D_{{emp}}={empirical_durations[bond_index]:.1f}$",
    )

axes[0].axhline(0, color=grey, linewidth=0.7)
axes[0].axvline(0, color=grey, linewidth=0.7)
axes[0].set_title("1  Estimate each bond separately", loc="left", fontweight="bold")
axes[0].set_xlabel("Treasury yield change (%)")
axes[0].set_ylabel("Bond return (%)")
axes[0].legend(frameon=False, fontsize=17, loc="lower left")
axes[0].text(
    0.04,
    0.96,
    "Repeat the time-series regression\n" + r"for every bond $i$",
    va="top",
    transform=axes[0].transAxes,
    color=ink,
    fontsize=17,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=grid),
)

# Step 2: calculate one multiplier for every bond.
spread_order = np.argsort(spreads)
bond_positions = np.arange(1, number_of_bonds + 1)
ordered_multipliers = multipliers[spread_order]
axes[1].vlines(
    bond_positions,
    0,
    ordered_multipliers,
    color="#B8D4EA",
    linewidth=2,
)
axes[1].scatter(
    bond_positions,
    ordered_multipliers,
    s=32,
    facecolor=blue,
    edgecolor=ink,
    linewidth=0.6,
)
axes[1].set_ylim(0, 1.05)
axes[1].set_xlim(0.2, number_of_bonds + 0.8)
axes[1].set_xticks([1, 6, 12, 18])
axes[1].set_xlabel("Bonds, ordered by spread")
axes[1].set_ylabel(r"Bond-level multiplier $M_i$")
axes[1].set_title("2  Compute one multiplier per bond", loc="left", fontweight="bold")
axes[1].text(
    0.5,
    0.91,
    r"$M_i=D_{emp,i}/D_{analytical,i}$",
    ha="center",
    transform=axes[1].transAxes,
    fontsize=17,
    color=ink,
    bbox=dict(boxstyle="round,pad=0.35", facecolor="#FFF7E5", edgecolor=gold),
)
axes[1].annotate(
    "18 separate ratios",
    xy=(14, ordered_multipliers[13]),
    xytext=(10, 0.28),
    arrowprops=dict(arrowstyle="->", color=grey),
    fontsize=17,
    color=ink,
)

# Step 3: regress all bond-level multipliers on spread.
axes[2].scatter(
    spreads,
    multipliers,
    s=38,
    facecolor="#FFF7E5",
    edgecolor=gold,
    linewidth=1,
)
spread_slope, spread_intercept = np.polyfit(spreads, multipliers, 1)
spread_range = np.array([35, 585])
axes[2].plot(
    spread_range,
    spread_intercept + spread_slope * spread_range,
    color=gold,
    linewidth=2.4,
    label=r"$M_i=a+bs_i+u_i$",
)
axes[2].axhline(0, color=grey, linewidth=0.8, linestyle="--")
axes[2].set_ylim(-0.08, 1.05)
axes[2].set_xlabel(r"Credit spread $s_i$ (bps)")
axes[2].set_ylabel(r"Bond-level multiplier $M_i$")
axes[2].set_title("3  Regress all multipliers on spread", loc="left", fontweight="bold")
axes[2].legend(frameon=False, fontsize=17, loc="upper right")
axes[2].text(
    0.05,
    0.08,
    "Each point is one bond",
    transform=axes[2].transAxes,
    color=ink,
    fontsize=17,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=grid),
)

for ax in axes:
    ax.grid(axis="y", color=grid, linewidth=0.7, alpha=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=16)



plt.tight_layout(w_pad=2.0)
fig.canvas.draw()
for k, ax in enumerate(axes):
    box=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted()).expanded(1.03,1.04)
    fig.savefig(OUT/f"lec10-fig-estimating-duration-multiplier-{k+1}.svg",bbox_inches=box)
plt.close(fig)


#| label: fig-duration-multipliers
#| fig-cap: "Duration multipliers typically decline as credit quality weakens"
import matplotlib.pyplot as plt

ratings = ["Aaa/Aa", "A", "Baa", "Ba", "B", "Caa"]
multipliers = [0.88, 0.85, 0.80, 0.22, -0.03, -0.15]
colors = ["#4C78A8" if m >= 0 else "#E45756" for m in multipliers]

fig, ax = plt.subplots(figsize=(13,5.4))
ax.bar(ratings, multipliers, color=colors, edgecolor="black")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylabel("Duration multiplier")
ax.set_title("Illustrative empirical Treasury hedge ratios by rating")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
save(plt.gcf(),"lec10-fig-duration-multipliers")


#| label: fig-bsm-asset-paths
#| fig-cap: "In the basic BSM model, default occurs at maturity if asset value ends below the debt threshold"
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(4110)
n_paths = 12
n_steps = 120
T = 1.0
dt = T / n_steps
A0 = 110
K = 100
mu = 0.04
sigma = 0.28

time = np.linspace(0, T, n_steps + 1)
paths = np.empty((n_paths, n_steps + 1))
paths[:, 0] = A0

for t in range(1, n_steps + 1):
    shocks = rng.normal(size=n_paths)
    paths[:, t] = paths[:, t - 1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks)

defaulted = paths[:, -1] < K

fig, ax = plt.subplots(figsize=(13,5.4))
for path, is_default in zip(paths, defaulted):
    color = "#E45756" if is_default else "#4C78A8"
    alpha = 0.9 if is_default else 0.55
    ax.plot(time, path, color=color, alpha=alpha, linewidth=1.5)

ax.axhline(K, color="black", linestyle="--", linewidth=1.2, label="Debt threshold K")
ax.scatter(np.repeat(T, defaulted.sum()), paths[defaulted, -1], color="#E45756", edgecolor="black", zorder=4, label="Default at T")
ax.set_xlabel("Time")
ax.set_ylabel("Firm asset value")
ax.set_title("Default depends on where asset value ends relative to debt")
ax.grid(alpha=0.3)
ax.legend(loc="upper left")
plt.tight_layout()
save(plt.gcf(),"lec10-fig-bsm-asset-paths")


#| label: fig-bsm-payoffs
#| fig-cap: "In the BSM model, equity is a call option and risky debt is capped at face value"
import numpy as np
import matplotlib.pyplot as plt

A = np.linspace(0, 180, 300)
K = 100
equity = np.maximum(A - K, 0)
debt = np.minimum(A, K)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(A, equity, label="Equity payoff", linewidth=2.0, color="#4C78A8")
ax.plot(A, debt, label="Debt payoff", linewidth=2.0, color="#F58518")
ax.axvline(K, color="black", linestyle="--", linewidth=1.0)
ax.text(K + 5, 80, "Debt face value K", fontsize=17)
ax.set_xlabel("Firm asset value at maturity")
ax.set_ylabel("Payoff")
ax.set_title("Black-Scholes-Merton payoff intuition")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
save(plt.gcf(),"lec10-fig-bsm-payoffs")


#| label: fig-poisson-distributions
#| fig-cap: "Poisson event-count distributions at different intensity rates; each dashed line marks the mean"
from math import exp, factorial
import numpy as np
import matplotlib.pyplot as plt

intensities = [0.5, 2, 5, 10]
k = np.arange(0, 22)
colors = ["#B8D4EA", "#6FA8D6", "#2F78B7", "#174A75"]

fig, axes = plt.subplots(2, 2, figsize=(13,7.5), sharex=True, sharey=True)
for ax, lam, color in zip(axes.flat, intensities, colors):
    pmf = np.array([exp(-lam) * lam**count / factorial(count) for count in k])
    ax.bar(k, pmf, width=0.82, color=color, edgecolor="#17324D", linewidth=0.5)
    ax.axvline(lam, color="#333333", linestyle="--", linewidth=1.3)
    ax.set_title(rf"$\lambda={lam:g}$: mean = variance = {lam:g}")
    ax.grid(axis="y", alpha=0.25)

for ax in axes[-1, :]:
    ax.set_xlabel(r"Event count $N_1$")
for ax in axes[:, 0]:
    ax.set_ylabel("Probability")

fig.suptitle("Higher intensity shifts and reshapes the Poisson distribution", fontsize=17)
plt.tight_layout()
save(plt.gcf(),"lec10-fig-poisson-distributions")


#| label: fig-poisson-process-simulations
#| fig-cap: "Simulated Poisson-process paths at different intensity rates; higher intensity produces faster average count growth"
rng = np.random.default_rng(411)
time_horizon = 10
steps_per_unit = 100
dt = 1 / steps_per_unit
time = np.linspace(0, time_horizon, time_horizon * steps_per_unit + 1)
line_styles = [":", "--", "-.", "-"]

fig, ax = plt.subplots(figsize=(13,5.4))
for lam, color, line_style in zip(intensities, colors, line_styles):
    increments = rng.poisson(lam * dt, size=time.size - 1)
    counts = np.concatenate(([0], np.cumsum(increments)))
    ax.step(
        time,
        counts,
        where="post",
        color=color,
        linestyle=line_style,
        linewidth=2.0,
        label=rf"$\lambda={lam:g}$",
    )

ax.set_xlabel("Time")
ax.set_ylabel(r"Cumulative event count $N_t$")
ax.set_title("One simulated Poisson-process path per intensity rate")
ax.grid(alpha=0.25)
ax.legend(title="Intensity per unit time", ncol=2)
plt.tight_layout()
save(plt.gcf(),"lec10-fig-poisson-process-simulations")


#| label: fig-poisson-survival
#| fig-cap: "Higher default intensity lowers survival probability more quickly"
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 200)
intensities = [0.01, 0.02, 0.05]

fig, ax = plt.subplots(figsize=(13,5.4))
for lam in intensities:
    ax.plot(t, np.exp(-lam * t), linewidth=2.0, label=f"lambda = {lam:.0%}")

ax.set_xlabel("Years")
ax.set_ylabel("Survival probability")
ax.set_title("Poisson default intensity and survival")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
save(plt.gcf(),"lec10-fig-poisson-survival")


#| label: fig-spread-pd-ratio
#| fig-cap: "A wider spread is not always better after adjusting for modeled default risk"
import numpy as np
import matplotlib.pyplot as plt

bonds = ["Bond A", "Bond B", "Bond C", "Bond D"]
spreads = np.array([120, 180, 90, 250])
pd = np.array([0.020, 0.060, 0.015, 0.100])
ratio = spreads / (pd * 100)

fig, ax = plt.subplots(figsize=(13,5.4))
bars = ax.bar(bonds, ratio, color="#54A24B", edgecolor="black")
ax.set_ylabel("Spread (bp) / PD (percentage points)")
ax.set_title("Relative value screen")
ax.grid(axis="y", alpha=0.3)

for bar, value in zip(bars, ratio):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 1, f"{value:.0f}", ha="center", fontsize=17)

ax.set_ylim(0,70)
plt.tight_layout()
save(plt.gcf(),"lec10-fig-spread-pd-ratio")


# Illustrative dependence comparison with identical marginal PD = 2%.
from scipy.stats import binom
k=np.arange(0,41)
ind=binom.pmf(k,100,.02)
cluster=.1*binom.pmf(k,100,.20);cluster[0]+=.9
fig,ax=axis();ax.plot(k,ind,label="Independent: each PD = 2%",color=GREEN);ax.plot(k,cluster,label="Common state: 90% calm / 10% stress",color=GOLD)
ax.set(xlabel="Number of defaults in 100 bonds",ylabel="Probability",title="Same expected defaults; different tail risk",ylim=(0,1))
ax.annotate("90% probability at zero",xy=(0,.9),xytext=(8,.67),arrowprops=dict(arrowstyle="->"))
ax.legend(loc="upper right");save(fig,"lec10-default-dependence")