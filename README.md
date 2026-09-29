<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=32&duration=3000&pause=1000&color=1F5C3D&center=true&vCenter=true&width=940&height=70&lines=REPORT+AUTOMATION+ENGINE" alt="Report Automation Engine" />

![Python](https://img.shields.io/badge/Python-3.10+-1F5C3D?style=for-the-badge&logo=python&logoColor=white)
![openpyxl](https://img.shields.io/badge/openpyxl-Excel-E4A11B?style=for-the-badge)
![DuckDB](https://img.shields.io/badge/DuckDB-SQL-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-Preview-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

### 🔗 [**Buka Preview →**](https://report-automation-engine.streamlit.app)

</div>

---

## 📊 Apa ini?

**Mesin yang menghasilkan laporan Excel profesional secara otomatis** —
multi-sheet, berformat, dengan grafik native & formula yang dapat diaudit.

Studi kasus: **Laporan Makroekonomi ASEAN** dari World Bank —
6 negara × 8 indikator × 2015–2024 (480 observasi) → workbook siap kirim,
dapat **dijadwalkan** harian/mingguan/bulanan.

```bash
python src/run_pipeline.py        # unduh → marts → xlsx → validate → tests
python src/scheduler.py --daily 06:00   # laporan otomatis tiap pagi
streamlit run app/dashboard.py
```

---

## 🎯 Kenapa project ini berguna

Bukan sekadar dashboard visual — ini **deliverable yang dibeli klien**:
laporan Excel yang bisa langsung dikirim, di-edit, dan dipivot penerima.

| Fitur | Manfaat |
|---|---|
| **5 sheet terstruktur** | Cover (navigasi) · Ringkasan · Per Indikator · Data · Catatan |
| **8 grafik native Excel** | Dapat diedit penerima (bukan gambar) |
| **Format profesional** | Header brand, zebra striping, freeze pane, number format |
| **Auditable** | Sheet Data mentah + autofilter untuk verifikasi |
| **Terjadwal** | `scheduler.py` — tanpa dependensi eksternal |
| **Terkonfigurasi** | Ganti negara/indikator cukup di `config.py` |

---

## 🏗️ Arsitektur

```
 World Bank API ─► ingest.py ─► staging (Parquet)
                                    │
             build_marts.py ─► DuckDB ─► marts
                                    │
  build_excel.py ─► output/ASEAN_Macro_Report_YYYYMMDD.xlsx
                                    │
       scheduler.py ─► otomatis (harian/mingguan/bulanan)
                                    │
        validate.py · tests/ · dashboard.py
```

| Lapisan | File | Peran |
|---|---|---|
| **Ingest** | `src/ingest.py` | Unduh World Bank → Parquet (retry) |
| **Marts** | `src/build_marts.py` | DuckDB: latest, growth, kategori |
| **Excel engine** | `src/build_excel.py` | ★ 5 sheet + chart + format |
| **Jadwal** | `src/scheduler.py` | Cron-style harian/mingguan/bulanan |
| **Validasi** | `src/validate.py` | 7 uji struktur laporan |
| **Tests** | `tests/test_data_quality.py` | 13 uji data & laporan |
| **Preview** | `app/dashboard.py` | Streamlit + unduh Excel |

---

## 📈 Isi laporan Excel

| Sheet | Isi |
|---|---|
| **Cover** | Judul, metadata, tanggal, daftar isi (hyperlink) |
| **Ringkasan** | KPI per negara (GDP, GDP/kapita, populasi, pengangguran, inflasi, internet) |
| **Per Indikator** | Tabel pivot negara×tahun + **grafik garis native** per indikator |
| **Data** | Data mentah + autofilter (transparansi & pivot klien) |
| **Catatan** | Metodologi, sumber, keterbatasan jujur |

---

## ⚠️ Keterbatasan (jujur)

- **USD nominal** — perbandingan lintas negara terpengaruh kurs, bukan PPP.
- **Lag publikasi** — beberapa indikator World Bank tertinggal 1–2 tahun.
- **Data dapat direvisi** — laporan ini snapshot saat generate.
- **6 negara ASEAN** (Indonesia, Malaysia, Thailand, Vietnam, Filipina, Singapura).

> Laporan menyertakan sheet **Data** mentah agar penerima dapat mengaudit —
> transparansi yang membangun kepercayaan klien.

---

## 🧪 Kualitas

```
PASS  5 sheet        PASS  jumlah baris = sumber
PASS  8 chart        PASS  header berformat
PASS  freeze pane    PASS  13 uji data & laporan → SEMUA LULUS
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python src/run_pipeline.py     # ~3 menit (unduh World Bank)
# laporan ada di output/ASEAN_Macro_Report_YYYYMMDD.xlsx
streamlit run app/dashboard.py
```

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|---|---|
| **Data** | World Bank Open Data API |
| **Excel** | openpyxl (format, formula, chart native) |
| **Database** | DuckDB |
| **Otomasi** | scheduler kustom (tanpa dependensi) |
| **Preview** | Streamlit |
| **Tests** | uji kustom |

---

<!-- INSIGHTS:START -->
## 💡 Insight & Rekomendasi (per analisis)

_Setiap analisis disertai kesimpulan, rekomendasi tindakan, dan risiko bila diabaikan — bukan sekadar angka._

### 🟠 Growth
**Kesimpulan.** Pertumbuhan 2015→2024 per indikator mengungkap arah tiap ekonomi. Kategori digital umumnya tumbuh paling cepat, sementara indikator struktural (ekspor % GDP) lebih datar.

**Rekomendasi tindakan:**
- Fokuskan analisis investasi pada indikator dengan pertumbuhan positif konsisten (mis. digital).
- Selidiki indikator yang menyusut — bisa peluang masuk atau tanda risiko.
- Gunakan pertumbuhan, bukan hanya angka absolut, untuk keputusan timing.

**⚠️ Risiko bila diabaikan.** Membandingkan angka absolut antar-tahun tanpa memperhitungkan pertumbuhan bisa menyesatkan; ekonomi yang 'besar' bisa sebenarnya melambat, sementara yang 'kecil' tumbuh cepat.

### 🔵 KPI / Ringkasan
**Kesimpulan.** Laporan mencakup 6 negara ASEAN, 8 indikator ekonomi, 2015–2024 (480 observasi) dari World Bank. Ini snapshot lengkap untuk analisis lintas-negara tanpa perlu mengumpulkan data manual.

**Rekomendasi tindakan:**
- Jadikan laporan ini basis briefing bulanan/kuartalan secara otomatis.
- Sesuaikan daftar negara/indikator cukup di config.py — tak perlu ubah kode.
- Kirim sheet 'Data' ke tim analis; sheet 'Ringkasan' ke manajemen.

**⚠️ Risiko bila diabaikan.** Laporan yang dibuat manual berulang rawan inkonsistensi & human error (angka tertukar, format beda). Otomasi menghilangkan seluruh kelas kesalahan itu dan menghemat jam kerja per siklus.

### 🔵 Report
**Kesimpulan.** Workbook 5 sheet siap kirim: Cover (navigasi), Ringkasan (KPI berformat), Per Indikator (8 grafik native Excel), Data (mentah + autofilter), Catatan (metodologi). Formula & grafik dapat diedit penerima.

**Rekomendasi tindakan:**
- Gunakan tab Cover untuk navigasi cepat (hyperlink antar-sheet).
- Sesuaikan warna brand di THEME (config.py) agar cocok identitas klien.
- Pertahankan sheet Data — transparansi membangun kepercayaan klien.

**⚠️ Risiko bila diabaikan.** Laporan tanpa sheet data mentah memaksa klien mempercayai angka buta. Menyertakan data mentah memungkinkan audit & meningkatkan kredibilitas — sekaligus mengurangi pertanyaan lanjutan.

### 🔵 Category
**Kesimpulan.** Profil per kategori (Ukuran Ekonomi, Kesejahteraan, Digital, dll) menunjukkan kekuatan & kelemahan relatif tiap negara — dasar benchmarking regional.

**Rekomendasi tindakan:**
- Identifikasi kategori terlemah per negara — prioritas kebijakan.
- Bandingkan antar-negara dalam kategori sama untuk menemukan best practice.
- Pantau pergeseran kategori dari waktu ke waktu via penjadwalan laporan.

**⚠️ Risiko bila diabaikan.** Tanpa pembandingan kategori, kesimpulan bisa terlalu umum ('negara X lebih maju') tanpa arah tindakan konkret tentang AREA mana yang perlu diperbaiki.

<!-- INSIGHTS:END -->

## 👤 Author

<div align="center">

**Sandi Ridwan** — Data Analyst · Automation Architect · Python

📍 Palu, Central Sulawesi, Indonesia

[![Upwork](https://img.shields.io/badge/Upwork-Hire_Me-6A4C93?style=for-the-badge&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~011f6d0fbb4a372974)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sandi-ridwan)

</div>

## 📄 License

MIT — Educational & portfolio. Data © World Bank (CC BY 4.0).
