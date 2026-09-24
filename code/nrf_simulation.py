#!/usr/bin/env python3
"""
NRF policy Monte Carlo: statutory front-loaded rule + cash  vs.
Norway-style real-return spending rule + diversified portfolio.

All monetary units: REAL 2026 US$. All returns: real.
Paired design: both policies run on IDENTICAL price/production/return-shock
paths, so differences are policy effects, not noise. The cash-return sweep
and the declining-rate scenario reuse the same shock draws (same seed, same
draw order), so they are paired too.

v2 (September 2026) changes vs. the August 2026 run
--------------------------------------------------
  * initial_balance -> US$4.35B (BoG, end-July 2026);
    prior_year_deposits -> US$2,509.71M (2025 NRF inflows, NRF Annual Report 2025).
  * NEW  cash_sweep()      : cash real return 0.00% -> 1.50% in 0.25pp steps
                             (+ an extended tail to 3.0% to locate the break),
                             reporting the statutory_port - statutory_cash
                             spread, the full 2x2, and rho* at each value.
  * NEW  declining_rate()  : cash real return falls linearly from its current
                             realized level to 0% real over 2026-2031.
  * NEW  amendment_cost()  : NRF Act 2021 schedule vs. Fiscal Enactments
                             (Amendment) Act 2024 schedule, cash and portfolio.
  * Existing outputs (fanchart, tornado, historical, results_summary.csv,
    decomposition_2x2.csv) are unchanged in name and layout.

Outputs (./out):
  fanchart.png            fund balance P10/50/90, both policies
  tornado.png             one-at-a-time sensitivity of the median terminal gap
  historical.png          NRF balance vs annual withdrawals (fallback data;
                          replaced by nrf_ingest.py output when available)
  results_summary.csv     percentiles of terminal wealth, gap, breakeven rho*
  decomposition_2x2.csv   {statutory, norway} x {cash, port} at rho_headline
  cash_sweep.csv          2x2 + allocation spread + rho* per cash real return
  cash_sweep.png          allocation spread vs cash real return
  declining_rate.csv      2x2 under flat-0.5%, flat-current, declining paths
  amendment_cost.csv      original2021 vs amended2024, cash and portfolio

Run: python nrf_simulation.py
"""

from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =============================================================================
# CONFIG — every judgment call lives here. See nrf_research_brief.md §1
# for options, justifications, and bias direction per parameter.
# =============================================================================
CONFIG = {
    "n_paths": 10_000,
    "seed": 42,
    "start_year": 2026,
    "horizon_years": 30,                 # A8

    # Opening state. NOTE on timing: the model is annual and treats
    # initial_balance as the 1 Jan 2026 opening balance, but the verified
    # figure is end-July 2026 and already embeds ~7 months of 2026 inflows
    # net of withdrawals. This is the same convention as the August run
    # (which used end-May). It shifts LEVELS for every policy identically
    # (paired design) and does not affect the sign of any 2x2 spread.
    # AUDITED. Both figures now come from Bank of Guyana quarterly reports
    # rather than monthly press figures:
    #   balance  = Total Net Assets at 30 Jun 2026, G$895,348,988k / 208.50
    #              (Jun-2026 Quarterly, Table 4) = US$4,294.24M
    #   deposits = 2025 profit oil US$2,164.04M + royalties US$330.67M
    #              + signature bonus US$15.00M (Dec-2025 Quarterly, s6.1)
    # The prior US$4.35B was an unaudited end-July monthly reading.
    "initial_balance": 4.29424e9,        # 2026Q2 Total Net Assets, audited
    "prior_year_deposits": 2.50971e9,    # 2025 inflows, Dec-2025 Quarterly s6.1

    # The 2026 withdrawal ceiling is already approved (~US$2.374B). Applying
    # the amended schedule to US$2.50971B of "inflows" gives US$2.409B, i.e.
    # the statutory base appears to exclude ~US$40M of interest income. We
    # pin year-1 of the amended schedule to the approved figure rather than
    # guess at the base definition. Set to None to disable.
    "ceiling_2026_approved": 2.374e9,

    # --- Oil price (A1, A2): mean-reverting log price (Schwartz 1-factor) ---
    "price_model": "mean_reverting",     # "mean_reverting" | "gbm"
    "p0": 70.0,                          # real US$/bbl starting level
    "long_run_price": 65.0,
    "mr_speed": 0.35,                    # kappa; half-life ~2 yrs
    "price_vol": 0.27,
    "gbm_drift": 0.0,
    "price_floor": 15.0,

    # --- Production, Mbpd gross (A3): base = operator guidance x haircut ---
    "prod_guidance": {2026: 0.98, 2027: 1.15, 2028: 1.30, 2029: 1.40,
                      2030: 1.55, 2031: 1.60, 2032: 1.60, 2033: 1.60,
                      2034: 1.60, 2035: 1.60},
    "prod_haircut": 0.90,                # megaproject base-rate discount
    "decline_start": 2036,
    "decline_rate": 0.06,
    "prod_shock_vol": 0.05,              # iid multiplicative annual shock

    # --- Government take = share of gross revenue deposited (A4) ---
    "take_start": 0.145,                 # royalty 2% + 50% x 25% profit oil
    "take_end": 0.25,
    "take_ramp_end_year": 2033,

    # --- Policy A: statutory rule + cash (A6, A10) ---
    "schedule": "amended2024",           # "amended2024" | "original2021"
    "withdrawal_utilization": 1.00,      # gov't has drawn ~100% of ceiling

    # Cash real return. "flat" uses cash_real_return every year.
    # "declining" runs linearly from cash_decline_start (2026) to
    # cash_decline_end (cash_decline_end_year) and stays there.
    "cash_return_mode": "flat",          # "flat" | "declining"
    "cash_real_return": 0.005,           # base case, A6
    "cash_return_vol": 0.005,
    "cash_current_real": 0.014,          # 2025 realized: 4.378% nominal YTD
                                         # annualized (NRF Q3 2025 Quarterly
                                         # Report) less ~3% US CPI -> ~1.4% real
    "cash_decline_start": 0.014,
    "cash_decline_end": 0.000,
    "cash_decline_end_year": 2031,

    # Sweep grid for cash_sweep(). The requested grid is 0.0-1.5% in 0.25pp
    # steps; the extended tail locates where the allocation spread breaks.
    "cash_sweep": [0.0000, 0.0025, 0.0050, 0.0075, 0.0100, 0.0125, 0.0150],
    "cash_sweep_extended": [0.0200, 0.0250, 0.0300],
    # Fine grid around the sign change, so the crossing is observed rather
    # than interpolated across a 0.5pp gap. See section 5.2: the crossing sits
    # slightly ABOVE the portfolio's single-year median compound return,
    # because terminal wealth is a sum of deposits compounded over different
    # horizons and the median of a sum of lognormals exceeds the sum of medians.
    "cash_sweep_fine": [0.0220, 0.0225, 0.0230, 0.0235, 0.0240, 0.0245,
                        0.0255, 0.0260],

    # --- Policy B: Norway-style (A5, A11) ---
    "spend_rate": 0.03,                  # handlingsregelen anchor since 2017
    "port_real_return": 0.03,
    "port_vol": 0.11,
    "port_fee": 0.0005,                  # GPFG-like passive cost
    "port_oil_corr": 0.0,                # sensitivity: 0.3

    # --- Evaluation (A7, A9) ---
    "rho_grid": [0.00, 0.03, 0.05, 0.08, 0.10, 0.15],  # domestic social return
    "rho_headline": 0.05,
}

SCHEDULES = {
    # (tranche width USD, withdrawable fraction), then marginal rate above
    "amended2024": {"tiers": [(1e9, 1.00), (1e9, 0.95), (1e9, 0.90),
                              (1e9, 0.85), (1e9, 0.50)], "above": 0.10},
    "original2021": {"tiers": [(0.5e9, 1.00), (0.5e9, 0.75), (0.5e9, 0.50),
                               (0.5e9, 0.25), (0.5e9, 0.05)], "above": 0.03},
}


def withdrawal_ceiling(prior_deposits: np.ndarray, schedule: str) -> np.ndarray:
    s = SCHEDULES[schedule]
    rem = prior_deposits.astype(float).copy()
    out = np.zeros_like(rem)
    for width, frac in s["tiers"]:
        take = np.minimum(rem, width)
        out += take * frac
        rem -= take
    out += rem * s["above"]
    return out


def cash_mean_path(cfg: dict, years: np.ndarray) -> np.ndarray:
    """Per-year mean real cash return. Flat or linearly declining."""
    if cfg["cash_return_mode"] == "flat":
        return np.full(len(years), float(cfg["cash_real_return"]))
    if cfg["cash_return_mode"] == "declining":
        y0, y1 = cfg["start_year"], cfg["cash_decline_end_year"]
        r0, r1 = cfg["cash_decline_start"], cfg["cash_decline_end"]
        frac = np.clip((years - y0) / max(y1 - y0, 1), 0.0, 1.0)
        return r0 + (r1 - r0) * frac
    raise ValueError(cfg["cash_return_mode"])


# =============================================================================
# Path generation (shared across policies — common random numbers)
# =============================================================================
def gen_paths(cfg: dict):
    rng = np.random.default_rng(cfg["seed"])
    n, T = cfg["n_paths"], cfg["horizon_years"]
    years = np.arange(cfg["start_year"], cfg["start_year"] + T)

    # prices
    z_p = rng.standard_normal((n, T))
    logp = np.empty((n, T))
    lp = np.log(cfg["p0"]) * np.ones(n)
    for t in range(T):
        if cfg["price_model"] == "mean_reverting":
            lp = lp + cfg["mr_speed"] * (np.log(cfg["long_run_price"]) - lp) \
                 - 0.5 * cfg["price_vol"] ** 2 + cfg["price_vol"] * z_p[:, t]
        else:  # gbm
            lp = lp + cfg["gbm_drift"] - 0.5 * cfg["price_vol"] ** 2 \
                 + cfg["price_vol"] * z_p[:, t]
        logp[:, t] = lp
    price = np.maximum(np.exp(logp), cfg["price_floor"])

    # production (Mbpd)
    base = np.empty(T)
    last = None
    for i, y in enumerate(years):
        if y in cfg["prod_guidance"]:
            last = cfg["prod_guidance"][y] * cfg["prod_haircut"]
        elif y >= cfg["decline_start"]:
            last = last * (1 - cfg["decline_rate"])
        base[i] = last
    prod = base[None, :] * np.exp(
        cfg["prod_shock_vol"] * rng.standard_normal((n, T))
        - 0.5 * cfg["prod_shock_vol"] ** 2)

    # government take ramp
    ramp_T = cfg["take_ramp_end_year"] - cfg["start_year"]
    take = np.clip(cfg["take_start"] + (cfg["take_end"] - cfg["take_start"])
                   * np.arange(T) / max(ramp_T, 1),
                   cfg["take_start"], cfg["take_end"])

    deposits = price * prod * 1e6 * 365.0 * take[None, :]

    # return shocks (portfolio correlated with oil optionally; cash shocks)
    z_r = rng.standard_normal((n, T))
    c = cfg["port_oil_corr"]
    z_port = c * z_p + np.sqrt(1 - c ** 2) * z_r
    port_r = (cfg["port_real_return"] - cfg["port_fee"]
              - 0.5 * cfg["port_vol"] ** 2 + cfg["port_vol"] * z_port)
    port_r = np.exp(port_r) - 1.0
    # cash draws come last so that changing the cash MEAN (sweep / declining)
    # leaves every other draw untouched -> paired across cash scenarios
    z_c = rng.standard_normal((n, T))
    cash_r = cash_mean_path(cfg, years)[None, :] + cfg["cash_return_vol"] * z_c

    return years, price, prod, deposits, port_r, cash_r


# =============================================================================
# Policy simulators. Order of operations each year:
#   returns accrue on opening balance -> deposits arrive -> withdrawal taken.
# Withdrawal timing symmetric across policies by construction.
# =============================================================================
def simulate(cfg: dict, deposits, ret, mode: str, schedule: str | None = None):
    n, T = deposits.shape
    schedule = schedule or cfg["schedule"]
    bal = np.full(n, float(cfg["initial_balance"]))
    prior = np.full(n, float(cfg["prior_year_deposits"]))
    balances = np.empty((n, T))
    withdrawals = np.empty((n, T))
    for t in range(T):
        bal = bal * (1 + ret[:, t]) + deposits[:, t]
        if mode == "statutory":
            w = withdrawal_ceiling(prior, schedule)
            # year-1 pin to the approved 2026 ceiling (amended schedule only:
            # the approved figure IS the amended-schedule number)
            if (t == 0 and schedule == "amended2024"
                    and cfg.get("ceiling_2026_approved")):
                w = np.full(n, float(cfg["ceiling_2026_approved"]))
            w = w * cfg["withdrawal_utilization"]
        elif mode == "norway":
            w = cfg["spend_rate"] * bal
        else:
            raise ValueError(mode)
        w = np.minimum(w, bal)
        bal = bal - w
        balances[:, t] = bal
        withdrawals[:, t] = w
        prior = deposits[:, t]
    return balances, withdrawals


def total_wealth(balances, withdrawals, rho: float):
    """Terminal national wealth = fund + withdrawals compounded at rho."""
    n, T = withdrawals.shape
    comp = (1 + rho) ** np.arange(T - 1, -1, -1)[None, :]
    return balances[:, -1] + (withdrawals * comp).sum(axis=1)


def breakeven_rho(bal_a, wd_a, bal_b, wd_b, lo=-0.02, hi=0.20, iters=40):
    """rho* where median terminal wealth is equal. Median gap is monotonically
    decreasing in rho (A withdraws more, earlier), so bisection is valid."""
    def med_gap(rho):
        return np.median(total_wealth(bal_b, wd_b, rho) - total_wealth(bal_a, wd_a, rho))
    glo, ghi = med_gap(lo), med_gap(hi)
    if glo * ghi > 0:
        return np.nan  # no crossing in range
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if med_gap(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def run(cfg: dict):
    years, price, prod, deposits, port_r, cash_r = gen_paths(cfg)
    out = {}
    # 2x2 decomposition: rule x asset allocation
    for name, (mode, ret) in {
        "statutory_cash":  ("statutory", cash_r),
        "statutory_port":  ("statutory", port_r),
        "norway_cash":     ("norway",    cash_r),
        "norway_port":     ("norway",    port_r),
    }.items():
        out[name] = simulate(cfg, deposits, ret, mode)
    return years, deposits, out


def median_2x2(res: dict, rho: float) -> dict:
    return {k: float(np.median(total_wealth(*res[k], rho))) / 1e9 for k in res}


# =============================================================================
# NEW: cash-return sweep
# The allocation spread (statutory_port - statutory_cash) is, by construction,
# a difference in retained balances only: both arms take the same statutory
# withdrawals on the same deposit paths, so rho cancels except on paths where
# the ceiling exceeds the balance (fund depletion). We report the spread at
# every rho on the grid to show this numerically rather than assert it.
# =============================================================================
def cash_sweep(cfg: dict) -> pd.DataFrame:
    grid = sorted(set(list(cfg["cash_sweep"])
                      + list(cfg["cash_sweep_extended"])
                      + list(cfg.get("cash_sweep_fine", []))))
    rows = []
    for c in grid:
        sub = dict(cfg, cash_return_mode="flat", cash_real_return=c)
        _, _, res = run(sub)
        row = {"cash_real_return": c}
        W = median_2x2(res, cfg["rho_headline"])
        row.update({f"{k}_p50_B": v for k, v in W.items()})
        # allocation spreads (per-path median of the difference, and P>0)
        for rule in ("statutory", "norway"):
            bp, wp = res[f"{rule}_port"]
            bc, wc = res[f"{rule}_cash"]
            d = total_wealth(bp, wp, cfg["rho_headline"]) - total_wealth(bc, wc, cfg["rho_headline"])
            row[f"{rule}_port_minus_cash_medianW_B"] = W[f"{rule}_port"] - W[f"{rule}_cash"]
            row[f"{rule}_port_minus_cash_pathmedian_B"] = float(np.median(d)) / 1e9
            row[f"{rule}_port_minus_cash_p10_B"] = float(np.percentile(d, 10)) / 1e9
            row[f"{rule}_port_minus_cash_p90_B"] = float(np.percentile(d, 90)) / 1e9
            row[f"P({rule}_port>cash)"] = float((d > 0).mean())
        # rho-independence check on the statutory allocation spread.
        # Per-path difference is EXACTLY rho-invariant whenever withdrawals are
        # identical across the two arms (no depletion). Median-of-each-arm
        # differences drift slightly with rho because medians of two different
        # distributions do not subtract; both are reported.
        bp, wp = res["statutory_port"]; bc, wc = res["statutory_cash"]
        row["statutory_withdrawals_identical"] = bool(np.array_equal(wp, wc))
        for rho in cfg["rho_grid"]:
            Wr = median_2x2(res, rho)
            tag = f"rho{int(round(rho*100)):02d}"
            row[f"stat_spread_medofeach_{tag}_B"] = Wr["statutory_port"] - Wr["statutory_cash"]
            d_r = total_wealth(bp, wp, rho) - total_wealth(bc, wc, rho)
            row[f"stat_spread_pathmedian_{tag}_B"] = float(np.median(d_r)) / 1e9
        # breakeven rho for the headline comparison (norway_port vs statutory_cash)
        ba, wa = res["statutory_cash"]; bb, wb = res["norway_port"]
        row["rho_star"] = breakeven_rho(ba, wa, bb, wb)
        # breakeven rho for rule effect holding allocation fixed at cash
        bnc, wnc = res["norway_cash"]
        row["rho_star_rule_only_cash"] = breakeven_rho(ba, wa, bnc, wnc)
        rows.append(row)
    return pd.DataFrame(rows)


# =============================================================================
# NEW: declining-rate scenario
# =============================================================================
def declining_rate(cfg: dict) -> pd.DataFrame:
    variants = {
        "flat_base_0.5pct":    dict(cfg, cash_return_mode="flat",
                                    cash_real_return=cfg["cash_real_return"]),
        "flat_current_real":   dict(cfg, cash_return_mode="flat",
                                    cash_real_return=cfg["cash_current_real"]),
        "declining_to_zero":   dict(cfg, cash_return_mode="declining"),
    }
    rows = []
    for name, sub in variants.items():
        years, _, res = run(sub)
        W = median_2x2(res, cfg["rho_headline"])
        ba, wa = res["statutory_cash"]; bb, wb = res["norway_port"]
        bp, wp = res["statutory_port"]
        d = total_wealth(bp, wp, cfg["rho_headline"]) - total_wealth(ba, wa, cfg["rho_headline"])
        rows.append({
            "scenario": name,
            "cash_mean_2026": float(cash_mean_path(sub, years)[0]),
            "cash_mean_2031plus": float(cash_mean_path(sub, years)[-1]),
            "avg_cash_real_2026_2055": float(cash_mean_path(sub, years).mean()),
            **{f"{k}_p50_B": v for k, v in W.items()},
            "statutory_port_minus_cash_medianW_B": W["statutory_port"] - W["statutory_cash"],
            "P(statutory_port>cash)": float((d > 0).mean()),
            "statutory_cash_terminal_balance_p50_B": float(np.median(ba[:, -1])) / 1e9,
            "statutory_port_terminal_balance_p50_B": float(np.median(bp[:, -1])) / 1e9,
            "rho_star": breakeven_rho(ba, wa, bb, wb),
        })
    return pd.DataFrame(rows)


# =============================================================================
# NEW: "Amendment Cost" scenario
# Statutory rule under the NRF Act 2021 schedule vs the Fiscal Enactments
# (Amendment) Act 2024 schedule, each with cash and with a portfolio.
# The amendment moves money out earlier; in total-wealth terms it costs
# Guyana only if rho is below the return the fund would have earned on the
# money it no longer holds. We report that breakeven explicitly.
# =============================================================================
def amendment_cost(cfg: dict) -> pd.DataFrame:
    years, price, prod, deposits, port_r, cash_r = gen_paths(cfg)
    T = len(years)
    arms = {}
    for alloc, ret in (("cash", cash_r), ("port", port_r)):
        for sched in ("amended2024", "original2021"):
            arms[(alloc, sched)] = simulate(cfg, deposits, ret, "statutory", schedule=sched)
    rows = []
    for alloc in ("cash", "port"):
        ba, wa = arms[(alloc, "amended2024")]
        bo, wo = arms[(alloc, "original2021")]
        # cumulative withdrawals over first 5 and 10 years and full horizon
        row = {"allocation": alloc}
        for h in (5, 10, T):
            row[f"cum_wd_amended_{h}y_p50_B"] = float(np.median(wa[:, :h].sum(1))) / 1e9
            row[f"cum_wd_original_{h}y_p50_B"] = float(np.median(wo[:, :h].sum(1))) / 1e9
        row["terminal_balance_amended_p50_B"] = float(np.median(ba[:, -1])) / 1e9
        row["terminal_balance_original_p50_B"] = float(np.median(bo[:, -1])) / 1e9
        row["forgone_terminal_balance_p50_B"] = row["terminal_balance_original_p50_B"] - row["terminal_balance_amended_p50_B"]
        for rho in cfg["rho_grid"]:
            Wa, Wo = total_wealth(ba, wa, rho), total_wealth(bo, wo, rho)
            row[f"W_amended_minus_original_rho{int(round(rho*100)):02d}_p50_B"] = float(np.median(Wa - Wo)) / 1e9
        # breakeven rho: amended == original in median total wealth.
        # breakeven_rho(A=original, B=amended): amended withdraws MORE, EARLIER,
        # so median(W_amended - W_original) is INCREASING in rho; flip sign by
        # passing (a=amended, b=original) so gap decreases in rho as required.
        row["rho_star_amendment"] = breakeven_rho(ba, wa, bo, wo)
        rows.append(row)
    return pd.DataFrame(rows)


# =============================================================================
# Sensitivity (tornado): one-at-a-time on median terminal total wealth gap
# (norway_port - statutory_cash) at rho_headline.
# =============================================================================
TORNADO_PARAMS = {
    "long_run_price":    (50.0, 80.0),
    "price_vol":         (0.20, 0.35),
    "prod_haircut":      (0.80, 1.00),
    "take_end":          (0.145, 0.30),
    "port_real_return":  (0.02, 0.04),
    "cash_real_return":  (0.000, 0.015),   # widened: 2025 realized ~1.4% real
    "rho_headline":      (0.00, 0.10),
    "spend_rate":        (0.02, 0.04),
    "port_oil_corr":     (0.0, 0.3),
    "decline_rate":      (0.04, 0.08),
}


def metric(cfg: dict) -> float:
    _, _, res = run(cfg)
    ba, wa = res["statutory_cash"]
    bb, wb = res["norway_port"]
    rho = cfg["rho_headline"]
    return float(np.median(total_wealth(bb, wb, rho) - total_wealth(ba, wa, rho)))


def tornado(cfg: dict, n_paths_fast: int = 4000):
    base_cfg = dict(cfg, n_paths=n_paths_fast)
    base = metric(base_cfg)
    rows = []
    for p, (lo, hi) in TORNADO_PARAMS.items():
        m_lo = metric(dict(base_cfg, **{p: lo}))
        m_hi = metric(dict(base_cfg, **{p: hi}))
        rows.append((p, m_lo, m_hi))
    rows.sort(key=lambda r: -abs(r[2] - r[1]))
    return base, rows


# =============================================================================
# Charts
# =============================================================================
def plot_fanchart(years, res, path):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for name, color, label in [("statutory_cash", "tab:red", "Status quo (statutory rule, cash)"),
                               ("statutory_port", "tab:green", "Statutory rule, diversified"),
                               ("norway_port", "tab:blue", "Norway-style (3% rule, diversified)")]:
        bal = res[name][0] / 1e9
        p10, p50, p90 = np.percentile(bal, [10, 50, 90], axis=0)
        ax.fill_between(years, p10, p90, alpha=0.15, color=color)
        ax.plot(years, p50, color=color, lw=2, label=f"{label} — median")
    ax.set_ylabel("NRF balance (real 2026 US$B)")
    ax.set_title("Fund balance trajectories, P10–P90 bands (paired paths)")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_tornado(base, rows, path):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    labels = [r[0] for r in rows][::-1]
    lo = np.array([min(r[1], r[2]) for r in rows][::-1]) / 1e9
    hi = np.array([max(r[1], r[2]) for r in rows][::-1]) / 1e9
    y = np.arange(len(rows))
    ax.barh(y, hi - lo, left=lo, color="tab:gray", alpha=0.75)
    ax.axvline(base / 1e9, color="k", lw=1.5, ls="--", label=f"base = {base/1e9:.1f}")
    ax.set_yticks(y, labels)
    ax.set_xlabel("Median terminal wealth gap, Norway − status quo "
                  f"(US$B, ρ = headline)")
    ax.set_title("One-at-a-time sensitivity")
    ax.legend(); ax.grid(alpha=0.3, axis="x")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_cash_sweep(sweep: pd.DataFrame, cfg: dict, path):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = sweep["cash_real_return"] * 100
    ax.plot(x, sweep["statutory_port_minus_cash_medianW_B"], "o-", color="tab:green",
            lw=2, label="Statutory rule: portfolio − cash (median terminal wealth)")
    ax.fill_between(x, sweep["statutory_port_minus_cash_p10_B"],
                    sweep["statutory_port_minus_cash_p90_B"], alpha=0.15, color="tab:green",
                    label="P10–P90 of per-path difference")
    ax.plot(x, sweep["norway_port_minus_cash_medianW_B"], "s--", color="tab:blue",
            lw=1.5, label="Norway rule: portfolio − cash")
    ax.axhline(0, color="k", lw=1)
    ax.axvline(cfg["cash_real_return"] * 100, color="gray", ls=":", label="Aug-2026 base (0.5%)")
    ax.axvline(cfg["cash_current_real"] * 100, color="tab:red", ls=":", label="2025 realized (~1.4% real)")
    ax.set_xlabel("Cash (FRBNY overnight) real return, % p.a.")
    ax.set_ylabel("US$B (real 2026), ρ = headline")
    ax.set_title("Allocation spread vs. assumed cash real return")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_historical(path, csv="nrf_timeseries.csv"):
    """Prefer parsed monthly data; fall back to annual reference points."""
    fig, ax = plt.subplots(figsize=(9, 5))
    if os.path.exists(csv):
        d = pd.read_csv(csv).dropna(subset=["balance"]).sort_values("period")
        ax.plot(d["period"], d["balance"] / 1e9, marker="o", label="Balance (parsed)")
        if "withdrawals" in d:
            ax.bar(d["period"], d["withdrawals"].fillna(0) / 1e9, alpha=0.4,
                   label="Withdrawals (parsed)")
        ax.set_title("NRF balance vs withdrawals (parsed from official PDFs)")
    else:
        yrs = [2021, 2022, 2023, 2024, 2025, 2026]
        # actuals: 2022 BoG; 2023 BoG Q4-2023 Quarterly; 2024 MoF; 2025 NRF
        # Annual Report 2025; 2026 = approved ceiling (not yet realized)
        wd = [0, 0.6076, 1.00213, 1.586, 2.463, 2.374]
        bal_pts = {2021: 0.6075, 2025.75: 3.594, 2026.58: 4.35}
        ax.bar(yrs, wd, alpha=0.5, color="tab:orange",
               label="Annual withdrawal (2022–25 actual; 2026 = approved ceiling)")
        ax.plot(list(bal_pts), list(bal_pts.values()), "o-", color="tab:blue",
                label="Balance (verified points: end-2021, 30-Sep-2025, end-Jul-2026)")
        ax.set_title("NRF: withdrawals vs balance — FALLBACK DATA, replace with "
                     "nrf_ingest.py output")
    ax.set_ylabel("US$B"); ax.legend(fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


# =============================================================================
def main():
    cfg = CONFIG
    os.makedirs("out", exist_ok=True)
    years, deposits, res = run(cfg)

    ba, wa = res["statutory_cash"]
    bb, wb = res["norway_port"]

    # summary table across rho grid (unchanged layout)
    rows = []
    for rho in cfg["rho_grid"]:
        Wa, Wb = total_wealth(ba, wa, rho), total_wealth(bb, wb, rho)
        gap = Wb - Wa
        rows.append({
            "rho": rho,
            "W_statusquo_p50_B": np.median(Wa) / 1e9,
            "W_norway_p50_B": np.median(Wb) / 1e9,
            "gap_p10_B": np.percentile(gap, 10) / 1e9,
            "gap_p50_B": np.median(gap) / 1e9,
            "gap_p90_B": np.percentile(gap, 90) / 1e9,
            "P(gap>0)": float((gap > 0).mean()),
        })
    summary = pd.DataFrame(rows)

    rho_star = breakeven_rho(ba, wa, bb, wb)

    # decomposition at rho_headline: isolate rule effect vs allocation effect
    rho = cfg["rho_headline"]
    W = median_2x2(res, rho)
    decomp = pd.DataFrame([
        {"variant": k, "median_terminal_wealth_B": v} for k, v in W.items()])

    # --- new scenarios ---
    sweep = cash_sweep(cfg)
    decl = declining_rate(cfg)
    amend = amendment_cost(cfg)

    base, trows = tornado(cfg)
    plot_fanchart(years, res, "out/fanchart.png")
    plot_tornado(base, trows, "out/tornado.png")
    plot_historical("out/historical.png")
    plot_cash_sweep(sweep, cfg, "out/cash_sweep.png")

    summary.to_csv("out/results_summary.csv", index=False)
    decomp.to_csv("out/decomposition_2x2.csv", index=False)
    sweep.to_csv("out/cash_sweep.csv", index=False)
    decl.to_csv("out/declining_rate.csv", index=False)
    amend.to_csv("out/amendment_cost.csv", index=False)

    ff = lambda x: f"{x:,.3f}"
    print(summary.to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print(f"\nBreakeven domestic social return rho* (median-wealth tie): "
          f"{rho_star:.3%}" if np.isfinite(rho_star) else "\nrho*: no crossing in [-2%, 20%]")
    print("\n2x2 decomposition (median terminal wealth, US$B, rho = "
          f"{rho:.0%}):\n{decomp.to_string(index=False, float_format=lambda x: f'{x:,.1f}')}")

    print("\n=== Cash real-return sweep (rho = headline) ===")
    cols = ["cash_real_return", "statutory_cash_p50_B", "statutory_port_p50_B",
            "statutory_port_minus_cash_medianW_B", "P(statutory_port>cash)",
            "norway_port_minus_cash_medianW_B", "rho_star", "rho_star_rule_only_cash"]
    print(sweep[cols].to_string(index=False, float_format=ff))
    print("\nStatutory allocation spread by rho — per-path median (exactly rho-invariant "
          "when withdrawals are identical):")
    print(sweep[["cash_real_return", "statutory_withdrawals_identical"]
                + [c for c in sweep.columns if c.startswith("stat_spread_pathmedian")]]
          .to_string(index=False, float_format=ff))

    print("\n=== Declining-rate scenario ===")
    print(decl.to_string(index=False, float_format=ff))

    print("\n=== Amendment Cost scenario (amended2024 vs original2021) ===")
    print(amend.to_string(index=False, float_format=ff))

    print("\nCharts + CSVs in ./out")


if __name__ == "__main__":
    main()
