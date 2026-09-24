"""
Does the NRF balance actually compound past a stabilisation buffer?

The paper's section 7.3 argues the all-cash allocation is defensible on today's
balance (~1.8 years of withdrawals) but that the balance compounds past any
defensible buffer, with the mandate having no trigger. This script tests that
premise against the realised history.
"""
import pandas as pd

# Annual inflows, US$M. Stated verbatim in the BoG quarterlies' section 6.1.
#   2022, 2023: Dec-2023 report.  2024, 2025: Dec-2025 report.  2026: Jun-2026 (H1).
INFLOWS = {
    2022: 1256.79 + 155.16,            # profit oil + royalties
    2023: 1390.13 + 218.09,
    2024: 2219.94 + 348.03,
    2025: 2164.04 + 330.67 + 15.00,    # + signature bonus
    2026: 577.60 + 1235.23,            # H1 only (Q1 + Q2)
}
WITHDRAWALS = {2022: 607.65, 2023: 1002.13, 2024: 1586.00, 2025: 2463.00, 2026: 1020.00}
CEILING     = {2022: 607.65, 2023: 1002.13, 2024: 1586.00, 2025: 2463.88, 2026: 2374.33}
CLOSING     = {2022: 1429.45, 2023: 2122.38, 2024: 3245.69, 2025: 3434.53, 2026: 4294.24}

rows = []
for y in sorted(INFLOWS):
    infl, wd = INFLOWS[y], WITHDRAWALS[y]
    rows.append({
        "year": y,
        "inflows_usd_m": round(infl, 2),
        "withdrawals_usd_m": round(wd, 2),
        "retained_usd_m": round(infl - wd, 2),
        "retention_pct_of_inflows": round(100 * (infl - wd) / infl, 1),
        "closing_balance_usd_m": CLOSING[y],
        "buffer_years": round(CLOSING[y] / CEILING[y], 2),
        "note": "H1 only" if y == 2026 else "",
    })
df = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print("=== RETENTION AND BUFFER ===")
print(df.to_string(index=False))

print("\n=== THE MECHANISM ===")
print("The amended 2024 schedule releases 100/95/90/85% of successive US$1B tranches")
print("of PRIOR-YEAR deposits. The ceiling therefore tracks deposits with a one-year")
print("lag at a rate near 90% in the relevant range. Check the realised pass-through:")
for y in [2023, 2024, 2025, 2026]:
    prior = INFLOWS[y - 1]
    print(f"  {y} ceiling US${CEILING[y]:>7.2f}M / {y-1} deposits US${prior:>7.2f}M "
          f"= {100*CEILING[y]/prior:>5.1f}%")

print("\n=== WHAT THIS MEANS FOR THE BUFFER ===")
full = df[df.note == ""]
print(f"  Buffer years, 2022 -> 2025: {' -> '.join(str(v) for v in full.buffer_years)}")
print(f"  Direction: {'FALLING' if full.buffer_years.iloc[-1] < full.buffer_years.iloc[0] else 'RISING'}")
print("  2026 H1 reads 1.81 because only 43% of the ceiling has been drawn so far;")
print("  the comparable end-year figure depends on H2 draws.")
print("\n  Projection at the realised pass-through: if the ceiling stays near 90-95% of")
print("  prior-year deposits, the fund retains only the residual plus interest, so the")
print("  balance grows roughly in proportion to deposits -- and so does the ceiling.")
print("  The RATIO is therefore near-stationary, not compounding, unless either")
print("  (a) deposits outrun the lagged ceiling during a steep ramp, or")
print("  (b) deposits exceed US$5B, where the top tier releases only 10%.")

print("\n=== WHEN DOES (b) BITE? ===")
print("  Deposits cross US$5B when production and price push annual NRF receipts there.")
print("  2026 H1 receipts were US$1,812.83M; Q2 alone was US$1,235.23M at an average")
print("  realised price of US$102.17/bbl (Jun-2026 report, section 2.1).")
print("  Annualising Q2: US$4,940.92M -- essentially AT the US$5B threshold already.")
q2_annualised = 1235.23 * 4
print(f"  Q2-2026 annualised: US${q2_annualised:,.2f}M")
print("  Above US$5B the marginal release rate drops from 85% to 10%, so the retained")
print("  share jumps discontinuously. THAT is the compounding trigger -- a kink in the")
print("  schedule, not smooth accumulation.")
