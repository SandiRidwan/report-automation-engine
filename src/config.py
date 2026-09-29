"""
config.py — satu sumber kebenaran: path, sumber, gaya laporan, konstanta.

Project: ASEAN Macro Report Engine
Fokus: menghasilkan LAPORAN EXCEL multi-sheet profesional secara OTOMATIS
dari data World Bank — siap kirim ke klien (format, chart, formula, ringkasan).
"""

from __future__ import annotations

from pathlib import Path

# ---- Path -----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"
STAGING = DATA / "staging"
MARTS = DATA / "marts"
DB = ROOT / "db"
REPORTS = ROOT / "reports"
OUTPUT = ROOT / "output"

for _p in (RAW, STAGING, MARTS, DB, REPORTS, OUTPUT):
    _p.mkdir(parents=True, exist_ok=True)

DB_FILE = DB / "report.duckdb"

# ---- Sumber data (publik, tanpa API key) -----------------------------------
WB_BASE = "https://api.worldbank.org/v2"
COUNTRIES = {
    "IDN": "Indonesia", "MYS": "Malaysia", "THA": "Thailand",
    "VNM": "Vietnam", "PHL": "Philippines", "SGP": "Singapore",
}
INDICATORS = {
    "NY.GDP.MKTP.CD": {"nama": "GDP (US$)", "satuan": "US$", "kategori": "Ukuran Ekonomi"},
    "SP.POP.TOTL": {"nama": "Populasi", "satuan": "jiwa", "kategori": "Demografi"},
    "NY.GDP.PCAP.CD": {"nama": "GDP per Kapita", "satuan": "US$", "kategori": "Kesejahteraan"},
    "SL.UEM.TOTL.ZS": {"nama": "Pengangguran", "satuan": "%", "kategori": "Pasar Kerja"},
    "FP.CPI.TOTL.ZG": {"nama": "Inflasi", "satuan": "%", "kategori": "Harga"},
    "NE.EXP.GNFS.ZS": {"nama": "Ekspor", "satuan": "% GDP", "kategori": "Perdagangan"},
    "BX.KLT.DINV.CD.WD": {"nama": "FDI Masuk", "satuan": "US$", "kategori": "Investasi"},
    "IT.NET.USER.ZS": {"nama": "Pengguna Internet", "satuan": "%", "kategori": "Digital"},
}
YEAR_START, YEAR_END = 2015, 2024

# ---- Gaya laporan Excel ----------------------------------------------------
THEME = {
    "brand": "1F5C3D",        # hijau gelap (header)
    "accent": "E4A11B",       # kuning (sub-header/ aksen)
    "ink": "1B2A33",          # teks utama
    "muted": "8B9AA6",        # teks sekunder
    "band": "F2F5F7",         # baris zebra
    "pos": "2A9D8F",          # positif
    "neg": "C0392B",          # negatif
}
FONT = "Segoe UI"

REPORT_TITLE = "ASEAN Macroeconomic Report"
REPORT_SUBTITLE = "Key Indicators 2015–2024 · World Bank Open Data"
