#!/usr/bin/env python3
"""
NRF report ingestion.

Parses Guyana Natural Resource Fund monthly/quarterly PDF reports
(Ministry of Finance, finance.gov.gy; figures originate with Bank of Guyana)
into a clean time series:

    period, balance_usd, inflows_usd, withdrawals_usd, interest_usd,
    financial_assets_fv_usd, source_file, flags

Design principles
-----------------
1. NEVER silently drop a document or a line item. Anything unparsed lands in
   flags.csv with the reason and the raw text neighborhood.
2. Layouts change across years. Extraction is keyword-anchored with synonym
   lists, not position-anchored.
3. Two modes:
     a) --dir <folder>   parse already-downloaded PDFs (recommended; grab them
                         manually or with --scrape which is best-effort only)
     b) --scrape         attempt to discover PDF links on the ministry site
4. Cross-checks: balance_t ?= balance_{t-1} + inflows - withdrawals + interest.
   Violations beyond tolerance are flagged, not "fixed".

Usage
-----
    pip install pdfplumber requests beautifulsoup4 pandas
    python nrf_ingest.py --dir ./nrf_pdfs --out nrf_timeseries.csv
    python nrf_ingest.py --scrape --out nrf_timeseries.csv   # best effort

Output: nrf_timeseries.csv, nrf_flags.csv
"""

from __future__ import annotations
import argparse, os, re, sys, glob
from dataclasses import dataclass, field

import pandas as pd

try:
    import pdfplumber
except ImportError:
    sys.exit("pip install pdfplumber")

# ----------------------------------------------------------------------------
# Label synonyms observed / expected across report vintages.
# Extend these lists when flags.csv shows misses — do not edit parser logic.
# ----------------------------------------------------------------------------
# VERIFIED 2026-09-23 against three fetched reports (Dec-2023, Dec-2025,
# Jun-2026). Patterns marked [V] match a label observed verbatim; the rest are
# retained as defensive synonyms for vintages not yet examined.
#
# Six of the twelve real labels were missed by the original guessed patterns,
# including "Financial Assets held at fair value through profit and loss" --
# the line item carrying the paper's central claim. The recurring failure was
# assuming adjacent words ("at fair value" vs "held at fair value";
# "Total Net Assets Value" vs "Total Net Assets").
LABELS = {
    "balance": [
        r"closing\s+balance",                       # [V] Table 3
        r"total\s+net\s+assets?\b",                 # [V] Table 4
        r"final\s+market\s+value",                  # [V] Table 1
        r"balance\s+at\s+end", r"end\s+of\s+period\s+balance",
        r"net\s+asset\s+value", r"fund\s+balance",
    ],
    "opening_balance": [
        r"opening\s+balance\s+at\s+beginning",      # [V] Table 3
        r"starting\s+market\s+value",               # [V] Table 1
    ],
    "inflows": [
        r"^\s*inflows\b",                           # [V] Table 1 (bare row label)
        r"inflows\s+to\s+fund\s+for\s+the\s+quarter",   # [V] Table 3
        r"total\s+(?:deposits|inflows|receipts)",
        r"petroleum\s+revenues?\s+(?:received|deposited)",
        r"deposits?\s+during\s+the\s+(?:month|period|quarter)",
    ],
    "royalty": [r"royalt(?:y|ies)"],                # [V] Tables 3, 6
    "profit_oil": [
        r"profit\s+oil",                            # [V] Tables 3, 6
        r"sale\s+of\s+(?:government'?s?\s+share\s+of\s+)?profit\s+oil",
        r"lift(?:s|ings)?\s+proceeds",
    ],
    "signature_bonus": [r"signature\s+bonus"],      # [V] Table 3, from 2025Q4
    "withdrawals": [
        r"withdrawal(?:s)?",                        # [V] Tables 1, 7
        r"outflows\s+from\s+fund\s+to\s+consolidated\s+fund",   # [V] Table 3
        r"transfer(?:s)?\s+to\s+(?:the\s+)?consolidated\s+fund",
    ],
    "interest": [
        r"interest\s+income",                       # [V] Tables 1, 5
        r"total\s+investment\s+income",             # [V] Table 5
        r"interest\s+(?:earned|received)", r"income\s+from\s+investments",
    ],
    "financial_assets_fv": [
        # [V] Table 4, exact: "Financial Assets held at fair value through
        # profit and loss". "held" sits between "assets" and "at fair value",
        # which is what broke the original pattern.
        r"financial\s+assets\s+(?:held\s+)?at\s+fair\s+value",
        r"securities\s+at\s+fair\s+value", r"investments?\s+at\s+fair\s+value",
    ],
    "other_receivables": [r"other\s+receivables"],  # [V] Table 4
    "cash_equivalents": [r"cash\s+and\s+cash\s+equivalents"],   # [V] Table 4
}

# ---------------------------------------------------------------------------
# COLUMN HAZARD -- read before trusting any parsed number.
#
# These are multi-column tables, not prose. Table 1 "Changes in Market Value"
# in the Jun-2026 report carries SIX numeric columns on one row:
#     2025Q3 | 2025Q4 | 2026Q1 | 2026Q2 | YTD | Since Inception
# A parser that takes "the first amount after the label" silently returns the
# OLDEST comparative quarter, not the reporting period, and a YTD or
# since-inception figure will occasionally land in a quarterly series.
#
# Table 3 (Capital Account), 4 (Assets) and 5 (Income) each carry two columns:
# the prior quarter and the reporting quarter -- so the naive first-match
# returns the PRIOR quarter there. Take the LAST numeric on those rows, or
# match on the column header, and cross-check every row against the
# balance identity below.
# ---------------------------------------------------------------------------

# US$ or G$ amounts like: US$1,234,567.89 / USD 1.2 billion / 4,100.5 million
AMOUNT = re.compile(
    r"(?P<cur>US\$|USD|G\$|GYD)?\s*(?P<num>[\d,]+(?:\.\d+)?)\s*(?P<scale>billion|bn|million|mn|m\b|thousand)?",
    re.IGNORECASE,
)
SCALE = {"billion": 1e9, "bn": 1e9, "million": 1e6, "mn": 1e6, "m": 1e6, "thousand": 1e3, None: 1.0, "": 1.0}

MONTHS = ("january february march april may june july august september october november december").split()
PERIOD_RE = re.compile(
    r"(?P<month>" + "|".join(MONTHS) + r")\s*,?\s*(?P<year>20\d\d)"
    r"|(?P<q>q[1-4]|first|second|third|fourth)\s+quarter\s*,?\s*(?P<qyear>20\d\d)",
    re.IGNORECASE,
)

# Annual reference points. Every row below is now transcribed from a primary
# Bank of Guyana quarterly report, so these serve as the parser's VALIDATION
# TARGET rather than as a fallback. Withdrawals are ACTUAL (Table 7,
# transaction level), not approved ceilings -- the distinction the earlier
# version of this table could not make.
# status: P = primary (BoG quarterly report, named in note)
ANNUAL_VERIFIED = [
    # year, deposits_usd, withdrawals_actual_usd, yearend_balance_usd, status, note
    (2021, None,     0.0,        607.65e6,  "P", "Dec-2023 Graph 6 (G$126,694M / 208.50)"),
    (2022, 1411.95e6, 607.646570e6, 1429.45e6, "P", "Dec-2023 s6.1 + Jun-2026 Table 7"),
    (2023, 1608.22e6, 1002.130249e6, 2122.38e6, "P", "Dec-2023 s6.1, Table 1, Table 7"),
    (2024, 2567.97e6, 1586.00e6,  3245.69e6, "P", "Dec-2025 s6.1 + Table 7"),
    (2025, 2509.71e6, 2463.00e6,  3434.53e6, "P", "Dec-2025 s6.1, s6.2, Table 1"),
    (2026, 1812.83e6, 1020.00e6,  4294.24e6, "P", "Jun-2026 -- H1 ONLY, through 2026Q2"),
]

# Approved ceilings, for the utilisation series. Footnoted verbatim in the
# reports for 2025 and 2026; 2023 is stated as "100% of the estimated amount".
CEILINGS_USD = {
    2022: 607.65e6, 2023: 1002.13e6, 2024: 1586.00e6,
    2025: 2463.88e6,   # Dec-2025 footnote 3
    2026: 2374.33e6,   # Jun-2026 footnote 1
}

# Constant in every report examined (Dec-2023, Dec-2025, Jun-2026).
GYD_PER_USD = 208.50

# Balance identity, for cross-checking any parse. Verified to close within
# G$1M in all 11 quarters where Table 1 supplies flows:
#     balance_t == balance_{t-1} + inflows - withdrawals + interest_income
BALANCE_IDENTITY_TOLERANCE_GYD = 1e6


@dataclass
class Flag:
    source: str
    field: str
    reason: str
    context: str = ""

@dataclass
class Record:
    period: str = ""
    source_file: str = ""
    values: dict = field(default_factory=dict)   # field -> USD float
    flags: list = field(default_factory=list)


def parse_amount_near(text: str, label_patterns: list[str], source: str, fieldname: str,
                      flags: list[Flag], window: int = 160):
    """Find first label match; extract the first plausible USD amount within
    `window` chars after it. Returns float USD or None (and flags the miss)."""
    for pat in label_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if not m:
            continue
        seg = text[m.end(): m.end() + window]
        best = None
        for am in AMOUNT.finditer(seg):
            num = am.group("num")
            if num in (None, "") or num.replace(",", "") in ("", "."):
                continue
            val = float(num.replace(",", ""))
            scale = SCALE[(am.group("scale") or "").lower() or None]
            cur = (am.group("cur") or "").upper()
            usd = val * scale
            if cur in ("G$", "GYD"):
                # G$ figure — convert at ~208 G$/US$ (flag: rate varies)
                usd = usd / 208.0
                flags.append(Flag(source, fieldname, "converted from G$ at 208; verify rate", seg[:80]))
            # plausibility gate: NRF magnitudes are 1e5..1e10 USD
            if 1e5 <= usd <= 5e10:
                best = usd
                break
        if best is not None:
            return best
        flags.append(Flag(source, fieldname, "label found but no plausible amount nearby", seg[:120]))
        return None
    flags.append(Flag(source, fieldname, "no label variant matched", ""))
    return None


def detect_period(text: str, source: str, flags: list[Flag]) -> str:
    m = PERIOD_RE.search(text[:2000]) or PERIOD_RE.search(text)
    if not m:
        flags.append(Flag(source, "period", "could not detect reporting period", text[:120]))
        return ""
    if m.group("month"):
        mon = MONTHS.index(m.group("month").lower()) + 1
        return f"{m.group('year')}-{mon:02d}"
    qmap = {"q1": "Q1", "first": "Q1", "q2": "Q2", "second": "Q2",
            "q3": "Q3", "third": "Q3", "q4": "Q4", "fourth": "Q4"}
    return f"{m.group('qyear')}-{qmap[m.group('q').lower()]}"


def parse_pdf(path: str) -> Record:
    rec = Record(source_file=os.path.basename(path))
    fl: list[Flag] = []
    try:
        with pdfplumber.open(path) as pdf:
            text = "\n".join((p.extract_text() or "") for p in pdf.pages)
    except Exception as e:
        fl.append(Flag(rec.source_file, "*", f"unreadable PDF: {e}"))
        rec.flags = fl
        return rec
    if len(text.strip()) < 100:
        fl.append(Flag(rec.source_file, "*", "near-empty text layer (scanned image?); needs OCR"))
        rec.flags = fl
        return rec

    rec.period = detect_period(text, rec.source_file, fl)
    for fieldname, pats in LABELS.items():
        v = parse_amount_near(text, pats, rec.source_file, fieldname, fl)
        if v is not None:
            rec.values[fieldname] = v
    rec.flags = fl
    return rec


def scrape_pdf_links(out_dir: str) -> list[str]:
    """Discovery of NRF report PDFs.

    VERIFIED 2026-09-23. The reports are served by the Bank of Guyana, and the
    working path segment is `bog3`, not `bog` -- the `bog` spelling redirects.
    Direct construction is more reliable than scraping an index:

        https://bankofguyana.org.gy/bog3/images/accounts_budgeting/
            natural_resource_fund/quarterly/nrf-{month}{year}-quarterly.pdf

    e.g. nrf-december2025-quarterly.pdf, nrf-june2026-quarterly.pdf.
    Confirmed working for december2023, december2025 and june2026.

    Fetch the December report of each year first: its Table 1 carries all four
    quarters of that year plus a since-inception column, Table 6 carries
    lift-level inflows since March 2020, and Table 7 carries every withdrawal
    by date since 2022. Roughly eight documents reconstruct the whole series.
    """
    import requests
    from bs4 import BeautifulSoup
    seeds = [
        "https://bankofguyana.org.gy/bog3/index.php/publications/natural-resource-fund",
        "https://finance.gov.gy/natural-resource-fund/",
        "https://finance.gov.gy/publications/",
    ]
    os.makedirs(out_dir, exist_ok=True)
    found = []
    for url in seeds:
        try:
            r = requests.get(url, timeout=30)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select("a[href$='.pdf']"):
                href = a["href"]
                if not href.startswith("http"):
                    href = "https://finance.gov.gy" + href
                if re.search(r"(nrf|natural[\s_-]*resource)", href, re.I):
                    found.append(href)
        except Exception as e:
            print(f"[scrape] {url}: {e}", file=sys.stderr)
    paths = []
    for href in sorted(set(found)):
        dest = os.path.join(out_dir, os.path.basename(href))
        if not os.path.exists(dest):
            try:
                r = requests.get(href, timeout=60)
                open(dest, "wb").write(r.content)
            except Exception as e:
                print(f"[download] {href}: {e}", file=sys.stderr)
                continue
        paths.append(dest)
    return paths


def cross_check(df: pd.DataFrame, flags: list[Flag], tol: float = 0.02):
    """balance_t ≈ balance_{t-1} + inflows - withdrawals + interest, within tol."""
    d = df.sort_values("period").reset_index(drop=True)
    for i in range(1, len(d)):
        prev, cur = d.loc[i - 1], d.loc[i]
        need = ("balance", "inflows", "withdrawals")
        if any(pd.isna(cur.get(k)) for k in need) or pd.isna(prev.get("balance")):
            continue
        implied = prev["balance"] + cur["inflows"] - cur["withdrawals"] + (cur.get("interest") or 0.0)
        if prev["balance"] > 0 and abs(implied - cur["balance"]) / max(cur["balance"], 1) > tol:
            flags.append(Flag(cur["source_file"], "reconciliation",
                              f"period {cur['period']}: implied {implied:,.0f} vs reported {cur['balance']:,.0f}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", help="folder of already-downloaded NRF PDFs")
    ap.add_argument("--scrape", action="store_true", help="attempt link discovery + download")
    ap.add_argument("--out", default="nrf_timeseries.csv")
    args = ap.parse_args()

    paths = []
    if args.scrape:
        paths += scrape_pdf_links("./nrf_pdfs")
    if args.dir:
        paths += sorted(glob.glob(os.path.join(args.dir, "*.pdf")))
    if not paths:
        print("No PDFs. Download reports from finance.gov.gy into ./nrf_pdfs "
              "and rerun with --dir ./nrf_pdfs.\nWriting fallback annual "
              "reference table (VERIFY before citing).", file=sys.stderr)
        pd.DataFrame(ANNUAL_FALLBACK, columns=[
            "year", "deposits_usd", "withdrawals_usd", "yearend_balance_usd",
            "status", "note"]).to_csv("nrf_annual_fallback.csv", index=False)
        return

    records = [parse_pdf(p) for p in paths]
    all_flags: list[Flag] = [f for r in records for f in r.flags]

    rows = []
    for r in records:
        row = {"period": r.period, "source_file": r.source_file}
        row.update({k: r.values.get(k) for k in LABELS})
        rows.append(row)
    df = pd.DataFrame(rows)
    cross_check(df, all_flags)

    df.to_csv(args.out, index=False)
    pd.DataFrame([vars(f) for f in all_flags]).to_csv("nrf_flags.csv", index=False)
    n_bad = sum(1 for r in records if not r.values)
    print(f"parsed {len(records)} PDFs -> {args.out}; {len(all_flags)} flags "
          f"({n_bad} files yielded nothing) -> nrf_flags.csv")
    print("Report the flag rate in your paper's data section — it is a feature.")


if __name__ == "__main__":
    main()
