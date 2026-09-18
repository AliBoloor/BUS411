"""Lecture 6 figures from the read-only lecture-note calculations."""

from build_figures import *

import pandas as pd

plt.rcParams["figure.figsize"]=(13,5.4)

R_RED=GOLD; R_GREEN=GREEN; R_BLUE=BLUE; R_CYAN=BLUE; R_ORANGE=GOLD; R_PURPLE="#85618b"; R_GRAY="#9ca99f"

#| label: fig-efficient-frontier
#| fig-cap: "Stylized mean-variance frontier. The efficient frontier contains portfolios with the highest expected return for each risk level."
#| echo: false
#| message: false
#| warning: false

risk_grid = np.linspace(2, 12, 100)
min_variance_return = 1.8 + 0.35 * risk_grid - 0.012 * (risk_grid - 7) ** 2
inefficient_return = min_variance_return - 1.5 - 0.15 * np.cos(risk_grid)

fig, ax = plt.subplots()
ax.plot(risk_grid, min_variance_return, color="#2563eb", linewidth=2.8, label="Efficient frontier")
ax.scatter(risk_grid[::10], inefficient_return[::10], color="#94a3b8", s=45, label="Inefficient portfolios")
ax.scatter([risk_grid[10]], [min_variance_return[10]], color="#16a34a", s=80, zorder=3, label="Lower-risk efficient portfolio")
ax.scatter([risk_grid[70]], [min_variance_return[70]], color="#dc2626", s=80, zorder=3, label="Higher-risk efficient portfolio")
ax.set_title("Mean-Variance Portfolio Selection")
ax.set_xlabel("Portfolio risk")
ax.set_ylabel("Expected return")
ax.legend(loc="best")
plt.tight_layout()
save(fig,"lec6-fig-efficient-frontier")


#| echo: false
#| message: false
#| warning: false

months_lbl = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
benchmark = np.array([0.04, 1.54, 0.00, 0.54, 0.76, 0.30, 0.83, 1.23, 0.76, 0.90, 1.04, 0.28])
portfolio_a = np.array([0.02, 1.58, 0.04, 0.61, 0.71, 0.27, 0.91, 1.26, 0.69, 0.95, 1.08, 0.02])
portfolio_b = np.array([1.05, 2.13, 0.37, 1.01, 1.44, 0.57, 1.95, 1.26, 2.17, 1.80, 2.13, 0.32])

tracking_example = pd.DataFrame(
    {
        "Month": months_lbl,
        "Benchmark return (%)": benchmark,
        "Portfolio A return (%)": portfolio_a,
        "A active return (%)": portfolio_a - benchmark,
        "Portfolio B return (%)": portfolio_b,
        "B active return (%)": portfolio_b - benchmark,
    }
)


#| echo: false
#| message: false
#| warning: false

active_a = portfolio_a - benchmark
active_b = portfolio_b - benchmark
te_a = active_a.std(ddof=1)
te_b = active_b.std(ddof=1)
summary_te = pd.DataFrame(
    {
        "Portfolio": ["A", "B"],
        "Monthly TE (%)": [te_a, te_b],
        "Monthly TE (bps)": [te_a * 100, te_b * 100],
        "Annualized TE (bps)": [te_a * np.sqrt(12) * 100, te_b * np.sqrt(12) * 100],
    }
)
summary_te.round(2)


#| label: fig-active-returns
#| fig-cap: "Monthly active returns for two portfolios. Portfolio B has much larger tracking error."
#| echo: false
#| message: false
#| warning: false

x = np.arange(len(months_lbl))
fig, ax = plt.subplots()
ax.bar(x - 0.18, active_a * 100, width=0.36, label="Portfolio A", color=R_BLUE)
ax.bar(x + 0.18, active_b * 100, width=0.36, label="Portfolio B", color=R_RED)
ax.axhline(0, color="#334155", linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(months_lbl)
ax.set_title("Active Returns Drive Tracking Error")
ax.set_ylabel("Active return (bps)")
ax.legend(loc="best")
plt.tight_layout()
save(fig,"lec6-fig-active-returns")


#| echo: false
#| message: false
#| warning: false

strategy_te = pd.DataFrame(
    {
        "Strategy": ["Pure indexing", "Enhanced indexing", "Active benchmark-aware", "Unconstrained / absolute return"],
        "Typical active risk": ["Near zero", "Low", "Moderate to high", "Benchmark may not control risk"],
        "Main objective": [
            "Replicate benchmark",
            "Small active gains with tight risk control",
            "Outperform benchmark using views",
            "Maximize absolute or risk-adjusted return",
        ],
    }
)
strategy_te


#| echo: false
#| message: false
#| warning: false

cell_example = pd.DataFrame(
    {
        "Sector": ["Treasury", "Agencies", "Corporates", "Agency MBS"],
        "Benchmark weight (%)": [33.3, 6.8, 26.6, 33.3],
        "Portfolio weight (%)": [29.5, 3.6, 34.8, 29.0],
    }
)
cell_example["Active weight (%)"] = cell_example["Portfolio weight (%)"] - cell_example["Benchmark weight (%)"]


#| label: fig-cell-sector-weights
#| fig-cap: "Example sector active weights. A cell-based approach makes benchmark tilts visible."
#| echo: false
#| message: false
#| warning: false

fig, ax = plt.subplots()
colors = np.where(cell_example["Active weight (%)"] >= 0, R_GREEN, R_RED)
ax.bar(cell_example["Sector"], cell_example["Active weight (%)"], color=colors)
ax.axhline(0, color="#334155", linewidth=1)
ax.set_title("Portfolio Active Weights by Sector")
ax.set_ylabel("Active weight (percentage points)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
save(fig,"lec6-fig-cell-sector-weights")


#| echo: false
#| message: false
#| warning: false
#| output: false

decomp = pd.DataFrame(
    {
        "Risk factor": [
            "Treasury level",
            "2-year key rate",
            "10-year key rate",
            "IG corporate spread",
            "Securitized spread",
        ],
        "Active exposure": [0.20, -0.10, 0.15, 0.60, -0.25],
        "Monthly factor volatility (bps)": [30, 25, 35, 18, 16],
    }
)
decomp["Isolated TE (bps/month)"] = (
    decomp["Active exposure"].abs() * decomp["Monthly factor volatility (bps)"]
)
decomp["Variance contribution if uncorrelated"] = decomp["Isolated TE (bps/month)"] ** 2
decomp["Share of uncorrelated systematic variance"] = (
    decomp["Variance contribution if uncorrelated"]
    / decomp["Variance contribution if uncorrelated"].sum()
)
decomp[
    [
        "Risk factor",
        "Active exposure",
        "Monthly factor volatility (bps)",
        "Isolated TE (bps/month)",
    ]
].round(2)


#| label: fig-risk-decomposition-isolated-te
#| fig-cap: "Isolated tracking error shows which active exposures are large before considering diversification across factors."
#| echo: false
#| message: false
#| warning: false

plot_decomp = decomp.sort_values("Isolated TE (bps/month)")
fig, ax = plt.subplots()
ax.barh(
    plot_decomp["Risk factor"],
    plot_decomp["Isolated TE (bps/month)"],
    color=R_BLUE,
)
ax.set_title("Step 1: Isolated Active Risk by Factor")
ax.set_xlabel("Isolated tracking error (bps/month)")
for i, value in enumerate(plot_decomp["Isolated TE (bps/month)"]):
    ax.text(value + 0.2, i, f"{value:.1f}", va="center")
plt.tight_layout()
save(fig,"lec6-fig-risk-decomposition-isolated-te")


#| echo: false
#| message: false
#| warning: false

uncorrelated_systematic_te = np.sqrt(
    decomp["Variance contribution if uncorrelated"].sum()
)
simple_sum_te = decomp["Isolated TE (bps/month)"].sum()
pd.DataFrame(
    {
        "Method": [
            "Incorrect simple sum",
            "Correct uncorrelated systematic TE",
        ],
        "Result (bps/month)": [simple_sum_te, uncorrelated_systematic_te],
    }
).round(2)


#| label: fig-correlation-effect
#| fig-cap: "Correlation changes total tracking error even when isolated factor risks are unchanged."
#| echo: false
#| message: false
#| warning: false

rho_grid = np.linspace(-0.9, 0.9, 181)
te_rate = 6.0
te_spread = 10.8
combined_te = np.sqrt(
    te_rate**2 + te_spread**2 + 2 * rho_grid * te_rate * te_spread
)

fig, ax = plt.subplots()
ax.plot(rho_grid, combined_te, color="#dc2626", linewidth=2.5)
ax.axvline(0, color="#334155", linewidth=1)
ax.set_title("Step 3: Correlation Changes Combined Risk")
ax.set_xlabel("Correlation between Treasury and spread active returns")
ax.set_ylabel("Combined tracking error (bps/month)")
for rho in [-0.5, 0, 0.5]:
    te = np.sqrt(te_rate**2 + te_spread**2 + 2 * rho * te_rate * te_spread)
    ax.scatter(rho, te, color="#111827")
    ax.text(rho + 0.03, te, f"{te:.1f}", va="center")
plt.tight_layout()
save(fig,"lec6-fig-correlation-effect")


#| echo: false
#| message: false
#| warning: false

idio_te = 8.0
total_te = np.sqrt(uncorrelated_systematic_te**2 + idio_te**2)
pd.DataFrame(
    {
        "Component": ["Systematic TE", "Idiosyncratic TE", "Total TE"],
        "bps/month": [uncorrelated_systematic_te, idio_te, total_te],
        "bps/year": [
            uncorrelated_systematic_te * np.sqrt(12),
            idio_te * np.sqrt(12),
            total_te * np.sqrt(12),
        ],
    }
).round(2)


#| label: fig-systematic-idio-risk
#| fig-cap: "Total tracking error combines systematic factor risk and idiosyncratic security-selection risk in variance terms."
#| echo: false
#| message: false
#| warning: false

components = pd.DataFrame(
    {
        "Component": ["Systematic", "Idiosyncratic"],
        "Variance": [uncorrelated_systematic_te**2, idio_te**2],
    }
)
components["Share"] = components["Variance"] / components["Variance"].sum()

fig, ax = plt.subplots()
ax.bar(
    components["Component"],
    components["Share"] * 100,
    color=[R_BLUE, R_ORANGE],
)
ax.set_title("Step 4: What Drives Total Tracking Error?")
ax.set_ylabel("Share of total TE variance (%)")
for i, row in components.iterrows():
    ax.text(i, row["Share"] * 100 + 1, f"{row['Share'] * 100:.0f}%", ha="center")
plt.tight_layout()
save(fig,"lec6-fig-systematic-idio-risk")


#| echo: false
#| message: false
#| warning: false

scenario = decomp[["Risk factor", "Active exposure"]].copy()
scenario["Factor change (bps)"] = [40, 20, 50, 25, 15]
scenario["Active return impact (bps)"] = (
    -scenario["Active exposure"] * scenario["Factor change (bps)"]
)


#| echo: false
#| message: false
#| warning: false

scenario_total = scenario["Active return impact (bps)"].sum()
pd.DataFrame(
    {
        "Measure": ["Total approximate active return"],
        "bps": [scenario_total],
    }
).round(2)


#| label: fig-scenario-active-return
#| fig-cap: "Scenario analysis converts active exposures into signed active return impacts."
#| echo: false
#| message: false
#| warning: false

fig, ax = plt.subplots()
colors = np.where(scenario["Active return impact (bps)"] >= 0, R_GREEN, R_RED)
ax.barh(scenario["Risk factor"], scenario["Active return impact (bps)"], color=colors)
ax.axvline(0, color="#334155", linewidth=1)
ax.set_title("Step 5: Scenario Active Return by Factor")
ax.set_xlabel("Approximate active return impact (bps)")
ax.set_xlim(-18, 5)
for i, value in enumerate(scenario["Active return impact (bps)"]):
    offset = 0.25 if value >= 0 else -0.25
    ha = "left" if value >= 0 else "right"
    ax.text(value + offset, i, f"{value:.1f}", va="center", ha=ha)
plt.tight_layout()
save(fig,"lec6-fig-scenario-active-return")


#| echo: false
#| message: false
#| warning: false

key_rate_table = pd.DataFrame(
    {
        "Key rate": ["2Y", "5Y", "10Y", "30Y"],
        "Portfolio KRD": [0.70, 1.35, 2.10, 1.25],
        "Benchmark KRD": [1.00, 1.30, 1.70, 1.40],
    }
)
key_rate_table["Active KRD"] = (
    key_rate_table["Portfolio KRD"] - key_rate_table["Benchmark KRD"]
)
key_rate_table.round(2)


#| label: fig-key-rate-decomposition
#| fig-cap: "Key rate decomposition reveals curve-shape risk that total duration can hide."
#| echo: false
#| message: false
#| warning: false

fig, ax1 = plt.subplots()
x = np.arange(len(key_rate_table))
width = 0.36
ax1.bar(
    x - width / 2,
    key_rate_table["Portfolio KRD"],
    width,
    label="Portfolio",
    color=R_BLUE,
)
ax1.bar(
    x + width / 2,
    key_rate_table["Benchmark KRD"],
    width,
    label="Benchmark",
    color=R_GRAY,
)
ax1.set_xticks(x)
ax1.set_xticklabels(key_rate_table["Key rate"])
ax1.set_ylabel("Key rate duration")
ax1.set_title("Same Total Duration, Different Curve Exposure")
ax1.legend(loc="upper left")
plt.tight_layout()
save(fig,"lec6-fig-key-rate-decomposition")


#| echo: false
#| message: false
#| warning: false

candidate_bonds = pd.DataFrame(
    {
        "Bond": ["Treasury 5Y", "Treasury 10Y", "Agency MBS", "A industrial", "BBB financial"],
        "Yield (%)": [4.3, 4.6, 5.1, 5.4, 6.0],
        "Duration": [4.6, 8.2, 4.1, 5.7, 6.1],
        "Spread duration": [0.0, 0.0, 3.2, 5.4, 5.8],
        "Sector": ["Treasury", "Treasury", "MBS", "Corporate", "Corporate"],
        "Weight chosen (%)": [25, 15, 25, 20, 15],
    }
)
candidate_bonds


#| echo: false
#| message: false
#| warning: false

w = candidate_bonds["Weight chosen (%)"].to_numpy() / 100
toy_summary = pd.DataFrame(
    {
        "Portfolio metric": ["Yield", "Duration", "Spread duration", "Treasury weight", "Corporate weight"],
        "Value": [
            np.sum(w * candidate_bonds["Yield (%)"]),
            np.sum(w * candidate_bonds["Duration"]),
            np.sum(w * candidate_bonds["Spread duration"]),
            candidate_bonds.loc[candidate_bonds["Sector"] == "Treasury", "Weight chosen (%)"].sum(),
            candidate_bonds.loc[candidate_bonds["Sector"] == "Corporate", "Weight chosen (%)"].sum(),
        ],
        "Benchmark / constraint": [5.0, 5.0, 3.0, ">= 30", "<= 40"],
    }
)


#| label: fig-toy-portfolio-exposures
#| fig-cap: "Toy portfolio construction: chosen exposures compared with target exposures."
#| echo: false
#| message: false
#| warning: false

toy_exposure = pd.DataFrame(
    {
        "Exposure": ["Yield", "Duration", "Spread duration"],
        "Portfolio": toy_summary.loc[:2, "Value"].astype(float).to_numpy(),
        "Target": [5.0, 5.0, 3.0],
    }
)
xpos = np.arange(len(toy_exposure))
fig, ax = plt.subplots()
ax.bar(xpos - 0.18, toy_exposure["Portfolio"], width=0.36, label="Portfolio", color=R_BLUE)
ax.bar(xpos + 0.18, toy_exposure["Target"], width=0.36, label="Target", color=R_ORANGE)
ax.set_xticks(xpos)
ax.set_xticklabels(toy_exposure["Exposure"])
ax.set_title("Optimizer Goal: Match Desired Exposures")
ax.set_ylabel("Percent or years")
ax.legend(loc="best")
plt.tight_layout()
save(fig,"lec6-fig-toy-portfolio-exposures")


#| echo: false
#| message: false
#| warning: false

rebalance_exposures = pd.DataFrame(
    {
        "Exposure": ["Duration gap", "Corporate active weight", "Bank active weight", "Issuer concentration", "Predicted TE"],
        "Before": [0.32, 9.5, 8.0, 4.2, 14.8],
        "After": [0.18, 6.2, 5.0, 2.9, 10.6],
        "Limit": [0.25, 8.0, 5.0, 3.0, 12.0],
        "Unit": ["years", "%", "%", "%", "bps/month"],
    }
)


#| label: fig-rebalance-before-after
#| fig-cap: "Rebalancing should target the exposures that violate risk limits, not mechanically eliminate all active views."
#| echo: false
#| message: false
#| warning: false

plot_reb = rebalance_exposures.copy()
plot_reb["Before / limit"] = plot_reb["Before"] / plot_reb["Limit"]
plot_reb["After / limit"] = plot_reb["After"] / plot_reb["Limit"]

xpos = np.arange(len(plot_reb))
fig, ax = plt.subplots()
ax.bar(xpos - 0.18, plot_reb["Before / limit"], width=0.36, label="Before", color=R_RED)
ax.bar(xpos + 0.18, plot_reb["After / limit"], width=0.36, label="After", color=R_GREEN)
ax.axhline(1.0, color="#334155", linestyle="--", linewidth=1.2, label="Risk limit")
ax.set_xticks(xpos)
ax.set_xticklabels(plot_reb["Exposure"], rotation=20, ha="right")
ax.set_title("Before and After Rebalancing")
ax.set_ylabel("Exposure as multiple of limit")
ax.legend(loc="best")
plt.tight_layout()
save(fig,"lec6-fig-rebalance-before-after")


#| label: fig-rebalance-frontier
#| fig-cap: "Illustrative tradeoff between transaction cost and tracking error reduction."
#| echo: false
#| message: false
#| warning: false

trades = np.arange(0, 21)
te_before = 12.0
te_after = te_before - 4.0 * (1 - np.exp(-trades / 5))
cost = 1.2 * trades + 0.04 * trades**2

fig, ax1 = plt.subplots()
ax1.plot(trades, te_after, color="#2563eb", linewidth=2.5, marker="o", label="Predicted TE")
ax1.set_xlabel("Number of trades")
ax1.set_ylabel("Predicted TE (bps/month)", color="#2563eb")
ax1.tick_params(axis="y", labelcolor="#2563eb")

ax2 = ax1.twinx()
ax2.plot(trades, cost, color="#dc2626", linewidth=2.5, marker="s", label="Transaction cost")
ax2.set_ylabel("Transaction cost (bps)", color="#dc2626")
ax2.tick_params(axis="y", labelcolor="#dc2626")
ax2.grid(False)

ax1.set_title("Rebalancing: Risk Reduction Has a Cost")
plt.tight_layout()
save(fig,"lec6-fig-rebalance-frontier")
