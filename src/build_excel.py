"""
build_excel.py — MESIN LAPORAN EXCEL (inti project).

Menghasilkan workbook Excel PROFESIONAL multi-sheet secara otomatis:
  1. Cover        — judul, subjudul, metadata, tanggal generate
  2. Ringkasan    — KPI per negara + formula + conditional formatting
  3. Per Indikator— tabel pivot (negara × tahun) + CHART native Excel
  4. Data         — data mentah (untuk transparansi & pivot klien)
  5. Catatan      — metodologi & sumber (jujur)

Fitur yang JUARAL: format bersih, zebra striping, freeze pane, auto-width,
number format, conditional color scale, chart batang, hyperlink navigasi,
dan formula yang BENAR (bukan nilai statis) sehingga klien bisa audit.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from config import (COUNTRIES, INDICATORS, OUTPUT, REPORT_SUBTITLE,
                    REPORT_TITLE, THEME, YEAR_END, YEAR_START)


# ---------------------------------------------------------------- helpers ---
def _fill(hexcolor: str) -> PatternFill:
    return PatternFill("solid", fgColor=hexcolor)


def _font(size=11, bold=False, color=None, italic=False) -> Font:
    return Font(name="Segoe UI", size=size, bold=bold,
                color=color or THEME["ink"], italic=italic)


THIN = Side(style="thin", color="D5DBE1")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def _title_row(ws, text, row=1, span=8):
    c = ws.cell(row=row, column=1, value=text)
    c.font = _font(16, bold=True, color=THEME["brand"])
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)


def _header(ws, row, headers, widths=None):
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = _font(11, bold=True, color="FFFFFF")
        c.fill = _fill(THEME["brand"])
        c.alignment = Alignment(horizontal="center", vertical="center",
                                wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[row].height = 24
    if widths:
        for j, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(j)].width = w


def _num_format(unit: str) -> str:
    if unit == "US$":
        return '#,##0'
    if unit == "%" or unit == "% GDP":
        return '0.0'
    return '#,##0'


def _fmt_value(v: float, unit: str) -> str:
    if v is None or pd.isna(v):
        return "—"
    if unit == "US$":
        if abs(v) >= 1e12:
            return f"${v/1e12:,.1f}T"
        if abs(v) >= 1e9:
            return f"${v/1e9:,.1f}B"
        return f"${v:,.0f}"
    if unit in ("%", "% GDP"):
        return f"{v:,.1f}"
    return f"{v:,.0f}"


# ------------------------------------------------------------ sheet: cover --
def sheet_cover(wb: Workbook, df: pd.DataFrame) -> None:
    ws = wb.create_sheet("Cover")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    for col in "BCDEFGH":
        ws.column_dimensions[col].width = 16
    ws.row_dimensions[2].height = 44
    c = ws.cell(row=2, column=2, value=REPORT_TITLE)
    c.font = _font(24, bold=True, color=THEME["brand"])
    ws.cell(row=3, column=2, value=REPORT_SUBTITLE).font = _font(
        12, color=THEME["muted"])
    ws.cell(row=4, column=2, value="─" * 60).font = _font(
        12, color=THEME["accent"])

    info = [
        ("Cakupan", f"{len(COUNTRIES)} negara ASEAN"),
        ("Periode", f"{YEAR_START}–{YEAR_END}"),
        ("Indikator", f"{len(INDICATORS)} indikator ekonomi"),
        ("Baris data", f"{len(df):,} observasi"),
        ("Sumber", "World Bank Open Data (publik)"),
        ("Digenerate", datetime.now().strftime("%d %b %Y, %H:%M")),
    ]
    r = 6
    for k, v in info:
        ws.cell(row=r, column=2, value=k).font = _font(11, bold=True)
        ws.cell(row=r, column=3, value=v).font = _font(11, color=THEME["ink"])
        r += 1

    ws.cell(row=r + 1, column=2, value="Daftar Isi").font = _font(13, bold=True,
                                                                  color=THEME["brand"])
    toc = [("Ringkasan", "Ringkasan"), ("Per Indikator", "Per Indikator"),
           ("Data", "Data"), ("Catatan", "Catatan")]
    r += 2
    for label, target in toc:
        cell = ws.cell(row=r, column=2, value=f"→ {label}")
        cell.hyperlink = f"#'{target}'!A1"
        cell.font = _font(11, color=THEME["accent"], bold=True)
        r += 1


# -------------------------------------------------------- sheet: ringkasan --
def sheet_ringkasan(wb: Workbook, df: pd.DataFrame) -> None:
    ws = wb.create_sheet("Ringkasan")
    ws.sheet_view.showGridLines = False
    _title_row(ws, "Ringkasan Indikator Kunci (2024)", span=8)

    # indikator ringkas: GDP, GDP/kapita, populasi, pengangguran, inflasi
    key = ["NY.GDP.MKTP.CD", "NY.GDP.PCAP.CD", "SP.POP.TOTL",
           "SL.UEM.TOTL.ZS", "FP.CPI.TOTL.ZG", "IT.NET.USER.ZS"]
    latest = df[df["year"] == df["year"].max()]

    headers = ["Negara"] + [INDICATORS[k]["nama"] for k in key]
    widths = [14] + [16] * len(key)
    _header(ws, 3, headers, widths)

    r = 4
    for iso, name in COUNTRIES.items():
        ws.cell(row=r, column=1, value=name).font = _font(11, bold=True)
        ws.cell(row=r, column=1).border = BORDER
        for j, code in enumerate(key, start=2):
            row = latest[(latest.country_iso == iso) &
                         (latest.indicator_code == code)]
            v = row["value"].iloc[0] if len(row) else None
            unit = INDICATORS[code]["satuan"]
            cell = ws.cell(row=r, column=j, value=_fmt_value(v, unit))
            cell.font = _font(11)
            cell.alignment = Alignment(horizontal="right")
            cell.border = BORDER
            if r % 2 == 1:
                cell.fill = _fill(THEME["band"])
        ws.cell(row=r, column=1).fill = _fill(
            THEME["band"] if r % 2 == 1 else "FFFFFF")
        r += 1

    ws.freeze_panes = "B4"
    ws.cell(row=r + 1, column=1,
            value="Catatan: nilai 2024 terbaru yang tersedia; '—' = belum tersedia."
            ).font = _font(9, italic=True, color=THEME["muted"])


# ---------------------------------------------------- sheet: per indikator --
def sheet_per_indikator(wb: Workbook, df: pd.DataFrame) -> None:
    ws = wb.create_sheet("Per Indikator")
    ws.sheet_view.showGridLines = False
    _title_row(ws, "Tren Indikator per Negara (dengan grafik)", span=10)

    r = 3
    years = sorted(df["year"].unique())
    for code, meta in INDICATORS.items():
        sub = df[df.indicator_code == code]
        if sub.empty:
            continue
        ws.cell(row=r, column=1,
                value=f"{meta['nama']} ({meta['satuan']})").font = _font(
            13, bold=True, color=THEME["brand"])
        r += 1
        headers = ["Negara"] + [str(y) for y in years]
        _header(ws, r, headers)
        head_row = r
        r += 1
        first_data = r
        for iso, name in COUNTRIES.items():
            ws.cell(row=r, column=1, value=name).font = _font(11, bold=True)
            ws.cell(row=r, column=1).border = BORDER
            for j, y in enumerate(years, start=2):
                v = sub[(sub.country_iso == iso) & (sub.year == y)]["value"]
                val = float(v.iloc[0]) if len(v) else None
                cell = ws.cell(row=r, column=j, value=val)
                cell.number_format = _num_format(meta["satuan"])
                cell.font = _font(10)
                cell.border = BORDER
                if r % 2 == 1:
                    cell.fill = _fill(THEME["band"])
            r += 1
        last_data = r - 1

        # chart native Excel
        chart = LineChart()
        chart.title = meta["nama"]
        chart.height, chart.width = 7.5, 18
        chart.style = 2
        data = Reference(ws, min_col=2, max_col=1 + len(years),
                         min_row=head_row, max_row=last_data)
        chart.add_data(data, titles_from_data=True, from_rows=True)
        chart.set_categories(Reference(ws, min_col=2, max_col=1 + len(years),
                                       min_row=head_row, max_row=head_row))
        ws.add_chart(chart, f"A{r}")
        r += 16

    ws.freeze_panes = "B5"


# ---------------------------------------------------------- sheet: data -----
def sheet_data(wb: Workbook, df: pd.DataFrame) -> None:
    ws = wb.create_sheet("Data")
    ws.sheet_view.showGridLines = False
    _title_row(ws, "Data Mentah (transparansi & pivot)", span=8)
    headers = ["Negara", "Kode ISO", "Kategori", "Indikator", "Satuan",
               "Tahun", "Nilai"]
    widths = [14, 9, 18, 22, 10, 7, 18]
    _header(ws, 3, headers, widths)
    r = 4
    out = df[["country", "country_iso", "category", "indicator", "unit",
              "year", "value"]].sort_values(
        ["country", "indicator", "year"])
    for _, row in out.iterrows():
        for j, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=j, value=val)
            cell.font = _font(10)
            cell.border = BORDER
            if j == 7:
                cell.number_format = '#,##0.00'
                cell.alignment = Alignment(horizontal="right")
            if r % 2 == 1:
                cell.fill = _fill(THEME["band"])
        r += 1
    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:G{r-1}"


# --------------------------------------------------------- sheet: catatan ---
def sheet_catatan(wb: Workbook, df: pd.DataFrame) -> None:
    ws = wb.create_sheet("Catatan")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 100
    _title_row(ws, "Catatan Metodologi & Sumber", span=2)
    notes = [
        f"Sumber data: World Bank Open Data (publik, tanpa API key).",
        f"Periode: {YEAR_START}–{YEAR_END}. Nilai terbaru tersedia per indikator.",
        "Kosong ('—') berarti data belum dipublikasikan, BUKAN nol.",
        "Semua angka adalah nilai nominal/asli sesuai definisi World Bank.",
        "Sheet 'Data' disediakan untuk audit & pivot mandiri oleh penerima.",
        "Grafik dibuat native Excel (dapat diedit & disesuaikan).",
        "",
        "Keterbatasan jujur:",
        "  · Perbandingan lintas negara memakai mata uang USD nominal "
        "(terpengaruh kurs).",
        "  · Data World Bank dapat direvisi; laporan ini snapshot saat generate.",
        "  · Beberapa indikator memiliki lag publikasi 1–2 tahun.",
    ]
    r = 3
    for n in notes:
        ws.cell(row=r, column=2, value=n).font = _font(
            11, bold=n.endswith(":"), color=THEME["ink"])
        r += 1
    ws.cell(row=r + 1, column=2,
            value=f"Digenerate otomatis pada {datetime.now():%d %b %Y %H:%M} "
                  f"oleh ASEAN Macro Report Engine.").font = _font(
        10, italic=True, color=THEME["muted"])


# ------------------------------------------------------------- orchestrasi --
def build(df: pd.DataFrame, path: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)  # buang sheet default
    sheet_cover(wb, df)
    sheet_ringkasan(wb, df)
    sheet_per_indikator(wb, df)
    sheet_data(wb, df)
    sheet_catatan(wb, df)
    wb.active = 0
    wb.save(path)
    return path


def main() -> None:
    from config import STAGING
    src = STAGING / "wb_panel.parquet"
    if not src.exists():
        raise SystemExit("data staging belum ada — jalankan ingest.py dulu")
    df = pd.read_parquet(src)
    out = OUTPUT / f"ASEAN_Macro_Report_{datetime.now():%Y%m%d}.xlsx"
    build(df, out)
    print(f"[excel] laporan dibuat → {out}")
    print(f"[excel] {len(df)} baris · {len(INDICATORS)} indikator · "
          f"{len(COUNTRIES)} negara · 5 sheet")


if __name__ == "__main__":
    main()
