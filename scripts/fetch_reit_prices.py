#!/usr/bin/env python3
"""Fetch REIT Weekly price data (Price / 5D / YTD / 1-Yr) for the 19-issuer universe.

Runs OUTSIDE the claude.ai routine sandbox (GitHub Actions, or any machine with a
plain internet route) because that sandbox's egress proxy refuses CONNECT to
query1.finance.yahoo.com ("Tunnel connection failed: 403 Forbidden") — blocked
every Monday run since 2026-08-10.

Output: rw_prices.json in the repo root. The REIT Weekly agent prompt reads that
file when its own direct Yahoo pull is blocked. Same data, same methodology, just
collected from a network that can actually reach Yahoo.

Methodology (unchanged from the approved format):
  as_of  = last trading day on or before the covered Friday
  Price  = close on as_of
  5D     = as_of close vs. the close one week earlier (prior Friday)
  YTD    = as_of close vs. the last close of the prior calendar year
  1-Yr   = as_of close vs. the close ~365 days earlier
"""
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone

TICKERS = ["CURB", "REG", "FRT", "BRX", "KIM", "KRG", "PECO", "UE", "IVT",
           "ADC", "SPG", "MAC", "CBL", "SKT", "AKR", "NNN", "EPRT", "BNL", "GTY"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HOSTS = ["query1.finance.yahoo.com", "query2.finance.yahoo.com"]


def fetch_series(ticker):
    """Return [(date, close), ...] ascending for ~2y of daily closes."""
    last_err = None
    for host in HOSTS:
        url = (f"https://{host}/v8/finance/chart/{ticker}"
               f"?range=2y&interval=1d&includePrePost=false")
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                           "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    payload = json.load(r)
                res = payload["chart"]["result"][0]
                stamps = res["timestamp"]
                closes = res["indicators"]["quote"][0]["close"]
                series = [(datetime.fromtimestamp(t, tz=timezone.utc).date(), c)
                          for t, c in zip(stamps, closes) if c is not None]
                series.sort()
                if series:
                    return series
                last_err = "empty series"
            except Exception as e:  # noqa: BLE001 - report whatever Yahoo did
                last_err = f"{type(e).__name__}: {e}"
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{ticker}: {last_err}")


def close_on_or_before(series, target):
    for d, c in reversed(series):
        if d <= target:
            return d, c
    return None, None


def pct(new, old):
    if new is None or old is None or not old:
        return None
    return round((new / old - 1.0) * 100, 2)


def covered_friday(today):
    """The Friday of the week the report covers (the most recent Friday before today)."""
    back = (today.weekday() - 4) % 7 or 7
    return today - timedelta(days=back)


def main():
    today = date.today()
    friday = covered_friday(today)
    out = {
        "schema": "rw_prices/1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generated_by": "GitHub Actions workflow reit-prices.yml (Yahoo Finance chart API)",
        "covered_friday": friday.isoformat(),
        "methodology": ("Price = close on as_of (last trading day <= covered Friday); "
                        "5D = vs close one week earlier; YTD = vs last close of prior "
                        "calendar year; 1-Yr = vs close ~365 days earlier. Source: "
                        "Yahoo Finance chart API v8, daily closes."),
        "tickers": {},
        "errors": {},
    }
    prior_year_end = date(friday.year - 1, 12, 31)
    for t in TICKERS:
        try:
            s = fetch_series(t)
        except RuntimeError as e:
            out["errors"][t] = str(e)
            print(f"ERROR {e}", file=sys.stderr)
            continue
        as_of, price = close_on_or_before(s, friday)
        _, wk_ago = close_on_or_before(s, friday - timedelta(days=7))
        ytd_date, ytd_base = close_on_or_before(s, prior_year_end)
        yr_date, yr_base = close_on_or_before(s, friday - timedelta(days=365))
        out["tickers"][t] = {
            "price": round(price, 2) if price is not None else None,
            "as_of": as_of.isoformat() if as_of else None,
            "ret_5d_pct": pct(price, wk_ago),
            "ret_ytd_pct": pct(price, ytd_base),
            "ret_1yr_pct": pct(price, yr_base),
            "ytd_base_date": ytd_date.isoformat() if ytd_date else None,
            "yr_base_date": yr_date.isoformat() if yr_date else None,
        }
        print(f"{t:5s} {out['tickers'][t]['price']!s:>8s} "
              f"5D {out['tickers'][t]['ret_5d_pct']!s:>7s} "
              f"YTD {out['tickers'][t]['ret_ytd_pct']!s:>7s} "
              f"1Y {out['tickers'][t]['ret_1yr_pct']!s:>7s}  as of {as_of}")
        time.sleep(0.4)

    out["complete"] = len(out["tickers"]) == len(TICKERS) and not out["errors"]
    with open("rw_prices.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=False)
        f.write("\n")
    print(f"\nWrote rw_prices.json — {len(out['tickers'])}/{len(TICKERS)} tickers, "
          f"complete={out['complete']}, covered Friday {friday}")
    # Fail the job if we got nothing at all; partial pulls still publish.
    return 0 if out["tickers"] else 1


if __name__ == "__main__":
    sys.exit(main())
