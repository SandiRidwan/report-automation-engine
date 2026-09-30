
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
        {
            "aksi": "Jadikan laporan ini basis briefing bulanan/kuartalan secara otomatis.",
            "langkah": [
                "Jalankan pipeline 6 negara ASEAN × 8 indikator (2015–2024, 480 observasi) dari World Bank sekali untuk baseline.",
                "Daftarkan jadwal berulang di scheduler tanpa dependensi: `scheduler.py --daily 06:00` (atau mingguan/bulanan).",
                "Sebarkan workbook 5 sheet yang dihasilkan ke pemangku kepentingan tiap siklus, tanpa entri ulang manual.",
            ],
            "metrik": "Ketersediaan laporan tepat jadwal (mis. ≥95% siklus terkirim tanpa penundaan).",
            "pemilik": "Analis data / operator scheduler.",
        },
        {
            "aksi": "Sesuaikan daftar negara/indikator cukup di config.py — tak perlu ubah kode.",
            "langkah": [
                "Buka `config.py`, ubah daftar negara atau indikator sesuai cakupan klien.",
                "Jalankan ulang pipeline; lembar Ringkasan, Per Indikator, dan Data ikut menyesuaikan otomatis.",
                "Jalankan 7 uji struktur laporan + 13 uji data untuk memastikan konfigurasi baru tidak merusak keluaran.",
            ],
            "metrik": "Tes: 7 uji struktur + 13 uji data lulus 100% tanpa menyentuh kode inti.",
            "pemilik": "Analis data (tanpa perlu engineer).",
        },
        {
            "aksi": "Kirim sheet 'Data' ke tim analis; sheet 'Ringkasan' ke manajemen.",
            "langkah": [
                "Bagi peran penerima: sheet Ringkasan (KPI berformat) untuk manajemen, sheet Data (mentah + autofilter) untuk tim analis.",
                "Tim analis menelusuri ulang angka pada sheet Data mentah saat ada pertanyaan.",
                "Cantumkan sheet Catatan (metodologi) agar batas jujur — USD nominal, revisi data, lag 1–2 tahun — terbaca jelas.",
            ],
            "metrik": "Waktu menjawab pertanyaan angka turun (mis. ≤1 hari kerja) & jumlah pertanyaan ulang menurun.",
            "pemilik": "Analis data (distribusi) & manajer (konsumsi).",
        },
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
        {
            "aksi": "Gunakan tab Cover untuk navigasi cepat (hyperlink antar-sheet).",
            "langkah": [
                "Klik hyperlink pada tab Cover untuk melompat ke Ringkasan, Per Indikator, Data, atau Catatan.",
                "Biasakan penerima mulai dari Cover agar alur baca 5 sheet konsisten.",
                "Perbarui tautan Cover bila struktur sheet berubah agar tidak menuju sel kosong.",
            ],
            "metrik": "Penerima menemukan sheet tujuan dalam ≤2 klik dari Cover.",
            "pemilik": "Penyusun laporan.",
        },
        {
            "aksi": "Sesuaikan warna brand di THEME (config.py) agar cocok identitas klien.",
            "langkah": [
                "Buka `config.py`, ubah palet pada `THEME` sesuai warna korporat klien.",
                "Regenerasi workbook; 8 grafik native Excel pada sheet Per Indikator mengikuti tema baru.",
                "Jalankan 7 uji struktur laporan untuk memastikan perubahan tema tidak merusak layout sheet.",
            ],
            "metrik": "Semua 5 sheet & 8 grafik konsisten dengan palet brand (tanpa warna default tertinggal).",
            "pemilik": "Desainer/analis laporan.",
        },
        {
            "aksi": "Pertahankan sheet Data — transparansi membangun kepercayaan klien.",
            "langkah": [
                "Cantumkan sheet Data (mentah 480 observasi + autofilter) pada setiap rilis, jangan dihapus.",
                "Aktifkan autofilter agar klien dapat menyaring per negara/indikator/tahun sendiri.",
                "Sertakan sheet Catatan yang menegaskan batas jujur: USD nominal (terpengaruh kurs), data dapat direvisi, lag publikasi 1–2 tahun.",
            ],
            "metrik": "Jumlah permintaan data mentah lanjutan dari klien menurun; audit klien dapat ditutup mandiri.",
            "pemilik": "Penyusun laporan.",
        },
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
        {
            "aksi": "Fokuskan analisis investasi pada indikator dengan pertumbuhan positif "
                    "konsisten (mis. digital).",
            "langkah": [
                "Urutkan indikator berdasarkan pertumbuhan 2015→2024 pada 6 negara ASEAN dari sheet Ringkasan/pipeline.",
                "Tandai indikator dengan tanda positif konsisten lintas-tahun sebagai kandidat prioritas investasi.",
                "Jadwalkan pemantauan ulang (`scheduler.py --daily 06:00` atau bulanan) agar tren positif terverifikasi berkelanjutan.",
            ],
            "metrik": "Jumlah indikator prioritas dengan pertumbuhan positif bertahan antar-siklus.",
            "pemilik": "Analis strategi / perencana investasi.",
        },
        {
            "aksi": "Selidiki indikator yang menyusut — bisa peluang masuk atau tanda risiko.",
            "langkah": [
                "Identifikasi indikator dengan pertumbuhan negatif 2015→2024 per negara dari hasil pipeline.",
                "Pisahkan penyebab struktural vs guncangan sementara dengan membaca data mentah sheet Data.",
                "Uji hipotesis 'peluang masuk' vs 'tanda risiko' dan catat di sheet Catatan agar diverifikasi periode berikutnya.",
            ],
            "metrik": "Jumlah indikator menyusut yang berhasil diklasifikasi (peluang/risiko) per siklus.",
            "pemilik": "Analis riset/risiko.",
        },
        {
            "aksi": "Gunakan pertumbuhan, bukan hanya angka absolut, untuk keputusan timing.",
            "langkah": [
                "Hitung laju pertumbuhan 2015→2024 tiap indikator, bukan hanya level absolutnya.",
                "Bandingkan ranking berdasarkan pertumbuhan vs absolut untuk menemukan perbedaan arah.",
                "Ambil keputusan timing masuk/keluar berbasis laju pertumbuhan, dengan sheet Data sebagai bukti pendukung.",
            ],
            "metrik": "Persentase keputusan yang memakai laju pertumbuhan (bukan absolut) sebagai dasar.",
            "pemilik": "Pengambil keputusan investasi.",
        },
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
        {
            "aksi": "Identifikasi kategori terlemah per negara — prioritas kebijakan.",
            "langkah": [
                "Petakan profil kategori (Ukuran Ekonomi, Kesejahteraan, Digital, dll) per negara dari sheet Ringkasan.",
                "Tandai kategori dengan skor terendah untuk tiap negara sebagai prioritas kebijakan.",
                "Sertakan temuan di sheet Catatan/Per Indikator agar dasar prioritas dapat diaudit.",
            ],
            "metrik": "Jumlah negara dengan kategori terlemah teridentifikasi & ditindaklanjuti.",
            "pemilik": "Analis kebijakan / perencana.",
        },
        {
            "aksi": "Bandingkan antar-negara dalam kategori sama untuk menemukan best practice.",
            "langkah": [
                "Pilih satu kategori (mis. Digital), lalu bandingkan 6 negara ASEAN pada kategori itu.",
                "Angkat negara dengan kinerja terbaik sebagai sumber best practice yang dapat direplikasi.",
                "Verifikasi bahwa keunggulan bersumber dari data mentah (sheet Data), bukan artefak agregasi.",
            ],
            "metrik": "Jumlah best practice terdokumentasi per kategori per siklus laporan.",
            "pemilik": "Analis benchmarking regional.",
        },
        {
            "aksi": "Pantau pergeseran kategori dari waktu ke waktu via penjadwalan laporan.",
            "langkah": [
                "Jalankan pipeline berulang via `scheduler.py --daily 06:00` (atau mingguan/bulanan).",
                "Bandingkan profil kategori antar-periode untuk mendeteksi pergeseran.",
                "Simpan snapshot tiap siklus agar tren pergeseran dapat dilacak.",
            ],
            "metrik": "Frekuensi deteksi pergeseran kategori per periode (target: tiap siklus tercatat).",
            "pemilik": "Analis data / operator scheduler.",
        },
    ],
    risiko=(
        "Tanpa pembandingan kategori, kesimpulan bisa terlalu umum ('negara X "
        "lebih maju') tanpa arah tindakan konkret tentang AREA mana yang perlu "
        "diperbaiki."),
    tingkat="sedang",
)


# --------------------------------------------------------------------------
# Chart ECharts (v2) — insight & rekomendasi.
# --------------------------------------------------------------------------

register(
    "echarts_waterfall",
    kesimpulan=(
        "Waterfall memecah TOTAL pertumbuhan agregat menjadi KONTRIBUSI tiap "
        "negara: bar hijau = pendorong, merah = penahan, biru = total. Ini "
        "menjawab 'siapa yang mengangkat/menahan angka ini' — jauh lebih berguna "
        "daripada satu angka rata-rata ASEAN untuk keputusan alokasi."),
    rekomendasi=[
        {
            "aksi": "Identifikasi negara pendorong utama untuk dijadikan studi kasus "
                    "kebijakan yang bisa direplikasi.",
            "langkah": [
                "Baca waterfall: bar hijau (pendorong) vs merah (penahan) vs biru (total) untuk memecah kontribusi tiap negara.",
                "Pilih negara dengan kontribusi positif terbesar sebagai kandidat studi kasus.",
                "Telusuri angka sumber di sheet Data agar kebijakan yang direplikasi berbasis bukti, bukan agregat ASEAN.",
            ],
            "metrik": "Jumlah studi kasus kebijakan terbentuk dari negara pendorong utama (mis. ≥1 per siklus).",
            "pemilik": "Analis kebijakan regional.",
        },
        {
            "aksi": "Selidiki negara ber-kontribusi negatif: apakah masalah struktural atau "
                    "guncangan sementara.",
            "langkah": [
                "Sorot bar merah pada waterfall sebagai negara ber-kontribusi negatif.",
                "Bandingkan pola lintas-tahun (2015–2024) untuk memisahkan struktural vs guncangan sementara.",
                "Catat klasifikasi beserta bukti dari sheet Data mentah untuk verifikasi periode berikutnya.",
            ],
            "metrik": "Jumlah negara ber-kontribusi negatif yang terklasifikasi (struktural/sementara).",
            "pemilik": "Analis risiko regional.",
        },
        {
            "aksi": "Sajikan waterfall dalam laporan agar pemangku kepentingan melihat "
                    "sumber pertumbuhan, bukan hanya totalnya.",
            "langkah": [
                "Sematkan waterfall pada sheet Ringkasan/Per Indikator sebagai grafik native Excel.",
                "Tunjukkan pemecahan kontribusi per negara di samping angka total agregat.",
                "Jadwalkan penyegaran laporan (`scheduler.py --daily 06:00`) agar waterfall selalu mutakhir saat disajikan.",
            ],
            "metrik": "Persentase sesi briefing yang membahas kontribusi per negara, bukan hanya total.",
            "pemilik": "Penyusun laporan / penyaji.",
        },
    ],
    risiko=(
        "Melaporkan hanya total pertumbuhan menyembunyikan divergensi antar-"
        "negara. Kebijakan berbasis agregat bisa mengabaikan negara yang "
        "tertinggal, memperlebar ketimpangan regional."),
    tingkat="sedang",
)

register(
    "echarts_pictorial",
    kesimpulan=(
        "Bar bertitik menampilkan rata-rata indikator per negara sebagai blok "
        "visual — ringkas untuk laporan eksekutif. Pesannya tetap sama: "
        "kesenjangan antar-negara pada indikator ini nyata, dan skalanya (bukan "
        "hanya urutannya) menentukan besarnya celah yang harus ditutup."),
    rekomendasi=[
        {
            "aksi": "Gunakan perbandingan visual ini sebagai pembuka diskusi alokasi, lalu "
                    "dalami penyebabnya dengan metrik pendukung.",
            "langkah": [
                "Tampilkan bar bertitik rata-rata indikator per negara sebagai pembuka sesi alokasi.",
                "Untuk negara dengan celah besar, dalami penyebabnya dengan metrik pendukung pada sheet Per Indikator.",
                "Tutup diskusi dengan keputusan alokasi yang mengacu ke selisih nyata (skala), bukan hanya urutan.",
            ],
            "metrik": "Setiap sesi alokasi menghasilkan keputusan tertulis berbasis skala celah.",
            "pemilik": "Pemimpin rapat alokasi.",
        },
        {
            "aksi": "Perhatikan indikator dengan jurang terlebar antar-negara — di situ "
                    "kerja sama regional paling berdampak.",
            "langkah": [
                "Hitung selisih rata-rata antar-negara tiap indikator untuk menemukan jurang terlebar.",
                "Prioritaskan indikator berjurang terlebar sebagai fokus kerja sama regional.",
                "Verifikasi jurang pada sheet Data mentah sebelum mengusulkan program bersama.",
            ],
            "metrik": "Jumlah indikator berjurang terlebar yang masuk agenda kerja sama regional.",
            "pemilik": "Koordinator kerja sama regional.",
        },
        {
            "aksi": "Perbarui laporan berkala (scheduler sudah ada) untuk memantau "
                    "penyempitan/pelebaran celah.",
            "langkah": [
                "Jadwalkan pembaruan otomatis via `scheduler.py --daily 06:00` (atau mingguan/bulanan).",
                "Bandingkan jurang antar-negara antar-periode untuk melihat arah penyempitan/pelebaran.",
                "Perhatikan batas jujur saat menafsirkan tren: USD nominal (terpengaruh kurs), data dapat direvisi, lag publikasi 1–2 tahun.",
            ],
            "metrik": "Tren lebar celah terpantau tiap periode dengan catatan keterbatasan data.",
            "pemilik": "Analis data / operator scheduler.",
        },
    ],
    risiko=(
        "Menampilkan rata-rata saja menyembunyikan distribusi internal tiap "
        "negara. Untuk indikator seperti populasi, rata-rata antar-negara "
        "mudah disalahartikan sebagai 'ukuran tipikal' bila skala tak dibaca "
        "hati-hati."),
    tingkat="rendah",
)
