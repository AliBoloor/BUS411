"""Lecture 9 charts use the lecture notes numerical inputs."""

from build_figures import *

#| label: fig-futures-positions
#| fig-cap: "A clearinghouse stands between the buyer and seller of a futures contract"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(13,5.4))
ax.set_axis_off()

items = [
    ("Long\nfutures", 0.25, 0.85, "#E8F1FA"),
    ("Clearinghouse", 2.75, 0.85, "#F6E8C3"),
    ("Short\nfutures", 5.25, 0.85, "#E6F2E6"),
]

for text, x, y, color in items:
    box = FancyBboxPatch(
        (x, y), 1.25, 0.65,
        boxstyle="round,pad=0.08",
        linewidth=1.1,
        edgecolor="black",
        facecolor=color,
    )
    ax.add_patch(box)
    ax.text(x + 0.625, y + 0.325, text, ha="center", va="center", fontsize=17)

for start, end in [((1.55, 1.18), (2.68, 1.18)), ((4.08, 1.18), (5.18, 1.18))]:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="<->", mutation_scale=14, linewidth=1.4))

ax.text(2.12, 0.55, "guarantees\nperformance", ha="center", fontsize=17)
ax.text(4.65, 0.55, "guarantees\nperformance", ha="center", fontsize=17)
ax.set_xlim(0, 6.8)
ax.set_ylim(0.2, 2.0)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-futures-positions")


#| label: fig-margin-account
#| fig-cap: "Daily mark-to-market cash flows for a long futures position"
import numpy as np
import matplotlib.pyplot as plt

days = np.array([0, 1, 2, 3])
settle_32nds = np.array([100 * 32, 100 * 32 + 12, 99 * 32 + 28, 100 * 32 + 8])
settle_decimal = settle_32nds / 32
daily_cash_flow = np.diff(settle_decimal) * 1000
cumulative_cash_flow = np.r_[0, daily_cash_flow.cumsum()]

fig, ax = plt.subplots(figsize=(13,5.4))
ax.bar(days, cumulative_cash_flow, color="#4C78A8", edgecolor="black")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(days)
ax.set_xlabel("Day")
ax.set_ylabel("Cumulative gain ($)")
ax.set_title("Daily settlement makes gains and losses cash flows")
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-margin-account")


#| label: fig-futures-payoff
#| fig-cap: "Long and short futures positions have opposite payoffs"
import numpy as np
import matplotlib.pyplot as plt

f0 = 100
f1 = np.linspace(80, 120, 81)
long_payoff = f1 - f0
short_payoff = -long_payoff

plt.figure(figsize=(13,5.4))
plt.plot(f1, long_payoff, label="Long futures", linewidth=2)
plt.plot(f1, short_payoff, label="Short futures", linewidth=2)
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(f0, color="gray", linestyle="--", linewidth=1)
plt.xlabel("Futures price when position is closed")
plt.ylabel("Payoff per unit")
plt.title("Futures payoff profiles")
plt.grid(True, alpha=0.3)
plt.legend()
save(plt.gcf(),"lec9-fig-futures-payoff")


#| label: fig-short-rate-futures
#| fig-cap: "Short-term rate futures prices move inversely with the implied reference rate"
import numpy as np
import matplotlib.pyplot as plt

rates = np.linspace(3.0, 7.0, 81)
prices = 100 - rates

plt.figure(figsize=(13,5.4))
plt.plot(rates, prices, linewidth=2, color="#4C78A8")
plt.scatter([5.48, 6.00], [94.52, 94.00], color="#F58518", zorder=3)
plt.annotate("Sell at 94.52\nrate = 5.48%", xy=(5.48, 94.52), xytext=(3.35, 95.0),
             arrowprops={"arrowstyle": "->", "linewidth": 1})
plt.annotate("Settle at 94.00\nrate = 6.00%", xy=(6.00, 94.00), xytext=(5.9, 95.2),
             arrowprops={"arrowstyle": "->", "linewidth": 1})
plt.xlabel("Implied 3-month reference rate (%)")
plt.ylabel("Futures price")
plt.title("Price = 100 - reference rate")
plt.grid(True, alpha=0.3)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-short-rate-futures")


#| label: fig-ctd-cost
#| fig-cap: "The cheapest-to-deliver issue has the lowest delivery cost"
import numpy as np
import matplotlib.pyplot as plt

bonds = np.array(["A", "B", "C"])
cash_prices = np.array([103.20, 98.40, 91.10])
conversion_factors = np.array([1.0800, 1.0300, 0.9550])
futures_price = 94.00
invoice_before_ai = futures_price * conversion_factors
net_delivery_cost = cash_prices - invoice_before_ai

plt.figure(figsize=(13,5.4))
bars = plt.bar(bonds, net_delivery_cost, color=["#72B7B2", "#72B7B2", "#F58518"], edgecolor="black")
for bar, value in zip(bars, net_delivery_cost):
    plt.text(bar.get_x() + bar.get_width() / 2, value + 0.03, f"{value:.2f}", ha="center", fontsize=17)
plt.ylabel("Net delivery cost")
plt.xlabel("Deliverable bond")
plt.title("Lower delivery cost is better for the short")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-ctd-cost")


#| label: fig-arbitrage-profit
#| fig-cap: "Arbitrage pressure pushes the futures price toward the no-arbitrage value"
import numpy as np
import matplotlib.pyplot as plt

futures_prices = np.linspace(90, 108, 181)
cash_and_carry_profit = futures_prices + 3 - 102
reverse_profit = 102 - (futures_prices + 3)

plt.figure(figsize=(13,5.4))
plt.plot(futures_prices, cash_and_carry_profit, label="Cash-and-carry profit", linewidth=2)
plt.plot(futures_prices, reverse_profit, label="Reverse cash-and-carry profit", linewidth=2)
plt.axhline(0, color="black", linewidth=0.8)
plt.axvline(99, color="gray", linestyle="--", linewidth=1)
plt.text(99.2, 5.8, "No-arbitrage\nprice = 99", fontsize=17)
plt.xlabel("Futures price")
plt.ylabel("Profit")
plt.title("Only one futures price eliminates both arbitrage trades")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
save(plt.gcf(),"lec9-fig-arbitrage-profit")


#| label: fig-no-arbitrage-band
#| fig-cap: "Different borrowing and lending rates create a no-arbitrage band"
import matplotlib.pyplot as plt

lower = 98.50
upper = 99.00
prices = [98.0, lower, upper, 99.5]

fig, ax = plt.subplots(figsize=(13,5.4))
ax.hlines(0, prices[0], prices[-1], color="black", linewidth=1)
ax.axvspan(lower, upper, color="#E6F2E6", alpha=0.9, label="No-arbitrage band")
ax.scatter([lower, upper], [0, 0], color="#4C78A8", zorder=3)
ax.text(lower, 0.08, "98.50\nlower", ha="center", fontsize=17)
ax.text(upper, 0.08, "99.00\nupper", ha="center", fontsize=17)
ax.text(98.18, -0.12, "Reverse cash-and-carry\npressure", ha="center", fontsize=17)
ax.text(99.32, -0.12, "Cash-and-carry\npressure", ha="center", fontsize=17)
ax.set_xlim(prices[0], prices[-1])
ax.set_ylim(-0.25, 0.25)
ax.set_yticks([])
ax.set_xlabel("Futures price")
ax.set_title("Arbitrage is cleanest outside the band")
ax.spines[["left", "right", "top"]].set_visible(False)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-no-arbitrage-band")


#| label: fig-duration-adjustment
#| fig-cap: "Buying futures adds the dollar duration needed to reach the target"
import matplotlib.pyplot as plt

current_dd = 1_428_594
target_dd = 1_770_110
futures_dd = target_dd - current_dd

plt.figure(figsize=(13,5.4))
plt.bar(["Current\nportfolio", "Futures\nposition", "Target\nportfolio"], [current_dd, futures_dd, target_dd],
        color=["#4C78A8", "#F58518", "#72B7B2"], edgecolor="black")
plt.ylabel("Dollar duration ($ per 100 bp)")
plt.title("Duration adjustment with futures")
plt.grid(axis="y", alpha=0.3)
for i, value in enumerate([current_dd, futures_dd, target_dd]):
    plt.text(i, value + 25_000, f"${value:,.0f}", ha="center", fontsize=17)
plt.ylim(0, 2000000)
plt.tight_layout()
save(plt.gcf(),"lec9-fig-duration-adjustment")


#| label: fig-hedged-vs-unhedged
#| fig-cap: "A short futures hedge reduces the sensitivity of sale proceeds to interest-rate moves"
import numpy as np
import matplotlib.pyplot as plt

rate_move_bp = np.linspace(-100, 100, 81)
initial_value = 10_000_000
bond_dollar_duration_100bp = 1_363_000
hedge_effectiveness = 0.96

unhedged_value = initial_value - bond_dollar_duration_100bp * (rate_move_bp / 100)
futures_gain = hedge_effectiveness * bond_dollar_duration_100bp * (rate_move_bp / 100)
hedged_value = unhedged_value + futures_gain

plt.figure(figsize=(13,5.4))
plt.plot(rate_move_bp, unhedged_value / 1_000_000, label="Unhedged bond value", linewidth=2)
plt.plot(rate_move_bp, hedged_value / 1_000_000, label="Hedged value", linewidth=2)
plt.axvline(0, color="gray", linestyle="--", linewidth=1)
plt.xlabel("Interest-rate change (bp)")
plt.ylabel("Value ($ millions)")
plt.title("Short futures hedge offsets most rate-driven price change")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
save(plt.gcf(),"lec9-fig-hedged-vs-unhedged")


#| label: fig-allocation-shift
#| fig-cap: "Futures can temporarily shift asset allocation without immediate cash-market trading"
import matplotlib.pyplot as plt

before = [500, 500]
target = [300, 700]
labels = ["Equities", "Bonds"]
colors = ["#4C78A8", "#F58518"]

fig, axes = plt.subplots(1, 2, figsize=(13,5.4), sharey=True)
for ax, values, title in zip(axes, [before, target], ["Current allocation", "Target exposure"]):
    ax.bar(labels, values, color=colors, edgecolor="black")
    ax.set_title(title)
    ax.set_ylim(0, 800)
    ax.grid(axis="y", alpha=0.3)
    for i, value in enumerate(values):
        ax.text(i, value + 18, f"${value}m", ha="center", fontsize=17)

axes[0].set_ylabel("Exposure ($ millions)")
plt.tight_layout()
save(plt.gcf(),"lec9-fig-allocation-shift")
