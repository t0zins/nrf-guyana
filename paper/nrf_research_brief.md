# Guyana NRF: Status Quo vs. Norway-Style Rule — Research Brief
*Prepared August 2026. Companion to `nrf_ingest.py` and `nrf_simulation.py`.*

---

## 0. Verified facts and corrections (as of Aug 2026)

| Item | Value | Status |
|---|---|---|
| NRF balance, end-May 2026 | ~US$3.96B (peaked $4.1B end-April) | Verified (Bank of Guyana via press) |
| Cumulative inflows since 2020 | ~US$9.3B | Verified |
| Cumulative transfers to Consolidated Fund | >US$6B | Verified |
| 2025 deposits | US$2.47B | Verified |
| 2026 approved withdrawal | US$2.374B (first YoY decline) | Verified |
| Withdrawal rule (current) | Fiscal Enactments (Amendment) Act 2024: 100%/95%/90%/85%/50% per US$1B tranche of prior-year deposits; 10% above US$5B | Verified |
| Withdrawal rule (original) | NRF Act 2021: 100%/75%/50%/25%/5% per US$500M tranche; 3% above US$2.5B | Verified |
| Asset allocation | Cash at Federal Reserve Bank of New York; no reported equity/bond portfolio | Supported; verify "financial assets at fair value ≈ 0" line item directly from monthly PDFs via ingestion script |
| Production, Feb 2026 | ~918k bpd (2025 avg: 716k) | Verified |
| Ramp | Uaru (+250k) Q4 2026 → ~1.2M capacity; Whiptail (+250k) 2027 → 1.3M by end-2027; Hammerhead (+150k) 2029; Exxon target 1.7M by 2030 | Verified (operator guidance — treat as upside case, not base) |
| Stabroek fiscal terms | 2% royalty; 75% cost-recovery ceiling; 50/50 profit-oil split → ~14.5% effective take while cost recovery binds | Widely reported; effective take path is a modeling judgment (see A7) |

**Key structural fact your original framing missed:** the 2024 amendment roughly *doubled* early-year withdrawal capacity. Any "the rule is too front-loaded" argument must engage with the fact that the legislature chose to loosen it — the rule is endogenous to politics. Run both schedules.

---

## 1. ASSUMPTIONS MENU

Format per assumption: **Options → strongest published justification → direction of bias on your headline result (the gap favoring the Norway-style counterfactual) → recommendation (confidence)**.

### A1. Oil price process
- **(a) Mean-reverting (Ornstein–Uhlenbeck / Schwartz one-factor) around a long-run real price.** Justification: Schwartz (1997), Pindyck (1999) — commodity prices show reversion to marginal cost over multi-year horizons; standard in petroleum fiscal modeling (IMF FARI framework).
- **(b) Geometric Brownian motion, zero real drift.** Justification: Hotelling-adjacent; random-walk hypothesis hard to reject in short samples (Hamilton 2009); avoids the fragile long-run-mean parameter.
- **(c) Regime-switching (normal vs. shock regimes).** Justification: fits history best (2008, 2014, 2020, 2022); but adds parameters you can't defend at HS-competition level.
- **Bias:** Mean reversion *shrinks* revenue tails both ways → narrows the distribution of the gap, barely moves its median. GBM fattens upside tails → slightly bigger absolute gaps in dollar terms.
- **Recommendation:** (a) as base, long-run real price US$60–70/bbl (note Brent ~mid-$70s spot 2026; EIA/IMF long-run reference cases cluster $60–80), κ ≈ 0.3–0.4 (half-life ~2 yrs), σ ≈ 25–30% annualized. Run (b) as robustness. **Confidence: medium.** Nobody can defend a point estimate here; that's why you show distributions.

### A2. Price volatility
- Options: σ = 20% / 27% / 35%. Justification: realized annualized vol of Brent log returns is ~30% over 2000–2025 including crisis years, ~20–25% excluding them; long-dated implied vols sit low-to-mid 20s.
- **Bias:** higher σ widens both policies' outcome distributions; it *raises* the value of the stabilization argument for the status quo (buffer against bad states) — so low σ quietly flatters your thesis. Don't pick low.
- **Recommendation:** 27% base, sweep 20–35. **Confidence: medium-high.**

### A3. Production ramp, plateau, decline
- **(a) Operator guidance:** 1.3M by end-2027, 1.7M by 2030, plateau into the 2030s. Justification: Exxon has beaten every prior Guyana timeline; all four FPSOs run above nameplate.
- **(b) Haircut path:** guidance × 0.85–0.9 with 1-year slippage on new FPSOs. Justification: base-rate literature on megaproject delay (Flyvbjerg); FPSO ramp risk; possible OPEC+/price-driven deferral of Longtail FID.
- **(c) Decline:** post-plateau decline 5–8%/yr starting ~2035–2038, tail sustained only if further FIDs (Longtail, project 9+) materialize.
- **Bias:** higher production → larger deposits → larger *absolute* gap between policies (more money to mismanage or compound). Production assumptions scale the answer's magnitude but rarely flip its sign.
- **Recommendation:** base = (b) haircut; upside = (a); decline 6%/yr from 2036. **Confidence: medium.** State explicitly that Exxon guidance is a *ceiling case* from an interested party.

### A4. Government take (share of gross revenue reaching the NRF)
You didn't list this. **It is the single most consequential physical-to-fiscal link in the model.**
- Mechanics: 2% royalty + 50% of profit oil, where profit oil = gross − cost recovery (capped at 75% of gross). While the cost-recovery ceiling binds: take ≈ 2% + 50%×25% = **14.5%**. As historical costs amortize, take drifts up — but each new US$12.7B project injects new recoverable costs, so the drift is slow.
- Options: (i) flat 14.5% for the whole horizon (conservative); (ii) ramp 14.5% → 25% over 2026–2033 (cost pools amortize); (iii) ramp to 30%+ by mid-2030s (optimistic, assumes no new mega-FIDs late).
- **Bias:** higher take scales deposits ~linearly → scales the gap.
- **Recommendation:** (ii) base, sweep (i)/(iii). **Confidence: low-medium** — the cost-recovery trajectory is genuinely opaque (there is an ongoing audit dispute over historical costs); flag it as a data gap.

### A5. Counterfactual portfolio real return
- **(a) 3% real.** Justification: Norway lowered its handlingsregelen anchor from 4% to 3% in 2017 based on Mork Commission expected-return work; GPFG realized ~3.5–4% real net since 1998.
- **(b) 4% real.** Justification: long-run global 60/40 real returns (Dimson–Marsh–Staunton ~4%+ for equities-heavy mixes); Guyana's horizon is long enough to bear equity risk.
- **(c) 2% real.** Justification: current high CAPE / low expected-return regime arguments (AQR, Vanguard capital-market assumptions cluster 2–3.5% real for balanced portfolios).
- **Bias:** THIS DIRECTLY SCALES YOUR RESULT. Every 1pp of assumed real return over 30 years on a multi-billion base is billions of dollars. If you pick 4% you will be accused of assuming your conclusion.
- **Recommendation:** **3% base (matching Norway's own current anchor — rhetorically bulletproof), 2% pessimistic, 4% optimistic. Portfolio vol 10–12%.** **Confidence: medium-high** on the range, low on any point.

### A6. Cash (status quo) real return
- Options: 0% real / +0.5% real / +1% real. Justification: T-bill real returns average ≈ 0–0.5% over the last century; the NRF earned healthy *nominal* interest in the 2023–25 rate environment but that's a regime, not a policy.
- **Bias:** higher cash return shrinks the gap. Using 2024's ~5% nominal as if permanent would be the classic error in your *opponents'* favor — pre-empt it.
- **Recommendation:** +0.5% real base, sweep 0–1%. **Confidence: high.** This is the best-anchored parameter in the model.

### A7. Discount rate (for NPV comparisons)
- Options: (i) don't discount — report terminal real wealth (cleanest, most honest for a wealth question); (ii) 3% social discount rate (matches portfolio return, standard); (iii) higher SDR (6%+) reflecting Guyana's capital scarcity — but note this smuggles in the development-needs argument through the back door.
- **Bias:** high discount rates favor front-loading mechanically.
- **Recommendation:** primary metric = **terminal real wealth distribution, undiscounted** (you're asking "how rich is Guyana in 2050"), with a 3% NPV variant in an appendix. **Confidence: high** that this framing is the defensible one.

### A8. Time horizon
- 20 vs. 30 years. Longer horizons compound the return gap and also stretch beyond credible production forecasts.
- **Recommendation:** 30-year headline (2026–2055), 20-year robustness. **Confidence: high.**

### A9. Treatment of Guyana's development needs (the crux)
- **(a) Ignore it (compare fund balances only).** Indefensible — it assumes withdrawn money evaporates. A referee kills this in one sentence.
- **(b) Total-wealth accounting:** national wealth = fund + Σ withdrawals compounded at a domestic social return ρ. Then report the **breakeven ρ\*** at which the policies tie. Justification: this is the actual economics — Collier, van der Ploeg, Spence & Venables (2010, "Managing Resource Revenues in Developing Economies") argue capital-scarce countries *should* invest domestically because marginal returns exceed world portfolio returns; the empirical counter is Pritchett (1996) and IMF PIMA-style evidence that a dollar of public "investment" often creates far less than a dollar of capital (efficiency losses of 30–40% common in low-capacity settings; Presbitero 2016 on absorptive capacity).
- **(c) Explicit two-sector growth model.** Overkill; you can't calibrate it credibly.
- **Bias:** (b) with ρ sweeps is the only version that doesn't pre-decide the answer.
- **Recommendation:** **(b), with ρ ∈ {0, 3, 5, 8, 10, 15%} and breakeven ρ\* reported per scenario.** Your empirical contribution is then arguing where Guyana's *realized* ρ sits, using budget execution rates, cost overruns (e.g., major infrastructure projects), inflation/Dutch-disease pressure, and audit findings. **Confidence: high that this is the right architecture.**

### A10. Withdrawal behavior under the status quo
- Options: government withdraws (i) 100% of the statutory ceiling every year (matches 2022–2026 behavior almost exactly); (ii) 90%; (iii) ceiling under the *original 2021 schedule* (counterfactual "the amendment never happened").
- **Bias:** (i) maximizes front-loading, maximizing your measured gap — but it is also simply what has happened.
- **Recommendation:** (i) base, (iii) as a named scenario ("Amendment Cost") — quantifying the 2024 amendment's cost in forgone compounding is a headline-worthy sub-result nobody else has published. **Confidence: high.**

### A11. Norway-rule implementation detail
- Spend 3% of fund value each year (smoothed vs. unsmoothed; Norway smooths over cycles). Unsmoothed is fine at annual resolution. Also decide whether the counterfactual government *tops up* spending shortfall vs. status quo from other borrowing — you should assume NOT (pure rule comparison) and say so, because otherwise you need a debt model.

### A12. Everything in real 2026 US$
State once, apply everywhere. Avoids separately modeling US inflation and G$/US$ (NRF flows are all USD anyway).

---

## 2. Model architecture (why it's built this way)

- Identical price/production paths feed both policies (common random numbers) → the *difference* distribution is tight and paired, which is the statistically correct way to compare policies.
- Metrics reported per path: fund balance trajectory; cumulative withdrawals; terminal total wealth W(ρ) for each ρ; ΔW = Norway − status quo; breakeven ρ\* (root of median ΔW(ρ) = 0).
- Expect ρ\* to land in the mid-single digits when portfolio return is 3% real: mechanically it must sit near the portfolio return, adjusted for the withdrawal-timing asymmetry and the schedule's shape. **If your empirical section can show Guyana's effective ρ is plausibly below ρ\* (execution inefficiency, overheating), your thesis survives. If not, it doesn't. Commit to that test in advance — that's what makes this research rather than advocacy.**

---

## 3. THE STRONGEST COUNTERARGUMENT (steelman)

**Claim: front-loaded spending is correct for Guyana.**

1. **Capital scarcity means high marginal returns.** Guyana pre-oil had among the region's worst infrastructure gaps: no deep-water port, unreliable power at ~2–3× regional cost, one bridge over the Demerara dating to 1978. The gas-to-energy project alone is projected to halve electricity costs — cheap power raises the return on *all* private capital. Collier–van der Ploeg–Spence–Venables explicitly conclude that the permanent-income/Norway rule is wrong for capital-scarce developing countries; the optimal path front-loads domestic investment. Your counterfactual imports a rich-country rule into a poor-country problem.
2. **The comparison portfolio is not risk-free at 3%.** A 3% real expected return comes with ~11% vol and deep-drawdown risk; Norway's fund fell ~25% in 2008. A small country with one income source holding its buffer in equities takes correlated risk (oil down + equities down in global recessions).
3. **Demography and politics.** Guyana's population is young and poor *now*; a dollar of health/education for a child today has compounding human-capital returns (Psacharopoulos–Patrinos estimate returns to schooling ~9–10%/yr) that plausibly exceed any portfolio. And a fund that visibly hoards billions abroad while citizens lack services invites raiding or political rupture — the *durability* of a savings rule is itself an asset; a modest rule actually followed beats an austere rule repealed. (The 2024 amendment is evidence the austere rule was not politically stable.)
4. **Oil in the ground is the real asset.** Total petroleum wealth is the resource, not the fund. With production still ramping, Guyana's total wealth is overwhelmingly subsoil; converting a slice to domestic capital early is diversification *away* from oil, not profligacy.
5. **Absorption is a choice variable.** Yes, spending too fast wastes money — but capacity is built by doing. PIM efficiency improves with institutions that only develop under real budgets.

**Honest assessment of whether your analysis survives:**

It survives **only in reframed form.** The steelman wins the argument "some front-loading > pure Norway rule" — the literature genuinely supports that for capital-scarce countries, and you should concede it in print. What the steelman does *not* establish is that Guyana's *actual realized* domestic return clears the breakeven: (i) execution — budget under-execution and cost overruns are documented in Auditor General reports; (ii) macro absorption — double-digit non-oil growth with construction bottlenecks and imported inputs means marginal dollars increasingly buy inflation and imports, not capital (classic Dutch-disease channel, van Wijnbergen 1984); (iii) scale — the argument for spending $1B/yr well is not an argument for spending $2.4B/yr well; marginal ρ declines steeply with volume; (iv) zero diversification — even conceding high-ρ domestic investment, holding the *residual* balance in cash rather than a diversified portfolio is dominated under any coherent view: the fund's stabilization tranche argument justifies T-bills for maybe 1–2 years of withdrawals, not 100% of assets. **Your strongest defensible thesis: not "Guyana should spend less" but (1) the marginal withdrawn dollar likely earns below breakeven at current volumes, and (2) the cash-only allocation of the retained balance is indefensible under every assumption — even the steelman's.** Point (2) is unconditionally true in your model and is where you should plant your flag.

---

## 4. PAPER SKELETON

1. **Introduction.** Claim: Guyana faces a quantifiable trade-off between front-loaded withdrawal + cash holding and a save-and-diversify rule; this paper quantifies it and identifies the breakeven domestic return that decides it. Evidence needed: verified NRF facts table (§0).
2. **Institutional background.** Claim: the NRF's rule was materially loosened in 2024 and its assets are held as cash. Evidence: NRF Act 2021 First Schedule vs. Fiscal Enactments (Amendment) Act 2024; monthly report line items (from your ingestion pipeline — this is your original dataset).
3. **Literature.** Claim: two live traditions disagree — permanent-income/bird-in-hand (Norway; Friedman PIH applied via Barnett–Ossowski IMF work) vs. invest-domestically-when-capital-scarce (Collier et al. 2010; van der Ploeg–Venables 2011); the disagreement reduces to ρ vs. r. Evidence: cite both sides *as a disagreement*, not a settled matter.
4. **Data.** Claim: a clean monthly time series of NRF balance/inflows/withdrawals/interest can be constructed from official PDFs. Evidence: your parsed dataset + flag log (report parse failure rate — transparency is a feature).
5. **Model.** Claim: paired Monte Carlo over price/production with two policy simulators isolates the policy effect. Evidence: equations, config table (= §1 menu choices), convergence check.
6. **Results.** Claims: (a) distribution of terminal wealth gap under base case; (b) breakeven ρ\* ≈ [computed]; (c) the "Amendment Cost" scenario; (d) cash-vs-portfolio effect isolated from withdrawal-rule effect (run the 2×2: {statutory, Norway rule} × {cash, portfolio} — this decomposition is the paper's best table). Evidence: fan charts, gap distributions, 2×2 decomposition.
7. **Sensitivity.** Claim: results are driven by portfolio return, ρ, and take; robust to price-process choice. Evidence: tornado chart; explicit statement of what flips the sign.
8. **The case against, and where it wins.** Claim: steelman §3 verbatim-in-spirit; concede the front-loading argument's validity range; show the cash-allocation result survives it unconditionally.
9. **Policy discussion.** Claim: feasible middle paths (stabilization tranche in bills + savings tranche diversified; withdrawal smoothing) dominate both corners. Evidence: one additional simulator run of a hybrid rule.
10. **Limitations.** = §5 gaps, honestly.

---

## 5. GAPS / what a knowledgeable critic attacks first

1. **Effective government take path (A4).** Cost-recovery balance and audit disputes are not fully public. A critic hits your deposit projections here first. Mitigation: sweep widely; anchor 2026–27 to actual reported deposits.
2. **"Cash-only" precision.** Confirm from the monthly PDFs whether small non-cash holdings exist and how "interest income" is booked. Don't overstate to "literally zero."
3. **Realized domestic ρ.** You will not find a clean published estimate of Guyana's marginal return on public investment. You'll be triangulating from execution rates, PIMA-style benchmarks, and project outcomes. A critic will call this soft — it is. Present it as bounding, not estimation.
4. **Endogeneity of the rule.** The counterfactual assumes a Norway rule would have been *followed*. The 2024 amendment is direct evidence against political stability of tight rules. Address head-on (this is steelman pt. 3).
5. **Stabilization value of cash.** Your model gives cash no option value against revenue busts. A fuller model would credit the status quo with avoided pro-cyclical austerity in bad states. Flag it; optionally proxy it by reporting P10 outcomes, where the gap narrows.
6. **Oil-equity correlation.** If portfolio returns correlate with oil (global demand shocks), diversification benefit shrinks. Sensitivity: correlate portfolio shocks with price shocks at 0 / +0.3.
7. **Data existence:** monthly PDFs before ~2022 may be sparse/formatted differently; Bank of Guyana and Ministry of Finance figures occasionally differ by timing (accrual vs. receipt). Log every discrepancy rather than reconciling silently.
8. **You are not modeling gas-to-energy, carbon-credit (LEAP/ART-TREES) revenue, or non-oil fiscal dynamics.** Say so; they don't change the fund-policy comparison but they change "Guyana's wealth."
