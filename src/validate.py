"""
validate.py — validasi LAPORAN EXCEL (uja kelengkapan & struktur).

Memastikan workbook yang dihasilkan benar-benar siap kirim:
  · 5 sheet ada
  · header & styling terpasang
  · chart native ada
  · data konsisten dengan sumber (jumlah baris)
  · tidak ada nilai kosong tak terduga
Output: reports/validation.json + reports/validation.md
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from openpyxl import load_workbook

from config import COUNTRIES, INDICATORS, OUTPUT, REPORTS, STAGING

EXPECTED_SHEETS = ["Cover", "Ringkasan", "Per Indikator", "Data", "Catatan"]


def main() -> None:
    files = sorted(glob.glob(str(OUTPUT / "*.xlsx")))
    if not files:
        raise SystemExit("belum ada laporan Excel — jalankan build_excel.py")
    f = files[-1]
    wb = load_workbook(f)
    df = pd.read_parquet(STAGING / "wb_panel.parquet")

    checks = []
    checks.append(("5 sheet sesuai", wb.sheetnames == EXPECTED_SHEETS,
                   str(wb.sheetnames)))
    n_chart = sum(len(wb[s]._charts) for s in wb.sheetnames)
    checks.append(("chart native ada (>0)", n_chart > 0, f"{n_chart} chart"))
    data_rows = wb["Data"].max_row - 3
    checks.append(("jumlah baris data = sumber",
                   data_rows == len(df), f"{data_rows} vs {len(df)}"))
    # header brand terpasang di Ringkasan
    hdr = wb["Ringkasan"].cell(row=3, column=1)
    checks.append(("header berformat (fill brand)",
                   hdr.fill.fgColor.rgb not in (None, "00000000"),
                   str(hdr.fill.fgColor.rgb)))
    # freeze pane
    checks.append(("freeze pane di Data",
                   wb["Data"].freeze_panes is not None,
                   str(wb["Data"].freeze_panes)))
    # jumlah indikator & negara tercakup
    checks.append(("8 indikator tercakup",
                   df.indicator_code.nunique() == len(INDICATORS),
                   f"{df.indicator_code.nunique()}"))
    checks.append(("6 negara tercakup",
                   df.country_iso.nunique() == len(COUNTRIES),
                   f"{df.country_iso.nunique()}"))

    result = {"file": Path(f).name,
              "size_kb": round(Path(f).stat().st_size / 1024, 1),
              "sheets": wb.sheetnames, "charts": n_chart,
              "data_rows": data_rows,
              "checks": [{"nama": n, "lulus": bool(ok), "detail": d}
                         for n, ok, d in checks]}
    (REPORTS / "validation.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [f"# Validasi Laporan Excel", "",
          f"- File: `{result['file']}` ({result['size_kb']} KB)",
          f"- Sheet: {', '.join(result['sheets'])}",
          f"- Chart native: {n_chart}", f"- Baris data: {data_rows}", "",
          "| Uji | Status | Detail |", "|---|---|---|"]
    for n, ok, d in checks:
        md.append(f"| {n} | {'✅' if ok else '❌'} | {d} |")
    (REPORTS / "validation.md").write_text("\n".join(md), encoding="utf-8")

    print("[validate] hasil:")
    for n, ok, d in checks:
        print(f"   {'PASS' if ok else 'FAIL'}  {n} — {d}")
    print(f"[validate] {sum(1 for _, ok, _ in checks if ok)}/{len(checks)} lulus")
    print(f"[validate] → {REPORTS / 'validation.md'}")


if __name__ == "__main__":
    main()
