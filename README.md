# Guyana's Natural Resource Fund: a verified dataset and a policy model

A machine-readable quarterly dataset for Guyana's Natural Resource Fund (NRF),
compiled from the Bank of Guyana's published quarterly reports, together with a
paired Monte Carlo model of the fund's withdrawal-rule and asset-allocation
choices and a working paper built on both.

**Headline result.** The Bank of Guyana reports the fund's since-inception
annualized return as 2.687% (to June 2026). Against roughly 4% annualized US
inflation over the same 6.3 years, that is a real return of about **−1.3% a
year**. The fund has lost purchasing power over its entire life. The model puts
a forward figure on continuing the all-cash allocation — a median US$24.8B in
real 2026 terms over 2026–2055 — but the realized number needs no model.

---

## What's here

```
data/       the dataset (CSV)
code/       dataset builder, analysis scripts, Monte Carlo simulation, PDF ingest
paper/      the working paper and the methodological brief behind it
figures/    charts
outputs/    simulation results
```

### `data/`

| file | rows | contents |
|---|---|---|
| `nrf_quarterly_verified.csv` | 26 | 2020Q1–2026Q2: market value (G$ and US$), inflows, withdrawals, interest income, asset composition, reported portfolio return, source report per row |
| `nrf_withdrawals_by_date.csv` | 30 | every transfer to the Consolidated Fund, 2022-05-10 to 2026-06-29, with running cumulative |
| `nrf_annual_verified.csv` | 7 | annual roll-up: **actual** withdrawals against **approved** ceilings, utilization, buffer ratio |
| `nrf_deposit_projection.csv` | 15 | deposit and retention projection under three oil-price scenarios |

Every row names the report it came from. Figures are transcribed from the
audited financial summaries, which the reports state are audited by the Bank of
Guyana's Internal Audit Department and which carry the Chief Accountant's and
Governor's signatures.

## Sources

All data is from Bank of Guyana NRF quarterly reports:

```
https://bankofguyana.org.gy/bog3/images/accounts_budgeting/
    natural_resource_fund/quarterly/nrf-{month}{year}-quarterly.pdf
```

e.g. `nrf-december2023-quarterly.pdf`, `nrf-june2026-quarterly.pdf`. Note the
path segment is `bog3`; `bog` redirects.

Three reports supply the whole series, because each December report carries:

- **Table 1** — all four quarters of that year plus a since-inception column
- **Table 6** — every inflow by date and by FPSO since 11 March 2020
- **Table 7** — every withdrawal by date since 2022
- **Tables 3/4/5** — capital account, assets, income for the reporting quarter

The reports used here are December 2023, December 2025 and June 2026.

## Validation

Two independent checks, both reproducible from this repo:

**1. The accounting identity.** `balance_t = balance_{t-1} + inflows −
withdrawals + interest` closes to **under G$1M in all 11 quarters** where Table 1
supplies flows. The residual is consistent with the published market-value chart
rounding to the nearest G$ million.

```
python code/build_dataset.py
```

**2. The statutory schedules reproduce the approved ceilings.** Applying the
Fiscal Enactments (Amendment) Act 2024 schedule to published prior-year deposits
reproduces the approved ceiling to within 1.5% for 2024, 2025 and 2026; the
original NRF Act 2021 schedule misses those years by 27–48% but is the closer
fit for 2023. This independently dates the amendment's effect and confirms the
deposit series.

```
python code/schedule_check.py
```

## Reproducing everything

```bash
pip install -r requirements.txt

python code/build_dataset.py      # dataset + identity check
python code/schedule_check.py     # schedule validation + retention curve
python code/buffer_analysis.py    # buffer ratio and retention history
python code/projection.py         # deposit projection + figure
python code/nrf_simulation.py     # Monte Carlo (10,000 paths, ~2 min)
```

The simulation is seeded (`seed: 42`) and reproduces exactly.

## The model

`code/nrf_simulation.py` compares two policies on identical price and production
paths (common random numbers), scoring **total national wealth = terminal fund
balance + all withdrawals compounded at a domestic social return ρ**:

- **Statutory rule + cash** — the status quo: draw the full ceiling, hold the
  remainder as overnight deposits
- **Norway-style rule + diversified portfolio** — spend 3% of fund value, hold
  the remainder at a 3% real expected return

Scoring total wealth rather than fund balance alone matters: withdrawn money
isn't destroyed, it buys roads and schools. The model solves for the breakeven ρ
at which the policies tie.

**Key results** (10,000 paths, 30-year horizon, 2026–2055, real 2026 US$):

| | |
|---|---|
| Breakeven ρ\* | **4.12%** |
| 2×2 at ρ = 5% | statutory+cash 302.5 · statutory+port 328.5 · norway+cash 221.3 · norway+port 282.0 (US$B) |
| Allocation spread (per-path median) | **US$24.8B**, identical at every ρ to within 5×10⁻¹⁴ |
| Sweep crossing | 2.45% cash real return |

The allocation spread is **exactly invariant to ρ** because both statutory arms
take bit-identical withdrawals on every path, so ρ multiplies terms that cancel.
That is the paper's central claim: the cost of holding the retained balance in
cash does not depend on any view about how productively Guyana spends what it
withdraws.

## The paper

`paper/the_cash_problem.md` — *The Cash Problem: Asset Allocation, Not
Withdrawal Rates, Is Guyana's Defensible Sovereign Wealth Failure*.

The paper argues the allocation, not the withdrawal rate, is the defensible
failure — and concedes the withdrawal-rate argument explicitly. An earlier
version of this project set out to show Guyana withdraws too fast. The evidence
assembled to test that claim did not support it: gross social returns to core
infrastructure in capital-scarce economies are high enough that, even after
documented public-investment efficiency losses, a well-selected project plausibly
clears the 4.12% breakeven. Section 6 makes that case in full and does not soften
it.

`paper/nrf_research_brief.md` is the methodological brief: an assumptions menu
with the justification and direction of bias for each modelling choice.

## Limitations

Stated at length in §8 of the paper. In short: the series is quarterly, not
monthly; the Assets table appears in six of the twenty-six quarters, so asset
composition is observed six times; 2020–2022 market values come from a chart
rounded to the nearest G$ million; the PDF parser in `code/nrf_ingest.py` carries
a documented multi-column extraction hazard and the dataset here was hand-built
and validated by the identity check rather than produced by it. The inflation
adjustment behind the −1.3% real return is the author's, using BLS CPI-U and the
CPI prints quoted in the NRF quarterlies.

## Citation

If you use the dataset, please cite the repository. Underlying figures are the
Bank of Guyana's; errors in transcription, derivation and interpretation are
mine.

## License

Code: MIT. Data and text: CC BY 4.0. Underlying source documents are the
Bank of Guyana's and are not covered by this license.
