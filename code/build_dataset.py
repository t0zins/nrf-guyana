"""
Build the verified NRF dataset from Bank of Guyana quarterly reports.

Sources (fetched directly from bankofguyana.org.gy/bog3/images/accounts_budgeting/
natural_resource_fund/quarterly/nrf-{month}{year}-quarterly.pdf):
  - nrf-december2023-quarterly.pdf  Tables 1,2,3,4,5,6; Graph 6 (market value 2020Q1-2023Q4)
  - nrf-december2025-quarterly.pdf  Tables 1,2,3,4,5,6,7
  - nrf-june2026-quarterly.pdf      Tables 1,2,3,4,5,6,7

All figures transcribed verbatim from the audited financial summaries.
FX is GYD 208.50 = USD 1, stated identically in all three reports.
"""
import pandas as pd

FX = 208.50

# --------------------------------------------------------------------------
# 1. Quarterly market value, G$ millions. Graph 6 of Dec-2023 (2020Q1-2023Q4)
#    extended by Dec-2025 and Jun-2026.
# --------------------------------------------------------------------------
MARKET_VALUE_GM = {
    "2020Q1": 11454, "2020Q2": 19792, "2020Q3": 30163, "2020Q4": 41349,
    "2021Q1": 55809, "2021Q2": 71758, "2021Q3": 90934, "2021Q4": 126694,
    "2022Q1": 150081, "2022Q2": 157054, "2022Q3": 219178, "2022Q4": 298041,
    "2023Q1": 305363, "2023Q2": 359341, "2023Q3": 391431, "2023Q4": 442516,
    "2024Q1": 491512, "2024Q2": 598514, "2024Q3": 665825, "2024Q4": 676726,
    "2025Q1": 696260, "2025Q2": 665564, "2025Q3": 749395, "2025Q4": 716099,
    "2026Q1": 759667, "2026Q2": 895349,
}

# --------------------------------------------------------------------------
# 2. Withdrawals, transaction level. Table 7 of the Jun-2026 report (complete
#    since inception).
# --------------------------------------------------------------------------
WITHDRAWALS = [
    ("2022-05-10", 200_000_000.00), ("2022-07-12", 200_000_000.00),
    ("2022-12-09", 207_646_570.00),
    ("2023-02-06", 200_000_000.00), ("2023-05-04", 200_000_000.00),
    ("2023-08-03", 100_000_000.00), ("2023-09-06", 100_000_000.00),
    ("2023-09-26",  50_000_000.00), ("2023-10-24", 100_000_000.00),
    ("2023-11-24", 100_000_000.00), ("2023-12-28", 152_130_249.00),
    ("2024-03-06", 250_000_000.00), ("2024-05-15", 300_000_000.00),
    ("2024-07-22", 300_000_000.00), ("2024-10-01", 300_000_000.00),
    ("2024-12-16", 436_000_000.00),
    ("2025-02-10", 400_000_000.00), ("2025-04-09", 400_000_000.00),
    ("2025-06-04", 200_000_000.00), ("2025-06-25", 200_000_000.00),
    ("2025-09-24", 200_000_000.00), ("2025-10-31", 200_000_000.00),
    ("2025-11-20", 200_000_000.00), ("2025-12-10", 200_000_000.00),
    ("2025-12-29", 463_000_000.00),
    ("2026-03-11", 400_000_000.00), ("2026-05-04", 100_000_000.00),
    ("2026-05-13", 200_000_000.00), ("2026-05-20", 200_000_000.00),
    ("2026-06-29", 120_000_000.00),
]

# --------------------------------------------------------------------------
# 3. Statutory ceilings approved by the National Assembly, US$ millions.
#    2025 and 2026 are footnoted verbatim in the BoG quarterlies; 2023 is
#    stated as "100% of the estimated amount" in the Dec-2023 report.
# --------------------------------------------------------------------------
CEILINGS_USD_M = {
    2022: 607.65,
    2023: 1002.13,
    2024: 1586.00,
    2025: 2463.88,   # Dec-2025 report, footnote 3
    2026: 2374.33,   # Jun-2026 report, footnote 1
}

# --------------------------------------------------------------------------
# 4. Table 1 "Changes in Market Value", G$'000.
# --------------------------------------------------------------------------
TABLE1_GK = {  # quarter -> (inflows, withdrawals, interest_income)
    "2023Q1": (45_756_167,  -41_700_000,  3_266_127),
    "2023Q2": (91_521_053,  -41_700_000,  4_156_487),
    "2023Q3": (79_169_635,  -52_125_000,  5_045_658),
    "2023Q4": (118_867_088, -73_419_157,  5_636_983),
    "2024Q4": (156_599_360, -153_456_000, 7_756_897),
    "2025Q1": (95_822_401,  -83_400_000,  7_112_071),
    "2025Q2": (128_843_669, -166_800_000, 7_260_398),
    "2025Q3": (117_705_010, -41_700_000,  7_825_906),
    "2025Q4": (180_904_245, -221_635_500, 7_435_430),
    "2026Q1": (120_430_148, -83_400_000,  6_537_704),
    "2026Q2": (257_545_266, -129_270_000, 7_406_671),
}

# --------------------------------------------------------------------------
# 5. Table 4 "Assets", G$'000. Every observation available in the three
#    reports. The third field is the line item carrying the paper's claim.
# --------------------------------------------------------------------------
ASSETS_GK = {  # quarter -> (cash_and_equivalents, other_receivables, fin_assets_fv)
    "2023Q3": (391_431_221,          0, 0),
    "2023Q4": (411_469_069, 31_047_066, 0),
    "2025Q3": (749_395_024,          0, 0),
    "2025Q4": (677_711_491, 38_387_708, 0),
    "2026Q1": (759_667_051,          0, 0),
    "2026Q2": (895_348_988,          0, 0),
}

# --------------------------------------------------------------------------
# 6. Table 2 "Fund Portfolio" reported returns, %.
# --------------------------------------------------------------------------
RETURNS = {
    "2023Q1": 1.059, "2023Q2": 1.159, "2023Q3": 1.253, "2023Q4": 1.269,
    "2024Q1": 1.255, "2024Q2": 1.238, "2024Q3": 1.318, "2024Q4": 1.190,
    "2025Q1": 1.069, "2025Q2": 1.080, "2025Q3": 1.082, "2025Q4": 0.972,
    "2026Q1": 0.877, "2026Q2": 0.886,
}
YTD_ANNUALISED = {2023: 4.824, 2024: 5.095, 2025: 4.270, 2026: 3.574}  # 2026 = H1

SRC = {
    "2020": "BoG NRF Quarterly Dec-2023, Graph 6",
    "2021": "BoG NRF Quarterly Dec-2023, Graph 6",
    "2022": "BoG NRF Quarterly Dec-2023, Graph 6",
    "2023": "BoG NRF Quarterly Dec-2023, Tables 1-6",
    "2024": "BoG NRF Quarterly Dec-2025, Table 1 / Graph 6",
    "2025": "BoG NRF Quarterly Dec-2025, Tables 1-7",
    "2026": "BoG NRF Quarterly Jun-2026, Tables 1-7",
}


def quarter_of(datestr):
    y, m = int(datestr[:4]), int(datestr[5:7])
    return f"{y}Q{(m - 1) // 3 + 1}"


# --- withdrawals -----------------------------------------------------------
wd = pd.DataFrame(WITHDRAWALS, columns=["date", "amount_usd"])
wd["quarter"] = wd["date"].map(quarter_of)
wd["year"] = wd["date"].str[:4].astype(int)
wd["cumulative_usd"] = wd["amount_usd"].cumsum()
wd["source_report"] = "BoG NRF Quarterly Jun-2026, Table 7"
wd_q = wd.groupby("quarter")["amount_usd"].sum().div(1e6)
wd_y = wd.groupby("year")["amount_usd"].sum().div(1e6)

# --- quarterly panel -------------------------------------------------------
rows = []
for q, mv_gm in MARKET_VALUE_GM.items():
    year = int(q[:4])
    t1 = TABLE1_GK.get(q)
    a = ASSETS_GK.get(q)
    rows.append({
        "quarter": q,
        "year": year,
        "market_value_gyd_m": mv_gm,
        "market_value_usd_m": round(mv_gm / FX, 2),
        "inflows_usd_m": round(t1[0] / 1e3 / FX, 2) if t1 else None,
        "withdrawals_usd_m": round(wd_q.get(q, 0.0), 2),
        "interest_income_usd_m": round(t1[2] / 1e3 / FX, 2) if t1 else None,
        "cash_and_equivalents_usd_m": round(a[0] / 1e3 / FX, 2) if a else None,
        "other_receivables_usd_m": round(a[1] / 1e3 / FX, 2) if a else None,
        "financial_assets_fair_value_usd_m": round(a[2] / 1e3 / FX, 2) if a else None,
        "portfolio_return_pct": RETURNS.get(q),
        "source_report": SRC[q[:4]],
    })
q_df = pd.DataFrame(rows)

# --- annual roll-up --------------------------------------------------------
ann = []
for year in sorted(set(q_df["year"])):
    sub = q_df[q_df["year"] == year]
    drawn = round(float(wd_y.get(year, 0.0)), 2)
    ceil = CEILINGS_USD_M.get(year)
    close = float(sub["market_value_usd_m"].iloc[-1])
    ann.append({
        "year": year,
        "closing_balance_usd_m": close,
        "withdrawals_actual_usd_m": drawn,
        "ceiling_approved_usd_m": ceil,
        "utilisation_pct": round(100 * drawn / ceil, 2) if ceil else None,
        "ytd_annualised_return_pct": YTD_ANNUALISED.get(year),
        "balance_over_ceiling_years": round(close / ceil, 2) if ceil else None,
        "note": "H1 only (through 2026Q2)" if year == 2026 else "",
    })
a_df = pd.DataFrame(ann)

q_df.to_csv("nrf_quarterly_verified.csv", index=False)
wd.to_csv("nrf_withdrawals_by_date.csv", index=False)
a_df.to_csv("nrf_annual_verified.csv", index=False)

pd.set_option("display.width", 220)
print("=== ANNUAL ===")
print(a_df.to_string(index=False))

print("\n=== CEILING UTILISATION ===")
for r in ann:
    if r["ceiling_approved_usd_m"]:
        print(f"  {r['year']}: drew US${r['withdrawals_actual_usd_m']:>8.2f}M of "
              f"US${r['ceiling_approved_usd_m']:>8.2f}M = {r['utilisation_pct']:>6.2f}%  {r['note']}")

print("\n=== ASSET COMPOSITION (every observation in the reports) ===")
ac = q_df.dropna(subset=["cash_and_equivalents_usd_m"])[
    ["quarter", "cash_and_equivalents_usd_m", "other_receivables_usd_m",
     "financial_assets_fair_value_usd_m"]]
print(ac.to_string(index=False))

print("\n=== STABILISATION BUFFER (closing balance / that year's ceiling) ===")
for r in ann:
    if r["balance_over_ceiling_years"]:
        print(f"  end-{r['year']}: {r['balance_over_ceiling_years']} years of withdrawals")

print("\n=== IDENTITY CHECK: bal_t = bal_{t-1} + inflows - withdrawals + interest ===")
qs = list(MARKET_VALUE_GM)
bad = 0
for i in range(1, len(qs)):
    q, p = qs[i], qs[i - 1]
    t1 = TABLE1_GK.get(q)
    if not t1:
        continue
    implied = MARKET_VALUE_GM[p] * 1e3 + t1[0] + t1[1] + t1[2]
    actual = MARKET_VALUE_GM[q] * 1e3
    diff_m = (implied - actual) / 1e3
    flag = "OK " if abs(diff_m) < 1.0 else "*** "
    if abs(diff_m) >= 1.0:
        bad += 1
    print(f"  {flag}{q}: implied G${implied/1e3:>10,.0f}M vs reported G${actual/1e3:>10,.0f}M "
          f"(diff G${diff_m:>7,.1f}M)")
print(f"  -> {bad} quarter(s) outside G$1M tolerance (rounding in Graph 6 is to the nearest G$M)")

print(f"\nRows written: quarterly={len(q_df)}, withdrawals={len(wd)}, annual={len(a_df)}")
