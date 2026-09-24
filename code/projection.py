"""
When do NRF deposits cross the US$5B threshold where the amended schedule's
marginal release rate collapses to 10%?

Built from realised per-lift economics in the 2026 quarterlies rather than from
an assumed take path, so the price and production assumptions are explicit.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def amended2024(dep):
    tr = [(1000, 1.00), (1000, 0.95), (1000, 0.90), (1000, 0.85), (1000, 0.50)]
    out, rem = 0.0, dep
    for size, rate in tr:
        take = min(rem, size)
        out += take * rate
        rem -= take
        if rem <= 0:
            return out
    return out + rem * 0.10


# --- Calibrate per-lift value from realised 2026 quarters -------------------
# Jun-2026 report: Q1 7 lifts / US$577.60M / avg realised US$65.53;
#                  Q2 11 lifts / US$1,235.23M / avg realised US$102.17.
# (lift counts: cumulative 99 at end-2025, 117 at end-2026Q2)
Q1 = dict(lifts=7,  inflow=577.60,  price=65.53)
Q2 = dict(lifts=11, inflow=1235.23, price=102.17)
for q, lbl in ((Q1, "Q1"), (Q2, "Q2")):
    q["per_lift"] = q["inflow"] / q["lifts"]
    q["mbbl_equiv"] = q["per_lift"] / q["price"]
    print(f"  {lbl} 2026: {q['lifts']:>2} lifts, US${q['per_lift']:>6.2f}M/lift "
          f"at US${q['price']:>6.2f}/bbl -> {q['mbbl_equiv']:.3f} Mbbl-equivalent per lift")

MBBL_PER_LIFT = np.mean([Q1["mbbl_equiv"], Q2["mbbl_equiv"]])
print(f"\n  Calibrated: {MBBL_PER_LIFT:.3f} Mbbl-equivalent per lift "
      f"(includes Guyana's royalty share)\n")

# --- Lift schedule from production ------------------------------------------
# Jun-2026 report: ~900k bpd now; Uaru (+250k) latter half of 2026;
# Whiptail (+250k) end-2027; Hammerhead (+150k) 2029; ~1.7M bpd by 2030.
PROD_KBPD = {2026: 960, 2027: 1150, 2028: 1400, 2029: 1500, 2030: 1700}
LIFTS_2026 = 40  # scheduled per the 2026 budget, per the Jun-2026 report

SCENARIOS = {"low US$60": 60.0, "base US$75": 75.0, "high US$90": 90.0}

rows = []
for name, price in SCENARIOS.items():
    for yr, kbpd in PROD_KBPD.items():
        lifts = LIFTS_2026 * kbpd / PROD_KBPD[2026]
        if yr == 2026:   # H1 realised + H2 projected
            dep = 1812.83 + (LIFTS_2026 - 18) * MBBL_PER_LIFT * price
        else:
            dep = lifts * MBBL_PER_LIFT * price
        ceil = amended2024(dep)
        rows.append({"scenario": name, "year": yr, "price": price,
                     "deposits_usd_m": round(dep, 1),
                     "ceiling_usd_m": round(ceil, 1),
                     "retained_usd_m": round(dep - ceil, 1),
                     "retained_pct": round(100 * (dep - ceil) / dep, 1),
                     "crosses_5b": dep >= 5000})
df = pd.DataFrame(rows)
pd.set_option("display.width", 220)
print("=== DEPOSIT PROJECTION AND RETENTION ===")
for name in SCENARIOS:
    print(f"\n  {name}/bbl")
    print(df[df.scenario == name][
        ["year", "deposits_usd_m", "ceiling_usd_m", "retained_usd_m",
         "retained_pct", "crosses_5b"]].to_string(index=False))

print("\n=== FIRST YEAR DEPOSITS CROSS US$5B ===")
for name in SCENARIOS:
    sub = df[(df.scenario == name) & df.crosses_5b]
    print(f"  {name:<12} -> {sub.year.iloc[0] if len(sub) else 'not by 2030'}")

df.to_csv("nrf_deposit_projection.csv", index=False)

# --- Chart: realised buffer ratio and retention rate -------------------------
hist_years = [2022, 2023, 2024, 2025]
buffer = [2.35, 2.12, 2.05, 1.39]
retention = [57.0, 37.7, 38.2, 1.9]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.6))

ax1.plot(hist_years, buffer, "o-", lw=2.2, color="#B4413C", ms=7)
ax1.axhspan(1, 2, color="#2E8B8B", alpha=0.13)
ax1.text(2022.05, 1.93, "stabilisation range a buffer argument defends",
         fontsize=8.5, color="#1F6F6F", va="top")
ax1.set_title("Realised buffer: closing balance ÷ that year's ceiling", fontsize=10.5)
ax1.set_ylabel("years of withdrawals")
ax1.set_xticks(hist_years)
ax1.set_ylim(0, 2.8)
ax1.grid(alpha=0.25)

ax2.bar([str(y) for y in hist_years], retention, color="#2E5F8B", width=0.6)
ax2.set_title("Share of each year's deposits retained in the fund", fontsize=10.5)
ax2.set_ylabel("% of deposits")
ax2.grid(alpha=0.25, axis="y")
for i, v in enumerate(retention):
    ax2.text(i, v + 1.6, f"{v}%", ha="center", fontsize=9)
ax2.set_ylim(0, 65)

fig.suptitle("The NRF has not been compounding: the buffer ratio fell 2022–2025",
             fontsize=12, y=1.005)
fig.tight_layout()
fig.savefig("buffer_and_retention.png", dpi=150, bbox_inches="tight")
print("\nWrote nrf_deposit_projection.csv and buffer_and_retention.png")
