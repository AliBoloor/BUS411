"""Lecture 8 source figures, reproduced with slide-scale labels."""

from build_figures import *

CURRENT_FIG="lec8-fig-spread-components"

#| label: fig-spread-components
#| fig-cap: "A quoted yield spread bundles together several sources of compensation"
#| echo: false
import matplotlib.pyplot as plt

components = ["Credit", "Liquidity", "Embedded\noption"]
values = [75, 25, 50]
colors = ["#4C78A8", "#72B7B2", "#F58518"]

fig, ax = plt.subplots(figsize=(13,5.4))
left = 0
for component, value, color in zip(components, values, colors):
    ax.barh(["Quoted\nspread"], [value], left=left, color=color, edgecolor="black", height=0.45)
    ax.text(left + value / 2, 0, f"{component}\n{value} bps", ha="center", va="center", fontsize=17)
    left += value

ax.set_xlim(0, sum(values) + 20)
ax.set_xlabel("Basis points")
ax.set_title("Why a raw yield spread is hard to interpret")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", length=0)
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-static-spread-curve"

#| label: fig-static-spread-curve
#| fig-cap: "Static spread adds the same margin to each point on the spot curve"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

maturities = np.array([0.5, 1, 2, 3, 5, 7, 10])
spot_curve = np.array([0.025, 0.027, 0.030, 0.033, 0.037, 0.039, 0.041])
static_spread = 0.008

plt.figure(figsize=(13,5.4))
plt.plot(maturities, spot_curve * 100, "o-", label="Treasury spot curve")
plt.plot(maturities, (spot_curve + static_spread) * 100, "s--", label="Spot curve + static spread")
for x, y in zip(maturities, spot_curve):
    plt.plot([x, x], [y * 100, (y + static_spread) * 100], color="gray", alpha=0.45, linewidth=1)

plt.xlabel("Maturity (years)")
plt.ylabel("Discount rate (%)")
plt.title("Static spread as a constant vertical shift")
plt.grid(True, alpha=0.3)
plt.legend()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-static-spread"

#| label: fig-static-spread
#| fig-cap: "Static spread is the spread where model present value equals the observed price"
import numpy as np
import matplotlib.pyplot as plt

coupons = np.array([30] * 10, dtype=float)
coupons[-1] += 1000
times = np.arange(0.5, 5.1, 0.5)

spot = np.array([0.02, 0.022, 0.026, 0.03, 0.034, 0.038, 0.04, 0.041, 0.042, 0.043])
price = 1020

def price_with_spread(s):
    disc = (1 + spot + s) ** (-times)
    return np.sum(coupons * disc)

spreads = np.linspace(-0.01, 0.06, 500)
vals = np.array([price_with_spread(s) for s in spreads])

order = np.argsort(vals)
s_est = np.interp(price, vals[order], spreads[order])
pv_at_s = price_with_spread(s_est)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(spreads * 10000, vals, color="#1f77b4", linewidth=2.2, label="Model PV using spot curve + trial spread")

ds = 0.0001
slope_at_solution = (price_with_spread(s_est + ds) - price_with_spread(s_est - ds)) / (2 * ds)
tangent = pv_at_s + slope_at_solution * (spreads - s_est)
ax.plot(
    spreads * 10000,
    tangent,
    color="#7A7A7A",
    linestyle=":",
    linewidth=1.6,
    label="Local linear approximation",
)

ax.axhline(price, color="black", linestyle="--", linewidth=1.4, label="Observed market price")
ax.axvline(s_est * 10000, color="dimgray", linestyle="--", linewidth=1.4, label=f"Static spread = {s_est*10000:.1f} bps")
ax.scatter([s_est * 10000], [pv_at_s], s=55, color="black", zorder=3)

ax.text(180, 1090, "Higher spread means heavier discounting\nand a lower present value.", fontsize=17)
ax.text(355, price - 90, "The curve is smooth, not linear;\nit only looks linear over short ranges.", fontsize=17)
plt.xlabel("Spread (basis points)")
plt.ylabel("Present value ($)")
plt.title("Finding the static spread from a nonlinear present-value curve")
plt.legend(fontsize=17)
plt.grid(True, alpha=0.3)
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-callable-bond-economic-states"

#| label: fig-callable-bond-economic-states
#| fig-cap: "Callable bond economics: falling rates help the issuer and limit investor upside"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

rates = np.array([2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
straight_value = np.array([125, 118, 110, 102, 95, 89])
call_price = 100
callable_value = np.minimum(straight_value, call_price)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(rates, straight_value, "o-", label="Option-free value")
ax.plot(rates, callable_value, "s--", label="Callable value to investor")
ax.axhline(call_price, color="gray", linestyle=":", linewidth=1.4, label="Call price")
ax.fill_between(rates, callable_value, straight_value, where=straight_value > callable_value, color="#F58518", alpha=0.25, label="Value transferred to issuer")

ax.annotate(
    "Rates fall:\nissuer likely calls",
    xy=(2.5, 100),
    xytext=(2.2, 88),
    arrowprops=dict(arrowstyle="->", linewidth=1),
    fontsize=17,
)
ax.annotate(
    "Rates rise:\ncall is unlikely",
    xy=(6.2, 92),
    xytext=(4.0, 118),
    arrowprops=dict(arrowstyle="->", linewidth=1),
    fontsize=17,
)

ax.set_xlabel("Market yield (%)")
ax.set_ylabel("Bond value")
ax.set_title("The call feature caps the investor's upside")
ax.grid(True, alpha=0.3)
ax.legend(fontsize=17)
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-callable-price-yield"

#| label: fig-callable-price-yield
#| fig-cap: "Price-yield relationship for an option-free bond and a callable bond"
import numpy as np
import matplotlib.pyplot as plt

def straight_bond_price(y, n, coupon, face=100):
    t = np.arange(1, n + 1)
    cfs = np.full(n, coupon, dtype=float)
    cfs[-1] += face
    yv = np.atleast_1d(y)
    disc = (1 + yv[:, None]) ** (-t)
    return np.sum(cfs * disc, axis=1)

def callable_bond_price_simple(y, n, coupon, face=100, call_price=100, call_after=3):
    yv = np.atleast_1d(y)
    prices = []
    cfs = np.full(n, coupon, dtype=float)
    cfs[-1] += face
    for yi in yv:
        pv_early = np.sum(cfs[:call_after] / (1 + yi) ** np.arange(1, call_after + 1))
        remaining = cfs[call_after:]
        pv_remaining_at_call = np.sum(remaining / (1 + yi) ** np.arange(1, len(remaining) + 1))
        continuation_at_call = min(call_price, pv_remaining_at_call)
        prices.append(pv_early + continuation_at_call / (1 + yi) ** call_after)
    return np.array(prices)

ys = np.linspace(0.02, 0.12, 200)
price_straight = straight_bond_price(ys, 10, 8)
price_call = callable_bond_price_simple(ys, 10, 8, call_price=100, call_after=3)

plt.figure(figsize=(13,5.4))
plt.plot(ys * 100, price_straight, label="Option-free bond")
plt.plot(ys * 100, price_call, linestyle="--", label="Callable bond")
plt.xlabel("Yield (%)")
plt.ylabel("Price ($)")
plt.title("Price-yield relationship")
plt.legend()
plt.grid(True)
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-embedded-option-decomposition"

#| label: fig-embedded-option-decomposition
#| fig-cap: "For a callable bond, the embedded call option is the gap between straight-bond value and callable-bond value"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

yields = np.linspace(0.025, 0.12, 250)
coupon = 0.08
face = 100
n = 10
t = np.arange(1, n + 1)
cash_flows = np.full(n, coupon * face)
cash_flows[-1] += face

straight = np.sum(cash_flows / (1 + yields[:, None]) ** t, axis=1)
callable_price = straight - 16 / (1 + np.exp((yields - 0.055) / 0.007))

target_yield = 0.045
idx = np.argmin(np.abs(yields - target_yield))

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(yields * 100, straight, color="#1f77b4", linewidth=2.2, label="Option-free bond")
ax.plot(yields * 100, callable_price, color="#2ca02c", linewidth=2.2, label="Callable bond")
ax.vlines(
    yields[idx] * 100,
    callable_price[idx],
    straight[idx],
    color="black",
    linewidth=1.5,
    linestyles="--",
)
ax.annotate(
    "Embedded call option value",
    xy=(yields[idx] * 100, (straight[idx] + callable_price[idx]) / 2),
    xytext=(6.4, 118),
    arrowprops=dict(arrowstyle="->", linewidth=1),
    fontsize=17,
)
ax.text(8.5, 104, r"$V_{\mathrm{callable}}=V_{\mathrm{straight}}-V_{\mathrm{call}}$", fontsize=17)
ax.set_xlabel("Yield (%)")
ax.set_ylabel("Bond value")
ax.set_title("Decomposing a callable bond")
ax.grid(True, alpha=0.3)
ax.legend(fontsize=17)
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-backward-induction-intuition"

#| label: fig-backward-induction-intuition
#| fig-cap: "Backward induction: start with future payoffs, then work back to today"
#| echo: false
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(13,5.4))

nodes = {
    (0, 0): ("Today\nprice", 0, 0),
    (1, 1): ("Future\nstate", 1.5, 1),
    (1, -1): ("Future\nstate", 1.5, -1),
    (2, 2): ("Final\npayoff", 3.0, 2),
    (2, 0): ("Final\npayoff", 3.0, 0),
    (2, -2): ("Final\npayoff", 3.0, -2),
}

edges = [
    ((0, 0), (1, 1)),
    ((0, 0), (1, -1)),
    ((1, 1), (2, 2)),
    ((1, 1), (2, 0)),
    ((1, -1), (2, 0)),
    ((1, -1), (2, -2)),
]

for start, end in edges:
    _, x0, y0 = nodes[start]
    _, x1, y1 = nodes[end]
    ax.plot([x0, x1], [y0, y1], color="gray", linewidth=1.1)

for label, x, y in nodes.values():
    ax.scatter(x, y, s=4200, color="#E8F1FA", edgecolor="black", zorder=3)
    ax.text(x, y, label, ha="center", va="center", fontsize=17, zorder=4, bbox=dict(boxstyle="round,pad=.35",facecolor="#E8F1FA",edgecolor="black"))


ax.set_xlim(-0.6, 3.8)
ax.set_ylim(-3.2, 3.2)
ax.set_xticks([0, 1.5, 3.0])
ax.set_xticklabels(["Time 0", "Intermediate date", "Final date"])
ax.set_yticks([])
ax.spines[["left", "right", "top"]].set_visible(False)
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)


CURRENT_FIG="lec8-fig-simple-rate-lattice"

#| label: fig-simple-rate-lattice
#| fig-cap: "Short-rate lattice used in the worked example"
#| echo: false
import matplotlib.pyplot as plt

def draw_lattice(
    nodes,
    edges,
    title,
    node_color="#E8F1FA",
    highlight_edges=None,
    xticks=None,
    xticklabels=None,
    xlim=None,
    node_size=1250,
    font_size=8.5,
):
    fig, ax = plt.subplots(figsize=(13,5.4))
    highlight_edges = set(highlight_edges or [])

    for start, end in edges:
        x0, y0, _ = nodes[start]
        x1, y1, _ = nodes[end]
        color = "black" if (start, end) in highlight_edges else "#8A8A8A"
        linewidth = 2.0 if (start, end) in highlight_edges else 1.1
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=linewidth, zorder=1)

    for key, (x, y, label) in nodes.items():
        pass
        ax.text(x, y, label, ha="center", va="center", fontsize=17, zorder=4, bbox=dict(boxstyle="round,pad=.35",facecolor="#E8F1FA",edgecolor="black"))

    ax.set_title(title)
    ax.set_xticks(xticks or [0, 1, 2, 3])
    ax.set_xticklabels(xticklabels or ["Year 0", "Year 1", "Year 2", "Year 3"])
    ax.set_yticks([])
    ax.spines[["left", "right", "top"]].set_visible(False)
    ax.set_xlim(xlim or (-0.35, 3.35))
    ax.set_ylim(-3.6, 3.6)
    plt.tight_layout()
    save(plt.gcf(),CURRENT_FIG)

rate_nodes = {
    "0": (0, 0, "6%"),
    "1L": (1, 1, "5%"),
    "1H": (1, -1, "9%"),
    "2L": (2, 2, "4%"),
    "2M": (2, 0, "8%"),
    "2H": (2, -2, "12%"),
    "3L": (3, 3, "3%"),
    "3ML": (3, 1, "7%"),
    "3MH": (3, -1, "11%"),
    "3H": (3, -3, "15%"),
}

lattice_edges = [
    ("0", "1L"), ("0", "1H"),
    ("1L", "2L"), ("1L", "2M"),
    ("1H", "2M"), ("1H", "2H"),
    ("2L", "3L"), ("2L", "3ML"),
    ("2M", "3ML"), ("2M", "3MH"),
    ("2H", "3MH"), ("2H", "3H"),
]

draw_lattice(rate_nodes, lattice_edges, "Each node is a possible one-year short rate")


CURRENT_FIG="lec8-fig-terminal-payoff-lattice"

#| label: fig-terminal-payoff-lattice
#| fig-cap: "Step 1: terminal payoff is coupon plus principal at every maturity node"
#| echo: false
terminal_nodes = {
    "0": (0, 0, "6%"),
    "1L": (1, 1, "5%"),
    "1H": (1, -1, "9%"),
    "2L": (2, 2, "4%"),
    "2M": (2, 0, "8%"),
    "2H": (2, -2, "12%"),
    "3L": (3, 3, "108"),
    "3ML": (3, 1, "108"),
    "3MH": (3, -1, "108"),
    "3H": (3, -3, "108"),
}

draw_lattice(terminal_nodes, lattice_edges, "Start at maturity: value = 100 + 8 = 108")


CURRENT_FIG="lec8-fig-year2-sublattice"

#| label: fig-year2-sublattice
#| fig-cap: "Step 2: each year-2 value is computed from the two adjacent terminal nodes"
#| echo: false
year2_nodes = {
    "2L": (0, 2, "Year 2\nr=4%\nV=111.85"),
    "2M": (0, 0, "Year 2\nr=8%\nV=108.00"),
    "2H": (0, -2, "Year 2\nr=12%\nV=104.43"),
    "3L": (1.4, 3, "108"),
    "3ML": (1.4, 1, "108"),
    "3MH": (1.4, -1, "108"),
    "3H": (1.4, -3, "108"),
}
year2_edges = [
    ("2L", "3L"), ("2L", "3ML"),
    ("2M", "3ML"), ("2M", "3MH"),
    ("2H", "3MH"), ("2H", "3H"),
]

draw_lattice(
    year2_nodes,
    year2_edges,
    "Move from year 3 payoffs back to year 2 values",
    xticks=[0, 1.4],
    xticklabels=["Year 2", "Year 3"],
    xlim=(-0.45, 1.85),
    node_size=1700,
    font_size=8.0,
)


CURRENT_FIG="lec8-fig-call-rule-sublattice"

#| label: fig-call-rule-sublattice
#| fig-cap: "Step 3: the call rule caps year-2 values above the call price"
#| echo: false
call_rule_nodes = {
    "2L": (0, 2, "H=111.85\nC=107.00"),
    "2M": (0, 0, "H=108.00\nC=107.00"),
    "2H": (0, -2, "H=104.43\nNo call\nV=104.43"),
}

draw_lattice(
    call_rule_nodes,
    [],
    "Callable value at year 2 is min(hold value, 107)",
    xticks=[0],
    xticklabels=["Year 2"],
    xlim=(-0.75, 0.75),
    node_size=2100,
    font_size=7.8,
)


CURRENT_FIG="lec8-fig-year1-straight-sublattice"

#| label: fig-year1-straight-sublattice
#| fig-cap: "Step 4: option-free year-1 values are rolled back from option-free year-2 values"
#| echo: false
year1_straight_nodes = {
    "1L": (0, 1, "Year 1\nr=5%\nV=112.69"),
    "1H": (0, -1, "Year 1\nr=9%\nV=105.44"),
    "2L": (1.4, 2, "111.85"),
    "2M": (1.4, 0, "108.00"),
    "2H": (1.4, -2, "104.43"),
}
year1_edges = [
    ("1L", "2L"), ("1L", "2M"),
    ("1H", "2M"), ("1H", "2H"),
]

draw_lattice(
    year1_straight_nodes,
    year1_edges,
    "Option-free rollback from year 2 to year 1",
    xticks=[0, 1.4],
    xticklabels=["Year 1", "Year 2"],
    xlim=(-0.45, 1.85),
    node_size=1900,
    font_size=7.8,
)


CURRENT_FIG="lec8-fig-year1-callable-sublattice"

#| label: fig-year1-callable-sublattice
#| fig-cap: "Step 5: callable year-1 values use the call-adjusted year-2 values"
#| echo: false
year1_callable_nodes = {
    "1L": (0, 1, "Year 1\nr=5%\nV=109.90"),
    "1H": (0, -1, "Year 1\nr=9%\nV=104.99"),
    "2L": (1.4, 2, "107.00"),
    "2M": (1.4, 0, "107.00"),
    "2H": (1.4, -2, "104.43"),
}

draw_lattice(
    year1_callable_nodes,
    year1_edges,
    "Callable rollback from year 2 to year 1",
    xticks=[0, 1.4],
    xticklabels=["Year 1", "Year 2"],
    xlim=(-0.45, 1.85),
    node_size=1900,
    font_size=7.8,
)


CURRENT_FIG="lec8-fig-time0-sublattice"

#| label: fig-time0-sublattice
#| fig-cap: "Step 6: final rollback gives today's option-free and callable values"
#| echo: false
time0_nodes = {
    "0": (0, 0, "Today\nr=6%\nS=110.89\nC=109.36"),
    "1L": (1.55, 1, "Year 1\nS=112.69\nC=109.90"),
    "1H": (1.55, -1, "Year 1\nS=105.44\nC=104.99"),
}
time0_edges = [("0", "1L"), ("0", "1H")]

draw_lattice(
    time0_nodes,
    time0_edges,
    "Roll year-1 values back to time 0",
    xticks=[0, 1.55],
    xticklabels=["Year 0", "Year 1"],
    xlim=(-0.55, 2.15),
    node_size=2900,
    font_size=7.3,
)


CURRENT_FIG="lec8-fig-putable-worked-example"

#| label: fig-putable-worked-example
#| fig-cap: "Worked Example 2: pricing a putable bond by backward induction"
#| echo: false
putable_nodes = {
    "0": (0, 0, "Today\nr=6%\nV=102.15"),
    "1L": (1.45, 1.35, "Year 1\nr=4%\nHold=105.96\nV=105.96"),
    "1H": (1.45, -1.35, "Year 1\nr=12%\nHold=98.75\nPut=100.00\nV=100.00"),
    "2L": (2.9, 2.5, "105"),
    "2M": (2.9, 0, "105"),
    "2H": (2.9, -2.5, "105"),
}
putable_edges = [
    ("0", "1L"), ("0", "1H"),
    ("1L", "2L"), ("1L", "2M"),
    ("1H", "2M"), ("1H", "2H"),
]

draw_lattice(
    putable_nodes,
    putable_edges,
    "Putable bond: max(hold value, put price) at year 1",
    xticks=[0, 1.45, 2.9],
    xticklabels=["Year 0", "Year 1", "Year 2"],
    xlim=(-0.45, 3.35),
    node_size=2600,
    font_size=7.2,
)


CURRENT_FIG="lec8-fig-effective-duration-intuition"

#| label: fig-effective-duration-intuition
#| fig-cap: "Effective duration and convexity reprice the bond after rate shocks"
#| echo: false
import numpy as np
import matplotlib.pyplot as plt

rate_shocks = np.array([-0.50, 0.00, 0.50])
option_free_prices = np.array([108, 103, 98])
callable_prices = np.array([103.5, 102, 98.5])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(rate_shocks, option_free_prices, "o-", label="Option-free bond")
ax.plot(rate_shocks, callable_prices, "s--", label="Callable bond")
ax.axvline(0, color="gray", linestyle=":", linewidth=1)
ax.set_xlabel("Parallel rate shock (percentage points)")
ax.set_ylabel("Repriced value")
ax.set_title("Callable bonds respond asymmetrically to rate changes")
ax.annotate(
    "Rate decline:\nupside is capped",
    xy=(-0.5, 103.5),
    xytext=(-0.35, 100.0),
    arrowprops=dict(arrowstyle="->", linewidth=1),
    fontsize=17,
)
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
save(plt.gcf(),CURRENT_FIG)
