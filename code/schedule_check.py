"""
Validate the statutory withdrawal schedules against realised ceilings, then
locate the deposit level at which the fund begins to retain materially.
"""

def amended2024(dep_musd):
    """Fiscal Enactments (Amendment) Act 2024: 100/95/90/85/50% per US$1B
    tranche of prior-year deposits, 10% above US$5B."""
    tranches = [(1000, 1.00), (1000, 0.95), (1000, 0.90), (1000, 0.85), (1000, 0.50)]
    out, rem = 0.0, dep_musd
    for size, rate in tranches:
        take = min(rem, size)
        out += take * rate
        rem -= take
        if rem <= 0:
            return out
    return out + rem * 0.10


def original2021(dep_musd):
    """NRF Act 2021 First Schedule: 100/75/50/25/5% per US$500M tranche,
    3% above US$2.5B."""
    tranches = [(500, 1.00), (500, 0.75), (500, 0.50), (500, 0.25), (500, 0.05)]
    out, rem = 0.0, dep_musd
    for size, rate in tranches:
        take = min(rem, size)
        out += take * rate
        rem -= take
        if rem <= 0:
            return out
    return out + rem * 0.03


DEPOSITS = {2022: 1411.95, 2023: 1608.22, 2024: 2567.97, 2025: 2509.71}
ACTUAL_CEILING = {2023: 1002.13, 2024: 1586.00, 2025: 2463.88, 2026: 2374.33}

print("=== DOES THE STATUTORY FORMULA REPRODUCE THE APPROVED CEILING? ===")
print("  (ceiling year Y is computed on deposits of year Y-1)\n")
for y in [2023, 2024, 2025, 2026]:
    dep = DEPOSITS[y - 1]
    act = ACTUAL_CEILING[y]
    am, og = amended2024(dep), original2021(dep)
    law = "original 2021" if y == 2023 else "amended 2024"
    pred = og if y == 2023 else am
    err = 100 * (pred - act) / act
    print(f"  {y}: deposits(Y-1)=US${dep:>8.2f}M  law={law}")
    print(f"        predicted US${pred:>8.2f}M vs approved US${act:>8.2f}M  "
          f"error {err:>+6.2f}%")
    print(f"        [other schedule would give US${(am if y==2023 else og):>8.2f}M]")

print("\n=== RELEASE AND RETENTION RATE BY DEPOSIT LEVEL (amended 2024) ===")
print(f"  {'deposits':>10} {'ceiling':>10} {'released':>10} {'retained':>10}  {'marginal':>9}")
prev_d = prev_c = None
for d in [1000, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 12000]:
    c = amended2024(d)
    marg = "" if prev_d is None else f"{100*(c-prev_c)/(d-prev_d):>8.1f}%"
    print(f"  US${d:>7,.0f}M US${c:>7,.0f}M {100*c/d:>9.1f}% {100*(d-c)/d:>9.1f}%  {marg:>9}")
    prev_d, prev_c = d, c

print("\n=== THE KINK ===")
for d in [4800, 4900, 5000, 5100, 5200, 5500]:
    c = amended2024(d)
    print(f"  deposits US${d:,}M -> retained US${d-c:>7,.1f}M ({100*(d-c)/d:>4.1f}% of deposits)")
print("\n  Below US$5B the marginal release rate is 50-100%. Above it, 10%.")
print("  Retention per extra dollar of deposits jumps from 50c to 90c at the threshold.")
