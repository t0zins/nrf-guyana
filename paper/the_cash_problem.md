# The Cash Problem: Asset Allocation, Not Withdrawal Rates, Is Guyana's Defensible Sovereign Wealth Failure

*Draft — September 2026. Companion code and data: `nrf_simulation.py` (v3, this run), `nrf_ingest.py`, and a verified quarterly dataset compiled from Bank of Guyana quarterly reports (§8.9).*

---

## Abstract

Guyana's Natural Resource Fund (NRF) is run at two extremes simultaneously: the government withdraws essentially 100% of an escalating statutory ceiling every year, and the Bank of Guyana holds the retained balance entirely as overnight cash at the Federal Reserve Bank of New York. A paired Monte Carlo model of total national wealth — fund balance plus withdrawals compounded at a domestic social return ρ — shows that the first of these is not a failure that the evidence can convict. The gross social return to core infrastructure in capital-scarce economies is high enough that, even after the public-investment efficiency losses documented for low-capacity states, a well-selected marginal project plausibly clears the model's ~4.1% breakeven. Holding the withdrawal rule fixed, the breakeven for the front-loading critique alone is not 4.1% but the cash return itself, about 0.5% real. The second extreme is different. Because ρ is applied only to money that leaves the fund, it never touches the retained balance, and the cost of holding that balance in cash rather than a diversified portfolio is invariant to ρ by construction. That cost is a median US$24.8B (real 2026) over 2026–2055 under the current schedule, positive at every cash real return from 0% to 2.0%, and breaks only when overnight cash is assumed to earn the portfolio's own median compound return. The cost is not only prospective. On the Bank of Guyana's own published figure, the fund has returned 2.687% a year since inception against roughly 4% annualized US inflation over the same period — a real return of about −1.3% a year. Guyana's sovereign wealth fund has lost purchasing power over its entire life. The thirty-year figure is the forward magnitude of a failure that is already realized, and the institutional failure is that a mandate producing it has been reaffirmed four times, most recently in March 2026.

---

## 1. Introduction

**The claim we make.** Guyana holds the Natural Resource Fund as cash. The Bank of Guyana's audited quarterly financial summaries record the line item "Financial Assets held at fair value through profit and loss" at exactly zero in every quarter for which the Assets table is published — 2023Q3, 2023Q4, 2025Q3, 2025Q4, 2026Q1 and 2026Q2 — with the entire fund sitting under "Cash and Cash Equivalents" (Bank of Guyana, NRF Quarterly Reports, Table 4). Each report carries the same footnote: *"The Fund is not currently tracking an index as funds were not invested in securities as at [date]."* The investment mandate that produces this — all funds in an overnight deposit account at the Federal Reserve Bank of New York at the prevailing federal funds rate — was approved by the NRF Board on June 26, 2023 and has been reaffirmed repeatedly since, most recently on March 27, 2026 (§2.3). This paper argues that the allocation, not the withdrawal rate, is the defensible sovereign-wealth failure: it has already cost the fund purchasing power over its entire life, it costs a median US$24.8B in real 2026 terms over the next thirty years, and — the property that makes it *defensible* — that cost does not depend on any assumption about how productively Guyana spends what it withdraws.

**The claim we do not make.** We do not argue that Guyana should withdraw less. An earlier version of this project set out to show that drawing the full statutory ceiling every year — US$607.6M in 2022, US$1,002.13M in 2023, US$1,586M in 2024, US$2,463M in 2025 (Bank of Guyana Quarterly Reports 2022–2023; Ministry of Finance 2024; NRF Annual Report 2025) — destroys wealth relative to a Norway-style rule because the domestic social return on that money sits below the model's breakeven. The evidence assembled to test that claim (§6) does not support it. Chari, Henry and Picardo (NBER Working Paper 34501, November 2025) estimate a median social return of 55% to an additional kilometre of two-lane highway in emerging and developing economies; even after the IMF's low-income-country efficiency gap of around 40% on average and up to 53% (IMF 134-country study; IMF WP/24/232, 2024), that leaves a net real return far above 4.1%. The front-loading critique fails on its own terms for well-selected core infrastructure. We say so here, again in §6, and we do not soften it.

**The concession does not touch the claim.** The model's accounting identity is what separates the two. Total national wealth at the horizon is the fund's terminal balance plus every withdrawal compounded forward at ρ. Under a given withdrawal rule, the cash arm and the portfolio arm take identical withdrawals on identical paths — the run confirms the withdrawal matrices are bit-identical across all 10,000 paths — so the difference between them is a difference in the retained balance alone. ρ multiplies the withdrawals, which cancel. Whatever Guyana earns on the money it spends, it earns overnight interest on the money it keeps, and whether that is the right return on a thirty-year balance is separable from, and survives, any view of how well the country spends.

**The scope of the claim.** Part of the cost is already realized and part is prospective, and the two rest on different evidence.

The realized part is simple arithmetic on a published number. The Bank of Guyana reports the fund's since-inception annualized return in every quarterly: 1.594% to December 2023, 2.613% to December 2025, 2.687% to June 2026 (NRF Quarterly Reports, Table 2). Against roughly 4% annualized US CPI inflation across the 6.3 years from the fund's first deposit on March 11, 2020 to June 30, 2026, that is a real return of approximately −1.3% a year. This requires no model and no view about Guyana's domestic returns.

The prospective part is where the thirty-year figure comes from, and it needs more care than an earlier version of this paper gave it. At 2026Q2 the fund held US$4,294.24M in audited total net assets against an approved 2026 ceiling of US$2,374.33M: **1.81 years of withdrawals**, at the top of the one-to-two-year range a stabilization rationale can defend. But the realized series runs the other way from what a compounding story would predict. The ratio of closing balance to that year's ceiling was 2.35 in 2022, 2.12 in 2023, 2.05 in 2024 and 1.39 in 2025; the fund retained just 1.9% of its 2025 deposits. The NRF entered the stabilization band *from above* and has been falling through it, because the amended schedule releases 94–99% of prior-year deposits and the fund keeps only the residual.

What turns that around is not gradual accumulation but a discontinuity in the schedule itself. Above US$5B of prior-year deposits the marginal release rate drops from 50% to 10%, so retention per marginal dollar jumps from 50 cents to 90 cents (§2.1, §5.4). Calibrated on realized 2026 per-lift economics against the operator's published production path, deposits cross US$5B in 2028 at US$75/bbl — 2027 at US$90, 2030 at US$60 (§8.9). The failure, precisely stated, is not that Guyana holds cash in 2026, which a buffer argument can defend. It is that the fund is approaching a statutory kink that will convert it from a pass-through into an accumulator, and the mandate governing what it accumulates into has been reviewed and left unchanged four times.

§2 sets out the institutions; §3 the literature, as the unsettled disagreement it is; §4 the model; §5 the results, including the cash-return sweep, a declining-rate scenario and a costing of the 2024 amendment; §6 the case against the original thesis in full; §7 why the allocation result survives it; §8 what we do not know.

---

## 2. Institutional background

### 2.1 The Natural Resource Fund Act 2021 and the 2024 amendment

The NRF Act 2021 set a withdrawal ceiling as a declining fraction of prior-year petroleum deposits: 100% of the first US$500M, 75% of the next US$500M, 50% of the third, 25% of the fourth, 5% of the fifth, and 3% of anything above US$2.5B (NRF Act 2021, First Schedule). The Fiscal Enactments (Amendment) Act 2024 replaced this with 100% of the first US$1B, 95% of the second, 90% of the third, 85% of the fourth, 50% of the fifth, and 10% above US$5B (Fiscal Enactments (Amendment) Act 2024).

On 2025 deposits of US$2,509.71M (Bank of Guyana, NRF Quarterly Report, December 2025, §6.1), the original schedule would have permitted about US$1,275M in 2026; the approved 2026 ceiling is US$2,374.33M — a factor of 1.86. The amendment did not adjust a parameter; it roughly doubled early-year withdrawal capacity. Any argument that the rule is "too front-loaded" must confront the fact that the legislature considered the original rule and loosened it: the withdrawal rule is endogenous to politics, and the amendment is direct evidence that a tighter rule was not politically stable. §5.4 costs it.

**Which schedule bound which year can be established from primary sources alone.** Applying each schedule to the prior year's published deposits and comparing against the approved ceiling:

| Ceiling year | Prior-year deposits | Original 2021 | Amended 2024 | Approved | Binding schedule |
|---|---|---|---|---|---|
| 2023 | US$1,411.95M | US$1,080.97M (+7.9%) | US$1,391.35M (+38.8%) | US$1,002.13M | original |
| 2024 | US$1,608.22M | US$1,152.06M (−27.3%) | US$1,577.81M (−0.5%) | US$1,586.00M | amended |
| 2025 | US$2,567.97M | US$1,277.04M (−48.2%) | US$2,461.17M (−0.1%) | US$2,463.88M | amended |
| 2026 | US$2,509.71M | US$1,275.29M (−46.3%) | US$2,408.74M (+1.4%) | US$2,374.33M | amended |

The amended schedule reproduces the approved ceiling to within 1.5% from 2024 onward and the original schedule misses by 27–48%; for 2023 the ordering reverses. The residual on the amended years is small and consistent with a statutory base that excludes interest income and the signature bonus from "deposits." This matters beyond bookkeeping: it means the schedule is a reliable forward-projection instrument, which §5.4 and §8.9 rely on.

**The schedule's shape matters more than its level.** Release and retention as a function of prior-year deposits, under the amended schedule:

| Prior-year deposits | Ceiling | Retained | Marginal release rate |
|---|---|---|---|
| US$3,000M | US$2,850M | 5.0% | 90% |
| US$4,000M | US$3,700M | 7.5% | 85% |
| US$5,000M | US$4,200M | 16.0% | **50%** |
| US$6,000M | US$4,300M | 28.3% | **10%** |
| US$8,000M | US$4,500M | 43.8% | 10% |

Below US$5B the fund is close to a pass-through. Above it, the ceiling is nearly flat in deposits and the fund becomes an accumulator. The transition is a kink, not a ramp, and §8.9 dates it.

### 2.2 Ceiling utilization

The government has drawn the ceiling, or very nearly, every year:

The government has drawn the ceiling, or very nearly, every year. Actual withdrawals here are summed from the transaction-level record in Table 7 of the quarterly reports, which lists every transfer to the Consolidated Fund by date since 2022 — so "actual" is actual, not the approved figure standing in for it:

| Year | Withdrawal (actual) | Approved ceiling | Utilization | Tranches |
|---|---|---|---|---|
| 2022 | US$607.65M | US$607.65M | **100.00%** | 3 |
| 2023 | US$1,002.13M | US$1,002.13M | **100.00%** | 8 |
| 2024 | US$1,586.00M | US$1,586.00M | **100.00%** | 5 |
| 2025 | US$2,463.00M | US$2,463.88M | **99.96%** | 9 |
| 2026 (H1) | US$1,020.00M | US$2,374.33M | 42.96% | 5 |

*Source: Bank of Guyana, NRF Quarterly Reports, Table 7 (withdrawals by date) and footnotes to §6.2 (approved amounts). 2026 is through June 30.*

Cumulative withdrawals were US$5,658.78M to end-2025 and US$6,678.78M to end-June 2026. Cumulative inflows since inception reached US$10,518.19M by 2026Q2 (Jun-2026 Quarterly, Table 6). 2025 inflows of US$2,509.71M were 2.27% below 2024's US$2,567.97M despite higher production, on lower prices; the 2026 ceiling is the first year-on-year decline because the ceiling is a function of prior-year deposits.

A note on basis, because published figures for 2026 disagree. The Bank of Guyana reports inflows on an accrual basis; press accounts generally report cash received. First-quarter 2026 inflows were US$577.60M on the accrual basis and US$761.70M on the cash basis, and the difference is exactly the US$184.11M of December 2025 lifts received on January 6 and 23, 2026. We use accrual throughout, to match the audited statements.

Because utilization is at or near 100% every year, the policy-relevant ρ is the return on the *marginal* accelerated tranche — the last dollar withdrawn — not the average return on the capital programme (§6).

### 2.3 The investment mandate

The mandate places the entire fund in an overnight deposit at the Federal Reserve Bank of New York at the prevailing federal funds rate. It has not been changed since it was set, and it has been reviewed and left in place repeatedly:

| Date | Board action | Fed funds target |
|---|---|---|
| June 26, 2023 | Mandate approved | 5.30% |
| May 16, 2024 | Reaffirmed | 5.25–5.50% |
| November 28, 2025 | "conferred its approval to continue with the existing investment mandate" | 3.50–3.75% |
| March 27, 2026 | "conferred its approval to continue with the existing investment mandate" | 3.50–3.75% |

*Source: Bank of Guyana, NRF Quarterly Reports, §5 (Investment Mandate), December 2023, December 2025 and June 2026.*

This is worth stating carefully, because the obvious criticism — that the arrangement has no mechanism for revisiting the allocation — is not true, and the truth is worse for the status quo. Every quarterly report records that the Bank of Guyana "will continue to monitor the overnight interest rate and related market developments, and inform the Chairman of any key changes to consider the feasibility of redeploying cash." A discretionary review clause exists. It has been exercised at least four times. It has produced *stay in cash* every time, including twice after the Federal Reserve had cut 175 basis points from the rate that was the mandate's original justification.

The return has followed the rate down. Year-to-date annualized returns were 4.824% in 2023, 5.095% in 2024, 4.270% in 2025 and 3.574% through June 2026 (Table 2 of the respective quarterlies). The often-quoted 4.378% is the *third-quarter* 2025 year-to-date figure, not the 2025 full-year figure, which was 4.270%. Either number is what a defender of the status quo reaches for; §7.2 explains why neither does the work asked of it.

The description of the allocation as cash rests on six audited quarterly Assets tables spanning 2023Q3 to 2026Q2, not on a single observation, together with the securities footnote reproduced in §1. §8.9 describes the dataset and what remains unverified.

---

## 3. Literature: a live disagreement

Two traditions disagree about what a capital-scarce oil exporter should do with a windfall, and the disagreement reduces to one inequality: is the domestic social return on public investment, ρ, above or below the return on a diversified foreign portfolio, r?

**Permanent income and bird-in-hand.** The permanent-income prescription, applied to resource revenue by Barnett and Ossowski (IMF Working Paper 02/177, 2002) and embodied in Norway's *handlingsregelen*, treats the resource as a stock of wealth and spends only its expected real return. Norway's fiscal rule targeted 4% of fund value from 2001 and was lowered to 3% in 2017 following the Mork Commission's expected-return work (Norwegian Ministry of Finance, 2017). The bird-in-hand variant (Bjerkholt, 2002) goes further and spends only the return on assets already accumulated, treating oil in the ground as too uncertain to consume against. The logic is intertemporal smoothing plus insurance against the absorptive-capacity and Dutch-disease failures of the resource-curse literature (van Wijnbergen, *Economic Journal*, 1984).

**Capital-scarce domestic investment.** Collier, van der Ploeg, Spence and Venables (*IMF Staff Papers* 57(1), 2010) and van der Ploeg and Venables (*Economic Journal* 121(551), 2011) argue that this prescription is wrong for capital-scarce developing economies. Where the marginal product of domestic capital exceeds the world return, a country that parks its windfall in foreign assets is lending at r what it could invest at ρ > r; the permanent-income rule "is not optimal for capital-scarce developing economies," and such countries should accumulate public and private capital to accelerate development. The empirical foundation is the high marginal product of public capital in low-income settings; Chari, Henry and Picardo's 55% median social return to EMDE roads (NBER WP 34501, 2025) is the most recent and direct estimate.

**The efficiency wedge.** The reply from the first tradition is not that ρ is low in principle but that realized ρ is low in practice. Pritchett (World Bank Policy Research Working Paper 1660, 1996) argues that in a typical developing country less than fifty cents of capital is created per public dollar invested. The IMF's public-investment-efficiency work puts the average efficiency gap at about 40% for low-income developing countries, 27% for emerging markets and 13% for advanced economies (IMF, 134-country study), with the upper bound "as high as 53 percent" (IMF WP/24/232, 2024) and above 60% in a few cases (IMF How To Note 2025/001). Presbitero (*Journal of Development Economics* 120, 2016) documents that scaling up public investment too fast lowers the growth payoff. Berg, Buffie, Pattillo, Portillo, Presbitero and Zanna (*Economica*, 2019) note, however, that a low efficiency score does not by itself imply a low return: a project that yields 55% gross and 40% net of waste is still an excellent project.

**Where this leaves ρ.** Both traditions agree the answer depends on ρ; neither provides a Guyana-specific estimate, and none exists. The IMF conducted a Public Investment Management Assessment for Guyana — it appears among fifteen emerging markets with completed PIMAs in the *PIMA Review and Update* (May 2018) — but Guyana did not consent to publication, so no institutional scores are public (§8). We therefore treat ρ as a range — roughly 3–10% real, with average returns on core infrastructure toward the top and the marginal return on the last accelerated tranche toward the bottom — and present the disagreement as unsettled because it is.

---

## 4. Model

### 4.1 Design

The model is a paired Monte Carlo over 10,000 thirty-year paths (2026–2055) of real oil prices, production and financial returns, all in real 2026 US dollars. Two withdrawal rules and two allocations run on *identical* shock paths (common random numbers), so differences are policy effects, not sampling noise; the cash sweep and declining-rate scenario reuse the same draws.

Prices follow a mean-reverting log process (Schwartz, *Journal of Finance*, 1997) around a long-run real US$65/bbl from US$70, reversion speed 0.35 (half-life about two years), 27% annual volatility. Production follows operator guidance toward 1.6 million barrels per day by 2031, haircut 10% for megaproject base-rate risk, with 6% annual decline from 2036 and a 5% annual shock. Government take ramps from 14.5% (the 2% royalty plus half of a 25% profit-oil share while the 75% cost-recovery ceiling binds under the 2016 Stabroek PSA) to 25% by 2033 as cost pools amortize. Every parameter, with alternatives and the direction of bias each choice imparts, is documented in the companion brief and lives in the code's `CONFIG` block.

The opening balance is **US$4,294.24M** — total net assets at June 30, 2026, from the audited Assets table of the June 2026 quarterly — and prior-year deposits are US$2,509.71M (2025). An earlier version of this paper used an unaudited end-July monthly reading of US$4.35B; the audited quarter-end figure is preferred and moves no result materially. The 2026Q2 balance is treated as a January 2026 opening balance; this embeds six months of 2026 net flows, shifts levels for every policy identically, and affects no sign or ranking. Applying the amended schedule to US$2,509.71M yields a 2026 ceiling of US$2,408.74M, not the approved US$2,374.33M — the statutory base evidently excludes interest income and the signature bonus — so year one is pinned to the approved figure.

### 4.2 Policies

*Statutory rule.* Each year the government withdraws 100% of the ceiling implied by prior-year deposits under the amended 2024 schedule (or, in §5.4, the original 2021 schedule) — the observed behaviour of 2022–2025, not an assumption.

*Norway-style rule.* Each year the government withdraws 3% of the fund's value after deposits, unsmoothed — the current *handlingsregelen* anchor.

*Cash.* The retained balance earns 0.5% real with 0.5% volatility in the base case — the century-long average for Treasury bills. §5 sweeps it from 0% to 3%.

*Portfolio.* The retained balance earns 3% real expected return with 11% volatility and a 5 basis point fee, matching Norway's own current return assumption; portfolio shocks are uncorrelated with oil in the base case (0.3 in sensitivity).

No policy borrows to top up spending shortfalls; the comparison is between rules, not fiscal stances.

### 4.3 The total-wealth metric and why the 2×2 isolates allocation

Comparing fund balances alone assumes withdrawn money evaporates. The metric is terminal total national wealth,

W(ρ) = B<sub>2055</sub> + Σ<sub>t</sub> w<sub>t</sub>(1+ρ)<sup>2055−t</sup>,

the fund balance plus every withdrawal compounded at the domestic social return ρ. We report W at ρ ∈ {0, 3, 5, 8, 10, 15}% and the breakeven ρ* at which median W is equal across two policies — the only architecture that does not pre-decide the answer.

The 2×2 — {statutory, Norway} × {cash, portfolio} — is the paper's central object. Within the statutory row the two cells take identical withdrawals, because the ceiling depends only on deposits, which are common to both; within the Norway row withdrawals are 3% of a balance that diverges once returns differ, so the separation is exact for the statutory row and approximate for the Norway row. For the statutory row, the difference in W is therefore exactly B<sub>2055</sub><sup>port</sup> − B<sub>2055</sub><sup>cash</sup>, and ρ cancels. The rule effect (down a column) and the allocation effect (across a row) are thereby separated; the headline comparison, Norway-portfolio versus statutory-cash, is their sum.

---

## 5. Results

All figures are from the September 2026 run (seed 42, 10,000 paths) of the accompanying code; August 2026 values are noted where they differ, which is rarely.

### 5.1 The headline comparison and the 2×2

The breakeven at which median terminal wealth under Norway-portfolio equals statutory-cash is **ρ\* = 4.12%** (4.1179%; on the earlier unaudited opening balance, 4.1200%). Below it the Norway rule with a diversified portfolio wins; above it, front-loaded domestic investment wins by a widening margin.

| ρ | W, statutory-cash (median, US$B) | W, Norway-portfolio (median, US$B) | Gap P10 | Gap P50 | Gap P90 | P(gap > 0) |
|---|---|---|---|---|---|---|
| 0% | 162.7 | 220.2 | −10.9 | 56.6 | 174.6 | 0.85 |
| 3% | 230.3 | 251.8 | −50.8 | 20.9 | 144.9 | 0.62 |
| 5% | 302.5 | 282.0 | −95.6 | −20.4 | 108.6 | 0.40 |
| 8% | 480.1 | 350.3 | −212.5 | −128.4 | 10.2 | 0.11 |
| 10% | 672.3 | 417.6 | −344.6 | −251.3 | −103.3 | 0.03 |

The 2×2 at ρ = 5% (median terminal wealth, real 2026 US$B):

| | Cash | Portfolio | Allocation effect |
|---|---|---|---|
| **Statutory rule** | 302.5 | 328.5 | +26.1 |
| **Norway rule** | 221.3 | 282.0 | +60.7 |
| **Rule effect** | −81.1 | −46.4 | |

(Earlier runs: 302.1 / 327.7 / 220.7 / 281.0 in August; 302.5 / 328.6 / 221.4 / 282.2 on the unaudited opening balance.) At ρ = 5% — well within the range §6 supports for average core infrastructure — the rule effect is negative and large: a Norway rule costs a median US$81.1B under cash and US$46.4B under a portfolio. The allocation effect is positive in both rows. The median-of-each-arm differences in the table drift slightly with ρ because medians of different distributions do not subtract; the per-path median of the statutory allocation spread, the exact object, is **US$24.8B** and is identical at every ρ on the grid to within 5×10⁻¹⁴, as the design implies.

The structural point the decomposition isolates, which the August run did not: holding allocation fixed at cash and varying only the rule, the breakeven at which the Norway rule ties the statutory rule is **ρ = 0.50%** — the cash real return itself. The front-loading critique on its own requires ρ below the overnight rate. All the force in the headline ρ* of 4.12% comes from bundling a diversified portfolio into the counterfactual. The model itself says the withdrawal rate was never the defensible target.

### 5.2 The cash-return sweep

The base case assumes +0.5% real on cash. The fund's realized 2025 return of 4.270% annualized (December 2025 quarterly, Table 2), against US CPI inflation of roughly 3%, is about 1.4% real — nearly three times that. We sweep the cash real return from 0% to 1.5% in 0.25-point steps, with an extended tail to 3% to locate the break.

| Cash real return | Statutory: portfolio − cash (per-path median, US$B) | P10 | P90 | P(portfolio > cash) | Norway: portfolio − cash (median) | ρ* (headline) |
|---|---|---|---|---|---|---|
| 0.00% | 29.8 | −3.5 | 104.2 | 0.86 | 71.4 | 4.36% |
| 0.25% | 27.4 | −6.1 | 101.1 | 0.84 | 65.6 | 4.25% |
| 0.50% | 24.8 | −8.6 | 97.9 | 0.81 | 60.7 | 4.12% |
| 0.75% | 22.2 | −11.6 | 95.3 | 0.77 | 53.3 | 3.99% |
| 1.00% | 19.4 | −14.7 | 91.8 | 0.74 | 46.9 | 3.84% |
| 1.25% | 16.5 | −18.0 | 88.1 | 0.71 | 40.1 | 3.68% |
| 1.50% | 13.3 | −21.5 | 84.1 | 0.66 | 33.1 | 3.50% |
| 2.00% | 6.4 | −29.2 | 75.8 | 0.58 | 18.1 | 3.09% |
| 2.50% | −0.9 | −38.3 | 67.3 | 0.49 | 2.1 | 2.60% |
| 3.00% | −9.1 | −48.7 | 57.5 | 0.40 | −15.6 | 1.94% |

The spread is positive in median across the whole requested range and still at 2.0%. It crosses zero at about 2.4% real — which is, not coincidentally, the portfolio's median compound real return (3% expected, less a 5 basis point fee, less volatility drag of ½ × 0.11², is 2.37%). The median result says exactly one thing: *cash cannot beat a diversified portfolio in median unless overnight cash is assumed to earn the portfolio's own geometric return.* That is nearly a tautology once stated, which is why the claim is robust. What it does not settle is whether 3% real is a fair portfolio assumption; we adopt it because it is Norway's own current anchor, with 2% and 4% as bounds.

The per-path probabilities are the counterweight. At 0.5% the portfolio beats cash on 81% of paths; at 1.5%, 66%; at 2%, 58%. P10 is negative throughout: one path in five at base, one in three at 1.5%, ends with cash ahead, because an 11%-volatility portfolio has a real left tail. The unconditional claim is about the median and about ρ-invariance, not about every path; §7 addresses what the tail justifies.

### 5.3 The declining-rate scenario

A flat 1.4% real treats 2025's rate regime as permanent. The federal funds rate was 5.30% when the mandate was set and 4.0–4.25% by the third quarter of 2025 (Federal Reserve); the direction is down. We run cash at 1.4% real in 2026 falling linearly to 0% in 2031 and holding.

| Scenario | Average cash real return 2026–55 | Statutory-cash terminal balance (median, US$B) | Statutory: portfolio − cash (per-path median) | P(portfolio > cash) | ρ* |
|---|---|---|---|---|---|
| Flat 0.5% (base) | 0.50% | 52.6 | 26.1 | 0.81 | 4.12% |
| Flat 1.4% (2025 regime made permanent) | 1.40% | 63.5 | 14.6 | 0.68 | 3.57% |
| Declining 1.4% → 0% by 2031 | 0.14% | 47.8 | 29.6 | 0.86 | 4.36% |

Under the declining path the spread is US$29.6B, larger than base, and the portfolio wins on 86% of paths. The reason is mechanical: the balance is small in 2026–2031 when cash yields something and large after 2035 when it yields nothing, so a front-loaded rate path buys the cash arm very little. The save-and-diversify case strengthens as rates normalize; the current regime flatters cash precisely when the balance is too small for it to matter.

### 5.4 The Amendment Cost scenario

Running the statutory rule under the original 2021 schedule against the amended 2024 schedule on the same paths:

| | Cash allocation | Portfolio allocation |
|---|---|---|
| Cumulative withdrawals, 2026–30 (median, US$B): amended / original | 16.8 / 6.6 | 16.8 / 6.6 |
| Cumulative withdrawals, 2026–35: amended / original | 38.8 / 13.7 | 38.8 / 13.7 |
| Cumulative withdrawals, 2026–55: amended / original | 109.9 / 40.5 | 109.9 / 40.5 |
| Terminal balance, 2055: amended / original | 52.7 / 127.9 | 78.2 / 182.7 |
| **Forgone terminal balance (original − amended)** | **75.2** | **104.5** |
| W(amended) − W(original) at ρ = 0% | −5.6 | −33.7 |
| W(amended) − W(original) at ρ = 3% | +37.9 | +9.6 |
| W(amended) − W(original) at ρ = 5% | +84.4 | +55.2 |
| **Breakeven ρ at which amendment is wealth-neutral** | **0.50%** | **2.46%** |

In fund-balance terms the amendment's cost is large: a median US$75.2B less in the fund by 2055 under cash, US$104.5B under a portfolio. In total-wealth terms it is small or negative at any plausible ρ: under cash the amendment reduces national wealth only if ρ is below 0.5% real, under a portfolio only below 2.46%, and at ρ = 5% it *adds* a median US$84.4B under cash. The forgone compounding is cheap because there is so little of it — the thesis restated from the other direction. The amendment's cost is precisely the return the fund would have earned on the money it no longer holds, and the fund earns overnight interest.

Corollary: under the original schedule the retained balance, and the cash problem with it, would have been larger — a median US$54.7B rather than US$24.8B. The amendment shrank the cash problem by shrinking the fund.

### 5.5 Sensitivity

The one-at-a-time tornado on the headline gap at ρ = 5% ranks the drivers: ρ (swing US$307B across 0–10%), portfolio real return (US$70B across 2–4%), terminal government take (US$24B), long-run price (US$23B), Norway spend rate (US$21B), cash real return (US$18B across 0–1.5%); production haircut, decline rate, oil–equity correlation and price volatility each move it by under US$12B. The headline is a statement about ρ and r; the physical parameters scale magnitudes without moving the sign.

---

## 6. The case against, and where it wins

This section is the reason the paper is titled as it is. The original thesis was that Guyana's realized ρ sits below ρ*. The evidence assembled to test it says otherwise for the core of the programme.

### 6.1 Capital scarcity means high marginal returns

Guyana entered the oil era with among the region's worst infrastructure gaps: power at two to three times regional cost, no deep-water port, a single Demerara crossing dating to 1978. Chari, Henry and Picardo (NBER WP 34501, 2025) find a median social return to an additional kilometre of two-lane EMDE highway of 55% and a mean of 97%, against a US private return of about 7%. Apply the IMF's LIDC efficiency haircut at its mean (40%), its upper estimate (53%) or its worst documented cases (over 60%, IMF How To Note 2025/001), and 55% gross leaves roughly 22–33% net real; even Pritchett's under-fifty-cents-on-the-dollar (PRWP 1996) leaves 27%. No haircut in the literature brings a median EMDE road below 4.1%. On this evidence Collier, van der Ploeg, Spence and Venables (2010) and van der Ploeg and Venables (2011) are simply correct that a Norway rule imports a rich-country prescription into a capital-scarce problem.

### 6.2 The comparison portfolio is not risk-free at 3%

A 3% real expected return comes with 11% volatility; the sweep's P10 is negative at every cash return; Norway's fund lost about a quarter of its value in 2008. A single-export country holding its buffer in global equities takes correlated risk in a global recession, when oil and equities fall together (the 0.3 correlation sensitivity moves the median gap by only US$2.5B, but the risk is in the tail, not the median). The stabilization value of cash in a bad state is real and the model does not credit it (§8).

### 6.3 Demography, politics, and the durability of rules

Guyana's population is young and poor now. Psacharopoulos and Patrinos (*Education Economics* 26(5), 2018), from 1,120 estimates across 139 countries, find private returns to a year of schooling of about 9% and social returns above 10% at secondary and higher levels — returns to schooling attained, not to ministry outlays, and subject to the same efficiency wedge. More fundamentally, a fund that visibly hoards billions abroad while citizens lack services invites raiding; a rule followed beats a rule repealed, and the 2024 amendment shows the austere rule was not politically durable. The counterfactual assumes a Norway rule would have been *obeyed*; the history says it would have been amended.

### 6.4 Oil in the ground is the real asset

With production ramping toward 1.3 million barrels per day by end-2027 and 1.7 million barrels of oil equivalent by 2030 (ExxonMobil guidance, 2026), Guyana's wealth is overwhelmingly subsoil; converting a slice into domestic capital early is diversification away from oil, not profligacy. Absorptive capacity is also a choice variable: institutions develop under real budgets, and six regional hospitals commissioned within a year at about GY$6.6B each (press reports, 2025) show that some of the execution machinery works.

### 6.5 Where the case wins, conceded

The steelman wins the argument it makes. **The evidence does not support a claim that ρ sits below breakeven for well-selected core infrastructure, and the front-loading critique therefore fails on its own terms.** The model agrees: holding cash fixed, the rule critique requires ρ below 0.5% real, a number no reading of the infrastructure literature produces. We withdraw the claim that Guyana should save more.

### 6.6 Where the case does not reach

What the steelman does not establish is that the *marginal* accelerated dollar — the last tranche of a ceiling drawn at 100% every year — earns what the average core-infrastructure project earns. Four pieces of Guyana-specific evidence bear on the margin; each is a reason to widen the ρ band, not to move its centre below 4.1%:

*Execution.* Where cleanly measurable, execution is high: 2024 actual capital expenditure of G$646.085B against G$666.175B approved, 97% (Auditor General's Report, 2024), though Gas-to-Energy recorded no 2024 expenditure because financing closed late. The 2022 and 2023 rates could not be verified against a clean primary actual-versus-budget figure; the 2025 outturn against a record allocation of about G$737.7B is provisional. High execution shows that money moves, not that it moves well.

*Flagship outcomes.* The Gas-to-Energy EPC contract rose from US$759M to US$856.152M after a roughly US$97M Dispute Adjudication Board award for soil stabilization (Demerara Waves, May 14, 2026); end-2024 completion has slipped to partial capacity at end-2026 and full combined-cycle by mid-2027; Kaieteur News (May 28, 2026) puts the total delay cost at approximately US$884M, including about US$166M for two powerships and about US$619M in higher-cost heavy-fuel-oil imports. Two VAMED hospital contracts totalling about EUR299M are in arbitration over about EUR45.3M disputed (Demerara Waves, July 16, 2026). The new Demerara River bridge was delivered at US$260.85M with a ministerial assertion of no cost overruns (Stabroek News, October 12, 2025) — a single-source claim, about five months late, part of a corridor above US$318M. No ex-post economic rate of return has been published for any of these.

*Macro absorption.* The IMF's 2026 Article IV Concluding Statement (July 31, 2026) records real growth above 19% in 2025, a non-oil primary deficit of about one-third of non-oil GDP, inflation of 3.3% in 2025 edging up by mid-2026, a tight foreign-exchange market driven by import-heavy private investment, and an explicit warning that overheating, if not contained, would produce higher inflation and real appreciation. This is the van Wijnbergen (1984) channel: at the margin, spending into a supply-constrained economy buys imports, wages and appreciation rather than capital.

*Scale.* The argument for spending US$1B a year well is not an argument for spending US$2.4B a year well. Presbitero (2016) is the general result; Timor-Leste is the cautionary case — public spending averaging 85% of GDP over 2013–2023, growth of 1.3% a year, 42% of the population in poverty (World Bank, February 2025).

The summary: average ρ on core infrastructure is very probably above 4.1%; marginal ρ on the last tranche is unmeasured and could sit either side of it. The thresholds that would confirm a sub-breakeven margin — rising construction-sector inflation, a rising import share of public investment, a non-oil primary deficit widening beyond one-third of non-oil GDP, further flagship slippage — are not yet established. We report ρ as a range of roughly 3–10% real and not as a point.

---

## 7. Why the allocation result survives the concession

### 7.1 ρ does not touch the retained balance

The concession in §6 is about ρ; the allocation result does not depend on ρ. Under the statutory rule the two arms take identical withdrawals on every path, so W<sup>port</sup> − W<sup>cash</sup> = B<sup>port</sup><sub>2055</sub> − B<sup>cash</sup><sub>2055</sub> identically, and the US$24.8B per-path median is the same number at ρ = 0 and at ρ = 15%. A reader who believes marginal ρ is 8% and one who believes it is 2% are given the same allocation cost. The concession moves the rule effect from "unknown" to "probably favourable" and leaves the allocation effect where it was.

### 7.2 What the reported return is and is not

The defence of the mandate is the headline return: 4.270% annualized in 2025, or the 4.378% third-quarter figure more often quoted. That return is a rate regime, not a policy, and the fund's own published series now shows the regime turning. Year-to-date annualized returns ran 4.824% (2023), 5.095% (2024), 4.270% (2025), 3.574% (H1 2026), tracking the federal funds target down from 5.25–5.50% to 3.50–3.75%. Net of roughly 3% US inflation the 2025 real return was about 1.4%; the century-long real return on bills is 0–0.5%. The sweep shows the allocation spread positive at 1.4% real made permanent (US$15.2B, 68% of paths) and larger under a declining path (US$31.0B, 86%). A policy defensible only if the highest short rates since 2007 persist for thirty years is not a policy; it is a bet on the Federal Reserve, made with the retained wealth of a country whose largest asset is already a single commodity.

**And the annual figures flatter the record.** The relevant number for a sovereign wealth fund is not any single year but the return over its life, which the Bank of Guyana also publishes: since-inception annualized returns of 1.594% to December 2023, 2.613% to December 2025 and 2.687% to June 2026 (Table 2 of the respective quarterlies). The fund's first deposit was March 11, 2020. Over the 6.3 years to June 30, 2026, US consumer prices rose roughly 28% in total, about 4.0% a year — the 2021–22 inflation ran directly through the middle of the period during which the fund held cash at near-zero policy rates, and the fund's own reports note that "during the first 2 years of the establishment of the Fund, interest rates were extremely low ranging between 0% to 0.05%."

The fund's real return since inception is therefore approximately **−1.3% a year**. Guyana's sovereign wealth fund has not underperformed a diversified portfolio in some counterfactual sense; it has lost purchasing power in absolute terms, on the fund manager's own published figures, over its entire existence. Every result in §5 is a projection and can be argued with on its assumptions. This one is arithmetic on two published numbers, and it is the single most important fact in this paper.

*Caveat: the inflation adjustment is ours. It uses BLS annual CPI-U for 2020–2024 and the CPI prints quoted in the NRF quarterlies themselves for 2025–2026, prorated for a March 2020 start. A reader preferring a different deflator or a different window will get a somewhat different figure; none of the plausible choices make the real return positive.*

### 7.3 What stabilization justifies, and what it does not

The strongest argument for cash is liquidity, not return: a fund drawn on every year needs assets it can sell at par in a bad year. We accept the argument and bound it. A stabilization tranche justifies holding one to two years of withdrawals — in 2026, roughly US$2.4–4.7B — in bills. At June 30, 2026 the fund held US$4,294.24M against an approved 2026 ceiling of US$2,374.33M: **1.81 years**. **On today's balance an all-cash allocation is within the range a stabilization rationale can defend, and this paper says so.**

**The realized series cuts against a naive compounding story, and we report it because it is the first thing a careful reader will check.** If the argument were that the balance is steadily outgrowing any defensible buffer, the history would show the ratio rising. It shows the opposite:

| Year | Closing balance | Approved ceiling | Buffer (years) | Share of that year's deposits retained |
|---|---|---|---|---|
| 2022 | US$1,429.45M | US$607.65M | 2.35 | 57.0% |
| 2023 | US$2,122.38M | US$1,002.13M | 2.12 | 37.7% |
| 2024 | US$3,245.69M | US$1,586.00M | 2.05 | 38.2% |
| 2025 | US$3,434.53M | US$2,463.88M | 1.39 | 1.9% |
| 2026 (Q2) | US$4,294.24M | US$2,374.33M | 1.81 | — |

*Source: authors' dataset from Bank of Guyana quarterly reports (§8.9). The 2026 figure is mid-year, with 43% of the ceiling drawn.*

The fund entered the stabilization band from above and fell through it. In 2025 it retained 1.9% of deposits. The mechanism is §2.1: the amended schedule released 94–99% of prior-year deposits in each of 2024, 2025 and 2026, so the fund keeps only a residual, and the residual has not kept pace with a ceiling growing off a rising deposit base.

**What changes this is the kink, not accumulation.** Above US$5B of prior-year deposits the ceiling is nearly flat in deposits — the marginal release rate falls from 50% to 10%, so retention per marginal dollar rises from 50 cents to 90 cents. The fund converts from a pass-through into an accumulator at a threshold written into the statute. Calibrating per-lift revenue on the two realized 2026 quarters (US$82.51M per lift at US$65.53/bbl in Q1; US$112.29M at US$102.17/bbl in Q2 — about 1.18 million barrels-equivalent per lift including royalty) and applying the operator's published production path, deposits cross US$5B in **2028 at US$75/bbl**, 2027 at US$90 and 2030 at US$60. The June 2026 quarterly adds that Guyana's profit-oil share "is expected to increase, as the cost bank for recoverable expenses by the Stabroek block operators is likely to be recovered sooner than previously anticipated," which pulls the date earlier.

So the precise failure is neither "Guyana holds cash" nor "the balance is quietly compounding." It is that a fund two years from a statutory transition into accumulation is governed by a mandate whose review clause — *"inform the Chairman of any key changes to consider the feasibility of redeploying cash"* — has been exercised at least four times and has returned the same answer each time, most recently in March 2026, after 175 basis points of cuts to the rate that justified it. There is no balance trigger, no glide path, and no distinction between a stabilization tranche and a savings tranche. Timor-Leste's Petroleum Fund, whose spending record is the cautionary tale of §6.6, nonetheless holds roughly 20% equities against a 3% real target. The failure is not that Guyana holds cash in 2026; it is that nothing in the arrangement causes it to hold anything else in 2029.

### 7.4 What the left tail justifies

The sweep's P10 is negative at every cash return, and one path in five at base ends with cash ahead. That is the cost of the recommendation and the reason it is a two-tranche structure rather than a portfolio: a stabilization tranche of one to two years of withdrawals absorbs the bad-state draw so the savings tranche can bear thirty-year equity risk. The model does not price this option (§8), so we do not quantify it; a hybrid rule dominates both corners of the 2×2 on any coherent view, and an explicit hybrid run is straightforward within the existing code.

---

## 8. Limitations and data gaps

Each of these caps the precision of a claim above; we list them as findings, not caveats.

1. **No published PIMA.** The IMF's *PIMA Review and Update* (May 2018) lists Guyana among fifteen emerging markets with a completed assessment; Guyana did not consent to publication, so no de jure or de facto institutional scores are available. This is a data gap, not an absence of assessment, and the single document most likely to move the marginal-ρ estimate.

2. **No ex-post economic rate of return on any flagship.** Gas-to-Energy, the Demerara bridge and the hospitals have cost data of varying quality and no realized-return evaluation. Guyana's efficiency wedge is borrowed from LIDC and EM cross-country means (§3); the 97% 2024 execution rate suggests it could be smaller, the flagship delays that it could be larger.

3. **Unverified 2022–2023 execution rates; provisional 2025.** Only 2024 rests on a clean audited actual-versus-approved figure; one Bank of Guyana series for 2025 is lower than the Ministry of Finance figure.

4. **Unresolved cost-recovery audit.** US$214.4M of 1999–2017 costs flagged by IHS Markit (Guyana's share about US$107M) remain in dispute and headed to a sole-expert or ICC process; the IMF's 2026 statement urged timely resolution. This affects the government-take path, which the tornado ranks third among drivers.

5. **Oil–equity correlation.** Zero in the base case; 0.3 moves the median gap by only US$2.5B, but the relevant risk is in the joint tail, which a median sensitivity does not capture.

6. **Stabilization option value.** The model gives cash no value for avoiding pro-cyclical austerity in a revenue bust. This is why §7 bounds the recommendation to a two-tranche structure rather than reporting the full US$24.8B as recoverable.

7. **Timing of the opening balance.** The June 30, 2026 audited balance is used as a January 2026 opening balance (§4.1). Levels in §5 should not be read as precise to the first decimal; rankings and signs are unaffected.

8. **Single-source figures.** The Demerara bridge's "no cost overruns" (Stabroek News, October 12, 2025) and the US$884M Gas-to-Energy delay cost (Kaieteur News, May 28, 2026) rest on single sources and are contested absent audited project accounts.

9. **The dataset, and what it still does not cover.** See §8.9 below.

### 8.9 The dataset

The empirical claims in §2, §7.2 and §7.3 rest on a dataset compiled for this paper from Bank of Guyana NRF quarterly reports, published alongside it.

**Sources.** Reports are served at `bankofguyana.org.gy/bog3/images/accounts_budgeting/natural_resource_fund/quarterly/nrf-{month}{year}-quarterly.pdf`. Each December report carries Table 1 (all four quarters of that year plus since-inception), Table 6 (every inflow by date and by FPSO since March 11, 2020) and Table 7 (every transfer to the Consolidated Fund by date since 2022), so the full history reconstructs from roughly eight documents. All figures are from the audited financial summaries, which the reports state are audited by the Bank of Guyana's Internal Audit Department and which carry the Chief Accountant's and Governor's signatures.

**Contents.** Twenty-six quarters, 2020Q1–2026Q2: market value in G$ and US$, inflows, withdrawals, interest income, asset composition where the Assets table is published, and the reported portfolio return, each row carrying the report it came from. Separately, all thirty withdrawals by date, 2022-05-10 to 2026-06-29, with running cumulative.

**Validation.** The accounting identity *balance*<sub>t</sub> = *balance*<sub>t−1</sub> + *inflows* − *withdrawals* + *interest* closes to under G$1M in all eleven quarters where Table 1 supplies flows; the residual is consistent with rounding in the published market-value chart. Separately, the statutory schedules reproduce the approved ceilings as set out in §2.1, which is an independent check on both the deposit series and our reading of the law.

**What it establishes that was previously assumed.** That withdrawals were 100.00% of the ceiling in 2022, 2023 and 2024 and 99.96% in 2025, from transaction-level records rather than from approved figures standing in for actuals. That the fair-value line item reads zero in all six published Assets tables spanning 2023Q3–2026Q2, not merely in the one 2025 statement an earlier draft relied on. That the accrual and cash bases for 2026 inflows differ by exactly the December 2025 receivables (§2.2).

**What it does not cover.** Monthly statements are not parsed; the series is quarterly. The Assets table is not reproduced in every quarterly, so asset composition is observed six times rather than twenty-six. The 2020–2022 quarters are taken from the market-value chart of the December 2023 report, which rounds to the nearest G$ million, and flows for those quarters are reconstructed from the transaction tables rather than read from a Table 1. The parser in `nrf_ingest.py` has been corrected against the verified labels but carries a known hazard documented in the file: these are multi-column tables, and a naive first-match extraction returns the wrong column. The hand-built series was validated by the balance identity precisely because of it. Extending to monthly frequency, and to the Ministry of Finance series where it differs from the Bank of Guyana's by timing, remains outstanding.

10. **Out of scope.** Gas-to-Energy revenue, carbon-credit (LEAP/ART-TREES) revenue and non-oil fiscal dynamics change Guyana's wealth; they do not change the fund-policy comparison.

---

## Conclusion

Guyana is often criticized for spending its oil money too fast. The evidence here does not sustain that criticism for the core of the programme, and this paper withdraws it. What it sustains is narrower, sharper, and — because it does not depend on how well the country spends — harder to dismiss.

The money Guyana keeps earns overnight interest. Over the fund's entire life that has meant a real return of about −1.3% a year, on the Bank of Guyana's own published since-inception figure against US inflation over the same period. That is not a projection and not a counterfactual; it is what has already happened to the money the country decided to save. The thirty-year model puts a forward number on continuing it — a median US$24.8B at base, US$13–30B across every defensible cash-return path, and zero only if overnight cash is assumed to earn what a diversified portfolio earns — but the model is the smaller half of the argument.

What makes it urgent rather than merely true is timing. The fund has spent four years shrinking relative to its own withdrawals, which is why an all-cash allocation has been defensible so far. That ends at a threshold written into the statute: above US$5B of prior-year deposits the release rate collapses to 10% and the fund becomes an accumulator, on the base case in 2028. The mandate governing what it accumulates into has been reviewed four times and left unchanged, most recently in March 2026.

The 2024 amendment made the fund smaller and the cash problem with it — the sense in which the rule and the allocation are one policy, and the sense in which the front-loading debate and this one are not really separate. But they come apart in the only way that matters for a decision: the case for spending depends on how well Guyana spends, and the case against holding the remainder in cash does not. A country that has decided to spend most of its windfall has less reason, not more, to hold what is left in a form that cannot compound.

---

### Selected references

Barnett, S. and R. Ossowski (2002). "Operational Aspects of Fiscal Policy in Oil-Producing Countries." IMF Working Paper 02/177.
Berg, A., E. Buffie, C. Pattillo, R. Portillo, A. Presbitero and L.-F. Zanna (2019). "Some Misconceptions about Public Investment Efficiency and Growth." *Economica* 86(342).
Bjerkholt, O. (2002). "Fiscal Rule Suggestions for Economies with Non-Renewable Resources." Norwegian Ministry of Finance / Univ. of Oslo.
Chari, A., P. B. Henry and S. Picardo (2025). "The Social Return to Infrastructure in Emerging and Developing Economies." NBER Working Paper 34501.
Collier, P., F. van der Ploeg, M. Spence and A. J. Venables (2010). "Managing Resource Revenues in Developing Economies." *IMF Staff Papers* 57(1).
IMF (2018). *Public Investment Management Assessment: Review and Update.*
IMF (2024). Working Paper 24/232, on public investment efficiency in LIDCs.
IMF (2025). How To Note 2025/001, on public investment efficiency.
IMF (2026). *Guyana: 2026 Article IV Consultation — Concluding Statement*, July 31, 2026.
Presbitero, A. F. (2016). "Too Much and Too Fast? Public Investment Scaling-Up and Absorptive Capacity." *Journal of Development Economics* 120.
Pritchett, L. (1996). "Mind Your P's and Q's: The Cost of Public Investment Is Not the Value of Public Capital." World Bank Policy Research Working Paper 1660.
Psacharopoulos, G. and H. A. Patrinos (2018). "Returns to Investment in Education: A Decennial Review of the Global Literature." *Education Economics* 26(5).
Schwartz, E. S. (1997). "The Stochastic Behavior of Commodity Prices." *Journal of Finance* 52(3).
van der Ploeg, F. and A. J. Venables (2011). "Harnessing Windfall Revenues: Optimal Policies for Resource-Rich Developing Economies." *Economic Journal* 121(551).
van Wijnbergen, S. (1984). "The 'Dutch Disease': A Disease After All?" *Economic Journal* 94(373).
World Bank (2025). *Timor-Leste: Transforming Public Spending to High Growth*, February 2025.
Primary sources: NRF Act 2021; Fiscal Enactments (Amendment) Act 2024; Bank of Guyana NRF Monthly Statements and Quarterly Reports (2022–2026); NRF Annual Reports (2023–2025); Auditor General of Guyana, Report on the Public Accounts 2024; Budget 2026.
