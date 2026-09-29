"""
ingest.py — unduh data World Bank untuk semua negara & indikator → staging.

Idempoten (lewati bila parquet sudah ada kecuali --force). Retry + timeout
agar tahan gangguan jaringan.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from config import COUNTRIES, INDICATORS, STAGING, WB_BASE, YEAR_END, YEAR_START

H = {"User-Agent": "report-automation-engine/1.0", "Accept": "application/json"}


def _get(url: str, retries: int = 3):
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=H), timeout=45) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(str(last)[:120])


def main(force: bool = False) -> None:
    t0 = time.time()
    out = STAGING / "wb_panel.parquet"
    if out.exists() and not force:
        print(f"[ingest] {out.name} sudah ada — dilewati (pakai --force untuk ulang)")
        return

    codes = ";".join(COUNTRIES)
    rows = []
    print(f"[ingest] World Bank: {len(COUNTRIES)} negara × "
          f"{len(INDICATORS)} indikator ({YEAR_START}–{YEAR_END})")
    for code, meta in INDICATORS.items():
        url = (f"{WB_BASE}/country/{codes}/indicator/{code}?format=json"
               f"&per_page=5000&date={YEAR_START}:{YEAR_END}")
        try:
            d = _get(url)
        except Exception as e:  # noqa: BLE001
            print(f"  ! {code}: {str(e)[:60]} — dilewati")
            continue
        if len(d) < 2 or not d[1]:
            print(f"  ! {code}: tidak ada data")
            continue
        n = 0
        for rec in d[1]:
            iso = rec["countryiso3code"]
            if iso not in COUNTRIES:
                continue
            rows.append({
                "country_iso": iso,
                "country": COUNTRIES[iso],
                "indicator_code": code,
                "indicator": meta["nama"],
                "category": meta["kategori"],
                "unit": meta["satuan"],
                "year": int(rec["date"]),
                "value": rec["value"],
            })
            n += 1
        print(f"  {code:20} {meta['nama']:20} {n} baris")

    df = pd.DataFrame(rows).dropna(subset=["value"])
    df.to_parquet(out, index=False)
    meta = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "rows": int(len(df)),
        "countries": list(COUNTRIES.values()),
        "indicators": list(INDICATORS),
        "years": [int(df["year"].min()), int(df["year"].max())] if len(df) else [],
        "duration_sec": round(time.time() - t0, 1),
    }
    (STAGING / "_ingest_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ingest] selesai: {len(df)} baris valid ({meta['duration_sec']}s)")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
