"""Lecture 7 simulation inputs and plots reproduced from the lecture notes."""

from build_figures import *

#| label: fig-drift-and-random-shocks
#| fig-cap: "Drift gives the expected path; at each future time, the short rate is normally distributed around that path"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(7)

r0 = 0.04
b = 0.004
sigma = 0.015
T = 5
dt = 1 / 252
steps = int(T / dt) + 1
times = np.linspace(0, T, steps)

drift_path = r0 + b * times

n_paths = 8
paths = np.empty((n_paths, steps))
paths[:, 0] = r0

for i in range(n_paths):
    shocks = sigma * np.sqrt(dt) * np.random.randn(steps - 1)
    increments = b * dt + shocks
    paths[i, 1:] = r0 + np.cumsum(increments)

plt.figure(figsize=(13,5.4))
for i in range(n_paths):
    plt.plot(times, paths[i] * 100, color="#9BBFE0", linewidth=1.1, alpha=0.9)

plt.plot(times, drift_path * 100, color="black", linewidth=2.4, label="Expected drift path: $r_0 + bt$")

# At any fixed future time, r_t is normally distributed:
# r_t ~ N(r_0 + bt, sigma^2 t).  The bell curve below is a visual schematic.
t_star = 3.0
mean_star = r0 + b * t_star
std_star = sigma * np.sqrt(t_star)
y_grid = np.linspace(mean_star - 2.6 * std_star, mean_star + 2.6 * std_star, 200)
pdf = np.exp(-0.5 * ((y_grid - mean_star) / std_star) ** 2)
pdf = pdf / pdf.max() * 0.45

plt.axvline(t_star, color="gray", linestyle="--", linewidth=1.1)
plt.plot(t_star + pdf, y_grid * 100, color="#D55E00", linewidth=2.0, label=r"$r_t \sim N(r_0+bt,\sigma^2t)$")
plt.scatter([t_star], [mean_star * 100], color="#D55E00", s=35, zorder=4)
plt.annotate(
    "At a fixed time $t$,\npossible $r_t$ values\nare normally distributed",
    xy=(t_star + 0.35, mean_star * 100),
    xytext=(3.65, 6.9),
    arrowprops=dict(arrowstyle="->", linewidth=1.0),
    fontsize=17,
)

plt.axhline(r0 * 100, color="gray", linestyle=":", linewidth=1)
plt.xlabel("Time (years)")
plt.ylabel("Short rate (%)")
plt.title(r"Short-rate paths under $dr_t = b\,dt + \sigma\,dz_t$")
plt.grid(True, alpha=0.3)
plt.legend()
save(plt.gcf(),"lec7-fig-drift-and-random-shocks")


#| label: fig-mean-reversion-speed
#| fig-cap: "Low versus high speed of mean reversion"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12)

r0 = 0.075
bar_r = 0.04
sigma = 0.012
T = 6
dt = 1 / 252
steps = int(T / dt) + 1
times = np.linspace(0, T, steps)
n_paths = 6

low_alpha = 0.15
high_alpha = 1.25

shock_matrix = np.random.randn(n_paths, steps - 1)

def simulate_mean_reversion(alpha):
    paths = np.empty((n_paths, steps))
    paths[:, 0] = r0
    for i in range(n_paths):
        for j in range(1, steps):
            r_prev = paths[i, j - 1]
            dr = -alpha * (r_prev - bar_r) * dt + sigma * np.sqrt(dt) * shock_matrix[i, j - 1]
            paths[i, j] = r_prev + dr
    return paths

low_paths = simulate_mean_reversion(low_alpha)
high_paths = simulate_mean_reversion(high_alpha)

fig, axes = plt.subplots(1, 2, figsize=(13,5.4), sharey=True)

for ax, paths, alpha, title in [
    (axes[0], low_paths, low_alpha, "Low mean reversion"),
    (axes[1], high_paths, high_alpha, "High mean reversion"),
]:
    for i in range(n_paths):
        ax.plot(times, paths[i] * 100, color="#9BBFE0", linewidth=1.1, alpha=0.9)
    ax.axhline(bar_r * 100, color="black", linestyle="--", linewidth=1.5, label="Long-run mean")
    ax.set_title(f"{title}\n$\\alpha={alpha}$")
    ax.set_xlabel("Time (years)")
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("Short rate (%)")
axes[1].legend(loc="upper right", fontsize=17)
fig.suptitle("Higher $\\alpha$ pulls rates back toward the long-run mean faster", y=1.03)
plt.tight_layout()
save(plt.gcf(),"lec7-fig-mean-reversion-speed")


#| label: fig-ou-simulation
#| fig-cap: "Simulated short‑rate paths following an Ornstein–Uhlenbeck process"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

alpha = 0.5    # speed of mean reversion
bar_r = 0.05   # long-run mean (5%)
sigma0 = 0.02  # volatility (2%)
r0 = 0.04      # starting short rate (4%)

T = 5          # 5 years
dt = 1/252     # daily time step
steps = int(T/dt)
paths = 5      # number of simulated paths

times = np.linspace(0, T, steps)
results = np.zeros((paths, steps))
for i in range(paths):
    r = r0
    for j in range(steps):
        dr = -alpha*(r - bar_r)*dt + sigma0*np.sqrt(dt)*np.random.randn()
        r += dr
        results[i,j] = r

plt.figure(figsize=(13,5.4))
for i in range(paths):
    plt.plot(times, results[i])
plt.xlabel("Time (years)")
plt.ylabel("Short rate")
plt.title("Ornstein–Uhlenbeck (Vasicek) process simulations")
plt.grid(True)
save(plt.gcf(),"lec7-fig-ou-simulation")


#| label: fig-short-rate-tree
#| fig-cap: "A simple short‑rate tree: each future node implies a future yield curve"
#| echo: false
import matplotlib.pyplot as plt

nodes = {
    (0, 0): ("$r_0$\n$P(0,T)$", 0, 0),
    (1, 1): ("$r_u$\n$P(t,T)$", 1, 1),
    (1, -1): ("$r_d$\n$P(t,T)$", 1, -1),
    (2, 2): ("$r_{uu}$\n$P(t,T)$", 2, 2),
    (2, 0): ("$r_{ud}$\n$P(t,T)$", 2, 0),
    (2, -2): ("$r_{dd}$\n$P(t,T)$", 2, -2),
}

edges = [
    ((0, 0), (1, 1)),
    ((0, 0), (1, -1)),
    ((1, 1), (2, 2)),
    ((1, 1), (2, 0)),
    ((1, -1), (2, 0)),
    ((1, -1), (2, -2)),
]

fig, ax = plt.subplots(figsize=(13,5.4))
for start, end in edges:
    _, x0, y0 = nodes[start]
    _, x1, y1 = nodes[end]
    ax.plot([x0, x1], [y0, y1], color="gray", linewidth=1.2)

for label, x, y in nodes.values():
    ax.scatter(x, y, s=4500, color="#E8F1FA", edgecolor="black", zorder=3)
    ax.text(x, y, label, ha="center", va="center", fontsize=17, zorder=4)

ax.set_xlim(-0.4, 2.4)
ax.set_ylim(-3.1, 3.0)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["Today", "Step 1", "Step 2"])
ax.set_yticks([])
ax.set_title("Short-rate paths in a simple recombining tree")
ax.spines[["left", "right", "top"]].set_visible(False)
save(plt.gcf(),"lec7-fig-short-rate-tree")


#| label: fig-hull-white-fit
#| fig-cap: "Hull–White calibration: theta(t) is chosen so the model fits today's observed curve"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([0.5, 1, 2, 3, 5, 7, 10, 20, 30])
observed_curve = np.array([0.041, 0.040, 0.0385, 0.0375, 0.037, 0.0372, 0.0378, 0.039, 0.040])

# Schematic fitted curve: close to the observed market curve by construction.
model_curve = observed_curve + np.array([0.0000, -0.0001, 0.0001, 0.0000, -0.00005, 0.00005, 0.0000, -0.0001, 0.0001])

plt.figure(figsize=(13,5.4))
plt.plot(maturities, observed_curve * 100, "o-", label="Today's observed yield curve")
plt.plot(maturities, model_curve * 100, "s--", label="Model-fitted yield curve")
plt.xlabel("Maturity (years)")
plt.ylabel("Zero rate (%)")
plt.title("No-arbitrage fit to the initial term structure")
plt.grid(True, alpha=0.35)
plt.legend()
save(plt.gcf(),"lec7-fig-hull-white-fit")


#| label: fig-one-period-option-tree
#| fig-cap: "A one-period binomial tree for an option on a fixed-income underlying asset"
#| echo: false
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13,5.4))
ax.set_axis_off()

nodes = {
    "today": ("Today\nBond: $B_0$\nOption: $C_0$", 0.0, 0.9),
    "up": ("Up state\nBond: $B_u$\nOption: $C_u$", 2.5, 1.55),
    "down": ("Down state\nBond: $B_d$\nOption: $C_d$", 2.5, 0.25),
}

for key, (label, x, y) in nodes.items():
    box = FancyBboxPatch(
        (x, y), 1.45, 0.7,
        boxstyle="round,pad=0.08",
        linewidth=1.1,
        edgecolor="black",
        facecolor="#E8F1FA",
    )
    ax.add_patch(box)
    ax.text(x + 0.725, y + 0.35, label, ha="center", va="center", fontsize=17)

arrows = [
    ((1.45, 1.25), (2.5, 1.9), "$q$"),
    ((1.45, 1.25), (2.5, 0.6), "$1-q$"),
]

for start, end, label in arrows:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.3, color="black"))
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    ax.text(mid_x, mid_y + 0.08, label, ha="center", va="center", fontsize=17)

# ax.text(
#     3.95, 0.9,
#     "$C_0 = \\dfrac{qC_u+(1-q)C_d}{1+r}$",
#     fontsize=17,
#     va="center",
# )

ax.set_xlim(-0.1, 4.2)
ax.set_ylim(0.0, 2.5)
plt.tight_layout(pad=0.2)
save(plt.gcf(),"lec7-fig-one-period-option-tree")
