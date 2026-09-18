"""Lecture 11 figures preserve the notes' numerical examples and chart data."""

from build_figures import *

#| label: fig-option-versus-futures
#| fig-cap: "A futures payoff is symmetric; a call payoff is one-sided"
import numpy as np
import matplotlib.pyplot as plt

terminal_futures = np.linspace(102, 118, 321)
futures_entry = 110
call_strike = 110

long_futures_payoff = terminal_futures - futures_entry
long_call_payoff = np.maximum(terminal_futures - call_strike, 0)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(terminal_futures, long_futures_payoff, color="#4C78A8", linewidth=2.2,
        label="Long futures payoff")
ax.plot(terminal_futures, long_call_payoff, color="#F58518", linewidth=2.2,
        linestyle="--", label="Long call payoff before premium")
ax.axhline(0, color="black", linewidth=0.9)
ax.axvline(call_strike, color="gray", linewidth=1, linestyle=":")
ax.set(xlabel="Futures price at expiration", ylabel="Payoff in price points",
       title="Futures and call payoffs at expiration")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-option-versus-futures")


#| label: fig-intrinsic-time-value
#| fig-cap: "Call value equals intrinsic value plus time value"
import math
import numpy as np
import matplotlib.pyplot as plt

def normal_cdf(x):
    """Standard normal cumulative distribution for scalars or arrays."""
    x = np.asarray(x, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(x / np.sqrt(2.0)))

def black_futures_call(futures_price, strike, time, rate, volatility):
    """European call on futures under Black's model, in price points."""
    futures_price = np.asarray(futures_price, dtype=float)
    vol_time = volatility * np.sqrt(time)
    d1 = (np.log(futures_price / strike) + 0.5 * volatility**2 * time) / vol_time
    d2 = d1 - vol_time
    return np.exp(-rate * time) * (
        futures_price * normal_cdf(d1) - strike * normal_cdf(d2)
    )

futures_prices = np.linspace(100, 120, 300)
strike = 110
# Set the discount rate to zero in this teaching picture so the plotted European
# value and the immediate-exercise intrinsic value share the same value basis.
# Later sections restore positive discounting in the full Black futures model.
call_value = black_futures_call(futures_prices, strike, 0.5, 0.00, 0.08)
intrinsic_value = np.maximum(futures_prices - strike, 0)
time_value = call_value - intrinsic_value

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(futures_prices, call_value, color="#4C78A8", linewidth=2.2, label="Call value")
ax.plot(futures_prices, intrinsic_value, color="black", linestyle="--", label="Intrinsic value")
ax.fill_between(futures_prices, intrinsic_value, call_value,
                where=call_value >= intrinsic_value, color="#F6C85F", alpha=0.45,
                label="Time value")
ax.axvline(strike, color="gray", linestyle=":")
ax.set(xlabel="Current futures price", ylabel="Option value (points)",
       title="Intrinsic value and time value of a call")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-intrinsic-time-value")


#| label: fig-four-option-profits
#| fig-cap: "Profit at expiration for the four basic option positions"
terminal_price = np.linspace(90, 130, 401)
strike = 110
call_premium = 3.0
put_premium = 2.5

profits = {
    "Long call": np.maximum(terminal_price - strike, 0) - call_premium,
    "Short call": call_premium - np.maximum(terminal_price - strike, 0),
    "Long put": np.maximum(strike - terminal_price, 0) - put_premium,
    "Short put": put_premium - np.maximum(strike - terminal_price, 0),
}

fig, axes = plt.subplots(2, 2, figsize=(22,12), sharex=True, sharey=True)
colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756"]

for ax, (name, profit), color in zip(axes.flat, profits.items(), colors):
    ax.plot(terminal_price, profit, color=color, linewidth=2.2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(strike, color="gray", linestyle=":", linewidth=1)
    ax.fill_between(terminal_price, 0, profit, where=profit >= 0, color=color, alpha=0.18)
    ax.fill_between(terminal_price, 0, profit, where=profit < 0, color="gray", alpha=0.15)
    ax.set_title(name)
    ax.grid(alpha=0.25)

axes[1, 0].set_xlabel("Underlying price at expiration")
axes[1, 1].set_xlabel("Underlying price at expiration")
axes[0, 0].set_ylabel("Profit (points)")
axes[1, 0].set_ylabel("Profit (points)")
plt.tight_layout()
fig.canvas.draw()
for k, ax in enumerate(axes.flat):
    for other in axes.flat: other.set_visible(other is ax)
    ax.tick_params(labelbottom=True,labelleft=True)
    ax.set_ylabel("Profit (points)" if "profits" in "fig-four-option-profits" else "Call value (points)")
    if "profits" in "fig-four-option-profits": ax.set_xlabel("Underlying price at expiration")
    fig.canvas.draw()
    box=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted()).expanded(1.03,1.04)
    fig.savefig(OUT/f"lec11-fig-four-option-profits-{k+1}.svg",bbox_inches=box)
plt.close(fig)


#| label: fig-put-call-parity
#| fig-cap: "A protective put and a fiduciary call have the same expiration value"
terminal_asset = np.linspace(70, 130, 301)
strike = 100

protective_put = terminal_asset + np.maximum(strike - terminal_asset, 0)
fiduciary_call = np.maximum(terminal_asset - strike, 0) + strike

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(terminal_asset, protective_put, color="#4C78A8", linewidth=3,
        label="Asset + put")
ax.plot(terminal_asset, fiduciary_call, color="#F58518", linewidth=1.8,
        linestyle="--", label="Call + strike cash")
ax.axvline(strike, color="gray", linestyle=":")
ax.set(xlabel="Asset price at expiration", ylabel="Position value at expiration",
       title="Equivalent positions from put-call parity")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-put-call-parity")


#| label: fig-option-input-sensitivities
#| fig-cap: "Call value rises with the underlying price, time, and volatility, but falls with the strike"
base_future = 110
base_strike = 110
base_time = 0.5
base_rate = 0.04
base_vol = 0.08

fig, axes = plt.subplots(2, 2, figsize=(22,12))

underlying_grid = np.linspace(100, 120, 100)
axes[0, 0].plot(underlying_grid,
                black_futures_call(underlying_grid, base_strike, base_time, base_rate, base_vol),
                color="#4C78A8")
axes[0, 0].set(title="Current futures price", xlabel="$F_0$", ylabel="Call value")

strike_grid = np.linspace(100, 120, 100)
axes[0, 1].plot(strike_grid,
                [black_futures_call(base_future, k, base_time, base_rate, base_vol) for k in strike_grid],
                color="#F58518")
axes[0, 1].set(title="Strike price", xlabel="$K$", ylabel="Call value")

time_grid = np.linspace(0.03, 2.0, 100)
axes[1, 0].plot(time_grid,
                [black_futures_call(base_future, base_strike, t, base_rate, base_vol) for t in time_grid],
                color="#54A24B")
axes[1, 0].set(title="Time to expiration", xlabel="$T$ (years)", ylabel="Call value")

vol_grid = np.linspace(0.01, 0.20, 100)
axes[1, 1].plot(100 * vol_grid,
                [black_futures_call(base_future, base_strike, base_time, base_rate, v) for v in vol_grid],
                color="#B279A2")
axes[1, 1].set(title="Price volatility", xlabel="$\sigma$ (%)", ylabel="Call value")

for ax in axes.flat:
    ax.grid(alpha=0.3)

plt.tight_layout()
fig.canvas.draw()
for k, ax in enumerate(axes.flat):
    for other in axes.flat: other.set_visible(other is ax)
    ax.tick_params(labelbottom=True,labelleft=True)
    ax.set_ylabel("Profit (points)" if "profits" in "fig-option-input-sensitivities" else "Call value (points)")
    if "profits" in "fig-option-input-sensitivities": ax.set_xlabel("Underlying price at expiration")
    fig.canvas.draw()
    box=ax.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted()).expanded(1.03,1.04)
    fig.savefig(OUT/f"lec11-fig-option-input-sensitivities-{k+1}.svg",bbox_inches=box)
plt.close(fig)


#| label: fig-call-value-volatility
#| fig-cap: "Volatility adds the most visible value near the strike"
price_grid = np.linspace(95, 125, 250)
fig, ax = plt.subplots(figsize=(13,5.4))

for volatility, color, style in [(0.04, "#9ECAE1", "-"),
                                  (0.08, "#4C78A8", "--"),
                                  (0.16, "#F58518", "-.")]:
    ax.plot(price_grid,
            black_futures_call(price_grid, 110, 0.5, 0.04, volatility),
            color=color, linestyle=style, linewidth=2,
            label=f"Volatility = {100 * volatility:.0f}%")

ax.plot(price_grid, np.maximum(price_grid - 110, 0), color="black", linewidth=1.2,
        label="Intrinsic value")
ax.set(xlabel="Current futures price", ylabel="Call value (points)",
       title="Call value across price and volatility")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-call-value-volatility")


#| label: binomial-visual-helper
#| include: false
def binomial_option_price(spot, strike, time, rate, volatility,
                          steps, option_type="call", american=False):
    """Price a call or put in a Cox-Ross-Rubinstein binomial tree."""
    dt = time / steps
    up = np.exp(volatility * np.sqrt(dt))
    down = 1.0 / up
    probability_up = (np.exp(rate * dt) - down) / (up - down)

    if not 0 < probability_up < 1:
        raise ValueError("Tree parameters do not produce a valid probability.")

    up_moves = np.arange(steps + 1)
    terminal_prices = spot * up**up_moves * down**(steps - up_moves)

    if option_type == "call":
        option_values = np.maximum(terminal_prices - strike, 0.0)
    elif option_type == "put":
        option_values = np.maximum(strike - terminal_prices, 0.0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Step backward from expiration to today.
    for step in range(steps - 1, -1, -1):
        option_values = np.exp(-rate * dt) * (
            probability_up * option_values[1:] +
            (1.0 - probability_up) * option_values[:-1]
        )

        if american:
            node_up_moves = np.arange(step + 1)
            node_prices = spot * up**node_up_moves * down**(step - node_up_moves)
            if option_type == "call":
                exercise_values = np.maximum(node_prices - strike, 0.0)
            else:
                exercise_values = np.maximum(strike - node_prices, 0.0)
            option_values = np.maximum(option_values, exercise_values)

    return float(option_values[0])
closed_form_call = 4.8673436512


#| label: fig-binomial-convergence
#| fig-cap: "The binomial value converges toward the closed-form European option value"
step_counts = np.arange(5, 201)
tree_values = np.array([
    binomial_option_price(92, 90, 0.5, 0.04, 0.10, int(n), "call")
    for n in step_counts
])

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(step_counts, tree_values, color="#4C78A8", linewidth=1.5, label="Binomial value")
ax.axhline(closed_form_call, color="#F58518", linestyle="--", linewidth=2,
           label="Black-Scholes value")
ax.set(xlabel="Number of time steps", ylabel="Call value",
       title="Binomial-tree convergence")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-binomial-convergence")


#| label: fig-implied-volatility-smile
#| fig-cap: "A stylized implied-volatility smile across option strikes"
strikes = np.arange(80, 105, 2.5)
stylized_implied_vol = 0.09 + 0.00012 * (strikes - 92.5)**2

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(strikes, 100 * stylized_implied_vol, "o-", color="#4C78A8")
ax.axvline(92.5, color="gray", linestyle=":", label="Near at-the-money")
ax.set(xlabel="Strike price", ylabel="Implied volatility (%)",
       title="Stylized bond-option volatility smile")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-implied-volatility-smile")


#| label: fig-protective-put-hedge
#| fig-cap: "Protective puts establish a floor while preserving gains above the strike"
initial_futures = 110.0
put_strike = 110.0
put_premium = 1.25
contracts = 100
dollars_per_point = 1_000
premium_cost = contracts * dollars_per_point * put_premium
futures_scenarios = np.linspace(102, 118, 321)
bond_change = contracts * dollars_per_point * (futures_scenarios - initial_futures)
protective_put_change = (
    bond_change
    + contracts * dollars_per_point * np.maximum(put_strike - futures_scenarios, 0)
    - premium_cost
)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(futures_scenarios, bond_change / 1_000, color="#4C78A8", linewidth=2,
        label="Unhedged bond portfolio")
ax.plot(futures_scenarios, protective_put_change / 1_000, color="#F58518",
        linewidth=2.2, linestyle="--", label="Bond portfolio + puts")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(put_strike, color="gray", linestyle=":")
ax.set(xlabel="Treasury futures price at expiration",
       ylabel="Net change ($ thousands)",
       title="Long-bond protective-put hedge")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-protective-put-hedge")


#| label: fig-covered-call
#| fig-cap: "Covered call writing adds premium income but caps gains above the strike"
call_strike = 113.0
call_premium = 1.0
long_change = contracts * dollars_per_point * (futures_scenarios - initial_futures)
covered_change = long_change + contracts * dollars_per_point * (
    call_premium - np.maximum(futures_scenarios - call_strike, 0)
)

fig, ax = plt.subplots(figsize=(13,5.4))
ax.plot(futures_scenarios, long_change / 1_000, color="#4C78A8", linewidth=2,
        label="Long bond exposure")
ax.plot(futures_scenarios, covered_change / 1_000, color="#54A24B",
        linewidth=2.2, linestyle="--", label="Long bonds + short calls")
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(call_strike, color="gray", linestyle=":")
ax.set(xlabel="Treasury futures price at expiration",
       ylabel="Net change ($ thousands)",
       title="Covered call writing on mapped bond exposure")
ax.legend()
ax.grid(alpha=0.3)
save(plt.gcf(),"lec11-fig-covered-call")


# Branching topology for the notes' instrument-choice map and one-period example.
from matplotlib.patches import FancyArrowPatch

def diagram_box(ax, x, y, text, color='#E8EDE1', size=20):
    ax.text(x,y,text,ha='center',va='center',fontsize=size,
            bbox=dict(boxstyle='round,pad=.6',facecolor=color,edgecolor=GREEN))

def arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=20,color=GOLD,lw=2))

fig,ax=plt.subplots(figsize=(13,5.4));ax.set_axis_off();ax.set(xlim=(0,10),ylim=(0,5))
diagram_box(ax,2,2.5,'Today\nBond = 100\nCall = ?')
diagram_box(ax,7.5,3.8,'Up state\nBond = 110\nCall payoff = 10')
diagram_box(ax,7.5,1.2,'Down state\nBond = 90\nCall payoff = 0')
arrow(ax,(3.2,2.8),(6.1,3.7));arrow(ax,(3.2,2.2),(6.1,1.3));save(fig,'lec11-one-period-tree')
fig,ax=plt.subplots(figsize=(13,5.4));ax.set_axis_off();ax.set(xlim=(0,12),ylim=(0,5.5))
diagram_box(ax,6,4.6,'Fixed-income risk',size=21)
for x,goal,instrument in [(1.4,'Lock\nexposure','Futures'),(4.5,'Protect\ndownside','Buy put'),(7.5,'Cap adverse\nupside risk','Buy call'),(10.6,'Earn\npremium','Write option')]:
    diagram_box(ax,x,2.6,goal,size=19);diagram_box(ax,x,.6,instrument,'#F6E8C3',19)
    arrow(ax,(6,4.15),(x,3.23));arrow(ax,(x,1.98),(x,1.06))
save(fig,'lec11-option-decision-tree')
