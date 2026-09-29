"""
dashboard.py — Streamlit: preview laporan & unduh Excel.

Menampilkan ringkasan (KPI, pertumbuhan, kategori) sebagai PREVIEW, plus
tombol UNDUH laporan Excel yang di-generate otomatis. Setiap elemen disertai
narasi Kenapa-Tujuan-Dampak & kotak Insight.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from config import COLORS as C, DB_FILE, MARTS, OUTPUT, THEME  # noqa: E402
import explanations as X  # noqa: E402
import insights_content  # noqa: E402,F401
import insight as INS  # noqa: E402
import echarts_charts as EC  # noqa: E402  (waterfall, pictorialBar)

st.set_page_config(page_title="Report Automation Engine", page_icon="📊",
                   layout="wide")

PLOT_COLORS = {"primary": "#1F5C3D", "accent": "#E4A11B", "blue": "#2E6F95",
               "red": "#C0392B", "purple": "#6A4C93", "teal": "#2A9D8F"}


def _src():
    if DB_FILE.exists():
        return "db"
    if (MARTS / "mart_latest.parquet").exists():
        return "marts"
    return "none"


_S = _src()
if _S == "none":
    st.error("Data belum ada. Jalankan: `python src/run_pipeline.py`")
    st.stop()


@st.cache_data(show_spinner="Membaca data...")
def q(name: str) -> pd.DataFrame:
    if _S == "db":
        con = duckdb.connect(str(DB_FILE), read_only=True)
        df = con.execute(f"SELECT * FROM {name}").df()
        con.close()
        return df
    p = MARTS / f"{name}.parquet"
    return pd.read_parquet(p) if p.exists() else pd.DataFrame()


def style(fig, h=420):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=54, b=10),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#D5DBE1"),
                      title=dict(font=dict(size=16, color="#fff")),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor="#2A3038", zeroline=False)
    fig.update_yaxes(gridcolor="#2A3038", zeroline=False)
    return fig


def kpi(col, label, value, sub, color):
    col.markdown(
        f"""<div style="background:#1A1F2B;border-left:4px solid {color};
        padding:14px 16px;border-radius:10px;height:118px;">
        <div style="color:#9AA7B4;font-size:.76rem;text-transform:uppercase;
        letter-spacing:.06em;">{label}</div>
        <div style="color:{color};font-size:1.55rem;font-weight:700;
        margin-top:6px;">{value}</div>
        <div style="color:#6B7885;font-size:.75rem;">{sub}</div></div>""",
        unsafe_allow_html=True)


latest = q("mart_latest")
growth = q("mart_growth")
cats = q("mart_category_avg")

st.markdown(
    f"""<div style="background:linear-gradient(100deg,{C['primary']},{C['purple']});
    padding:22px 26px;border-radius:14px;margin-bottom:18px;">
    <div style="font-size:1.7rem;font-weight:800;color:white;">
    📊 Report Automation Engine</div>
    <div style="color:#D7E4DC;font-size:.9rem;margin-top:4px;">
    Laporan Excel multi-sheet otomatis dari data World Bank · by
    <b>Sandi Ridwan</b></div></div>""", unsafe_allow_html=True)

X.render("kpi", st=st)
n_ctry = latest["country"].nunique() if len(latest) else 0
n_ind = latest["indicator"].nunique() if len(latest) else 0
k1, k2, k3, k4 = st.columns(4)
kpi(k1, "Negara", f"{n_ctry}", "ASEAN", PLOT_COLORS["primary"])
kpi(k2, "Indikator", f"{n_ind}", "ekonomi makro", PLOT_COLORS["accent"])
kpi(k3, "Periode", "2015–2024", "10 tahun", PLOT_COLORS["blue"])
kpi(k4, "Sheet Excel", "5", "siap kirim", PLOT_COLORS["purple"])
INS.box("kpi", st=st)

# ---- tombol unduh laporan ------------------------------------------------
st.markdown("### 📥 Unduh Laporan Excel")
X.render("report", st=st)
files = sorted(glob.glob(str(OUTPUT / "*.xlsx")))
if files:
    p = Path(files[-1])
    st.download_button(
        f"⬇️ Unduh {p.name} ({p.stat().st_size/1024:.0f} KB)",
        data=p.read_bytes(),
        file_name=p.name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.caption("Laporan di-generate otomatis: 5 sheet, 8 grafik native Excel, "
               "formula & format siap edit.")
else:
    st.info("Belum ada laporan. Jalankan: `python src/build_excel.py`")
INS.box("report", st=st)

t1, t2, t3 = st.tabs(["📈 Pertumbuhan", "🗂️ Kategori", "🔬 Metodologi"])

with t1:
    X.render("growth", st=st)
    g = growth.dropna(subset=["growth_pct"]).copy()
    sel = st.selectbox("Indikator", sorted(g["indicator"].unique()),
                       index=0)
    gs = g[g["indicator"] == sel].sort_values("growth_pct")
    fig = px.bar(gs, x="growth_pct", y="country", orientation="h",
                 color="growth_pct", color_continuous_scale="RdYlGn",
                 text=gs["growth_pct"].round(1))
    fig.add_vline(x=0, line_dash="dash", line_color="#8B9AA6")
    style(fig, 420).update_layout(coloraxis_showscale=False,
                                  title=f"Pertumbuhan {sel} (2015→2024, %)",
                                  xaxis_title="%", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
    INS.box("growth", st=st)

    st.markdown("#### Dekomposisi kontribusi pertumbuhan (waterfall ECharts)")
    st.caption("Waterfall memecah **total pertumbuhan agregat** menjadi "
               "kontribusi tiap negara, lalu menutup dengan total. Menjawab "
               "'siapa yang mengangkat/menahan angka ini?' — jauh lebih "
               "informatif dari bar biasa.")
    try:
        _g = g[g["indicator"] == sel].dropna(subset=["growth_pct"]).copy()
        if len(_g):
            _g = _g.sort_values("growth_pct", ascending=False)
            _contrib = (_g["growth_pct"] / len(_g)).round(2).tolist()
            _cats = list(_g["country"]) + ["Total (rata-rata)"]
            _vals = _contrib + [0.0]
            EC.waterfall(_cats, _vals,
                         title=f"Kontribusi negara ke pertumbuhan {sel} (%)",
                         yname="kontribusi (%)", height=460)
    except Exception as _e:  # noqa: BLE001
        st.caption(f"waterfall tak tersedia ({_e}).")
    INS.box("echarts_waterfall", st=st)

with t2:
    X.render("category", st=st)
    cat_sel = st.selectbox("Kategori", sorted(cats["category"].unique()))
    cs = cats[cats["category"] == cat_sel].sort_values("avg_value",
                                                       ascending=False)
    fig = px.bar(cs, x="country", y="avg_value", color="avg_value",
                 color_continuous_scale="Blues", text=cs["avg_value"].round(0))
    style(fig, 420).update_layout(coloraxis_showscale=False,
                                  title=f"Rata-rata: {cat_sel}",
                                  xaxis_title="", yaxis_title="nilai")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(cats, use_container_width=True, hide_index=True)
    INS.box("category", st=st)

    st.markdown("#### Perbandingan negara — bar bertitik (pictorialBar ECharts)")
    st.caption("PictorialBar menyajikan nilai rata-rata kategori per negara "
               "sebagai **blok bertitik** — tampilan ringkas yang cocok untuk "
               "laporan eksekutif, pesan tetap jelas: negara mana yang tertinggi.")
    try:
        _cs = cs.sort_values("avg_value", ascending=False)
        EC.pictorial_bar(
            categories=[str(c)[:14] for c in _cs["country"]],
            values=[float(v) for v in _cs["avg_value"]],
            symbol="rect", title=f"Rata-rata {cat_sel} per negara",
            yname="nilai", height=420)
    except Exception as _e:  # noqa: BLE001
        st.caption(f"pictorialBar tak tersedia ({_e}).")
    INS.box("echarts_pictorial", st=st)

with t3:
    X.render("method", st=st)
    st.markdown("#### Alur otomasi")
    st.code("""
 World Bank API ─► ingest.py ─► staging (Parquet)
                                     │
              build_marts.py ─► DuckDB ─► marts
                                     │
   build_excel.py ─► output/ASEAN_Macro_Report_YYYYMMDD.xlsx
                                     │
        scheduler.py (harian/mingguan/bulanan) ─► otomatis
    """, language="text")
    st.markdown(
        "- **Sumber:** World Bank Open Data (publik, tanpa kredensial).\n"
        "- **Otomasi:** `scheduler.py --daily 06:00` menghasilkan laporan tiap "
        "pagi tanpa intervensi.\n"
        "- **Konfigurasi:** ubah negara/indikator cukup di `config.py`.\n"
        "- **Validasi:** 7 uji struktur laporan + 13 uji data.\n"
        "- **Batas jujur:** USD nominal (terpengaruh kurs); data dapat direvisi; "
        "lag publikasi 1–2 tahun.")

st.markdown(
    f"""<hr style="border-color:#2A3038;">
    <div style="color:#8B9AA6;font-size:.8rem;text-align:center;">
    📊 Report Automation Engine · World Bank Open Data · python + openpyxl +
    DuckDB · oleh <b>Sandi Ridwan</b><br>
    Analisis edukasional. Laporan Excel siap kirim ke klien.</div>""",
    unsafe_allow_html=True)
