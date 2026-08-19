# Team Project Fallback Data

These files are a complete fallback when a team cannot retrieve a consistent real-market dataset. Real data remain preferred. The fallback observations are **synthetic teaching data**, calibrated to plausible market relationships as of **2025-01-15** unless a row states another date. They are not executable quotes and must not be presented as current market data.

## Use and citation

1. Use the official sources linked in the project first.
2. If access, licensing, timing, or matching prevents a reproducible download, use the named lecture CSV without requesting a separate instructor file.
3. Cite the file name, observation date, and this note. Distinguish supplied inputs from team estimates.
4. Preserve units: prices are per 100 of par; rates, yields, spreads, volatilities, and weights are percentages unless a column name says `_bp`, `_years`, `_usd`, or `_mm`.

## Files and fields

- `lecture-1-bond-features.csv`: issuer funding facts and three debt structures. `secured` and `callable` are yes/no flags; `asset_duration_years` and `funding_need_years` support the treasurer case.
- `lecture-2-pricing.csv`: same-date bond terms and horizon assumptions. `clean_price` excludes accrued interest; `accrued_interest` is per 100; `sale_ytm_pct` and `reinvestment_rate_pct` are scenario inputs.
- `lecture-3-duration-convexity.csv`: liability and government-bond present values (PV), modified duration, convexity, and key-rate durations (KRD). KRD columns are years of sensitivity and sum approximately to modified duration.
- `lecture-4-curves.csv`: par yields at common maturities on two dates, plus short event labels.
- `lecture-4-bootstrap.csv`: semiannual-pay instruments at a common settlement date. Coupon is annual; cash-flow intervals are 0.5 years; prices are clean and accrued interest is zero.
- `lecture-5-markets.csv`: matched Treasury liquidity/repo observations and a synthetic corporate credit-event window. `repo_rate_pct` below `general_collateral_repo_pct` indicates specialness.
- `lecture-6-portfolio.csv`: a 12-bond universe with benchmark and current weights, risk, liquidity, and trading-cost fields. `withdrawal_year` and `withdrawal_usd` define the five annual client cash needs; the nonprofit case has a 4.75-year duration target, BBB minimum, 5% issuer limit, 20% minimum government weight, and 15% annual turnover limit.
- `lecture-7-rate-models.csv`: monthly short rates, a current zero curve, model assumptions, scenario outputs, and liability facts distinguished by `record_type`. Rate-model parameter units are described in `notes`.
- `lecture-8-optionality.csv`: callable/option-free bonds, a recombining short-rate tree, mortgage scenarios, and two option-adjusted spread (OAS) model outputs distinguished by `record_type`.
- `lecture-9-futures.csv`: portfolio and contract DV01, delivery candidates, two Secured Overnight Financing Rate (SOFR) strips, and margin assumptions distinguished by `record_type`. DV01 is dollars per one basis-point move.
- `lecture-10-credit.csv`: holdings and claims with spreads, spread duration, default and recovery assumptions, rating transitions, covenants, and enterprise-value scenarios.
- `lecture-11-rate-options.csv`: borrower terms, cap/floor/swap quotes, Treasury-futures options, and volatility cases distinguished by `record_type`. Premiums are in basis points of notional unless noted.

## Validation notes

The files use comma-separated values with a single header row and no embedded commas. Missing fields are intentionally blank when they do not apply to a record type. Totals and basic identities are designed for checking: Lecture 6 benchmark and current weights each sum to 100%; Lecture 10 portfolio weights sum to 100%; and Lecture 9 SOFR implied rates equal `100 - futures_price`.
