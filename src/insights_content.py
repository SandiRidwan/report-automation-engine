
# ---------------------------------------------------------------------------
# KONTEN INSIGHT — Report Automation Engine
# Sudut pandang: analis yang menyerahkan laporan ke klien bisnis/pemerintah.
# ---------------------------------------------------------------------------
from insight import register

register(
    "kpi",
    kesimpulan=(
        "Laporan mencakup 6 negara ASEAN, 8 indikator ekonomi, 2015–2024 "
        "(480 observasi) dari World Bank. Ini snapshot lengkap untuk analisis "
        "lintas-negara tanpa perlu mengumpulkan data manual."),
    rekomendasi=[
        "Jadikan laporan ini basis briefing bulanan/kuartalan secara otomatis.",
        "Sesuaikan daftar negara/indikator cukup di config.py — tak perlu ubah kode.",
        "Kirim sheet 'Data' ke tim analis; sheet 'Ringkasan' ke manajemen.",
    ],
    risiko=(
        "Laporan yang dibuat manual berulang rawan inkonsistensi & human error "
        "(angka tertukar, format beda). Otomasi menghilangkan seluruh kelas "
        "kesalahan itu dan menghemat jam kerja per siklus."),
    tingkat="sedang",
)

register(
    "report",
    kesimpulan=(
        "Workbook 5 sheet siap kirim: Cover (navigasi), Ringkasan (KPI berformat), "
        "Per Indikator (8 grafik native Excel), Data (mentah + autofilter), "
        "Catatan (metodologi). Formula & grafik dapat diedit penerima."),
    rekomendasi=[
        "Gunakan tab Cover untuk navigasi cepat (hyperlink antar-sheet).",
        "Sesuaikan warna brand di THEME (config.py) agar cocok identitas klien.",
        "Pertahankan sheet Data — transparansi membangun kepercayaan klien.",
    ],
    risiko=(
        "Laporan tanpa sheet data mentah memaksa klien mempercayai angka buta. "
        "Menyertakan data mentah memungkinkan audit & meningkatkan kredibilitas "
        "— sekaligus mengurangi pertanyaan lanjutan."),
    tingkat="sedang",
)

register(
    "growth",
    kesimpulan=(
        "Pertumbuhan 2015→2024 per indikator mengungkap arah tiap ekonomi. "
        "Kategori digital umumnya tumbuh paling cepat, sementara indikator "
        "struktural (ekspor % GDP) lebih datar."),
    rekomendasi=[
        "Fokuskan analisis investasi pada indikator dengan pertumbuhan positif "
        "konsisten (mis. digital).",
        "Selidiki indikator yang menyusut — bisa peluang masuk atau tanda risiko.",
        "Gunakan pertumbuhan, bukan hanya angka absolut, untuk keputusan timing.",
    ],
    risiko=(
        "Membandingkan angka absolut antar-tahun tanpa memperhitungkan "
        "pertumbuhan bisa menyesatkan; ekonomi yang 'besar' bisa sebenarnya "
        "melambat, sementara yang 'kecil' tumbuh cepat."),
    tingkat="tinggi",
)

register(
    "category",
    kesimpulan=(
        "Profil per kategori (Ukuran Ekonomi, Kesejahteraan, Digital, dll) "
        "menunjukkan kekuatan & kelemahan relatif tiap negara — dasar "
        "benchmarking regional."),
    rekomendasi=[
        "Identifikasi kategori terlemah per negara — prioritas kebijakan.",
        "Bandingkan antar-negara dalam kategori sama untuk menemukan best practice.",
        "Pantau pergeseran kategori dari waktu ke waktu via penjadwalan laporan.",
    ],
    risiko=(
        "Tanpa pembandingan kategori, kesimpulan bisa terlalu umum ('negara X "
        "lebih maju') tanpa arah tindakan konkret tentang AREA mana yang perlu "
        "diperbaiki."),
    tingkat="sedang",
)
