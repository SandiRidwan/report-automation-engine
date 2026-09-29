"""explanations.py — narasi Kenapa · Tujuan · Dampak tiap elemen."""

from __future__ import annotations

EXPLAIN: dict[str, dict] = {
    "kpi": {
        "judul": "Ringkasan Laporan",
        "kenapa": "Klien butuh tahu laporan ini mencakup apa & seberapa baru.",
        "tujuan": "Menjawab: berapa negara, indikator, periode, baris data.",
        "dampak": "Menentukan cakupan keputusan yang bisa diambil dari laporan.",
        "baca": "Metadata ringkas dari workbook yang dihasilkan.",
    },
    "growth": {
        "judul": "Pertumbuhan Indikator (2015→2024)",
        "kenapa": "Angka absolut tak menunjukkan arah. Pertumbuhan menunjukkan "
                  "tren — ekonomi melejit atau stagnan?",
        "tujuan": "Menjawab: indikator mana yang tumbuh/menyusut per negara?",
        "dampak": "Arah investasi & prioritas kebijakan; deteksi stagnasi dini.",
        "baca": "% = perubahan dari tahun awal ke akhir pada indikator sama.",
    },
    "category": {
        "judul": "Profil per Kategori",
        "kenapa": "Mengelompokkan indikator ke kategori (ekonomi, demografi, "
                  "digital) memudahkan melihat kekuatan/kelemahan tiap negara.",
        "tujuan": "Menjawab: kategori mana yang menonjol per negara?",
        "dampak": "Menemukan area prioritas (mis. digital tertinggal).",
        "baca": "Rata-rata nilai per kategori; dibandingkan antar-negara.",
    },
    "report": {
        "judul": "Struktur Laporan Excel",
        "kenapa": "Deliverable harus siap kirim: terorganisir, berformat, "
                  "dapat diaudit. Itu yang dibeli klien, bukan sekadar angka.",
        "tujuan": "Menjelaskan isi 5 sheet & alasan masing-masing.",
        "dampak": "Laporan dapat langsung dipakai untuk presentasi/pengambilan "
                  "keputusan tanpa editing manual.",
        "baca": "Cover · Ringkasan · Per Indikator · Data · Catatan.",
    },
    "method": {
        "judul": "Metodologi & Otomasi",
        "kenapa": "Laporan harus reproducible & dapat dijadwalkan.",
        "tujuan": "Menjelaskan sumber data & cara generate/penjadwalan.",
        "dampak": "Dapat dijalankan otomatis (harian/mingguan) tanpa kerja manual.",
        "baca": "Lihat docs/ADR.md.",
    },
}


def text(key: str) -> str:
    e = EXPLAIN.get(key)
    if not e:
        return ""
    p = [f"**{e['judul']}**", f"- **Kenapa:** {e['kenapa']}",
         f"- **Tujuan:** {e['tujuan']}", f"- **Dampak:** {e['dampak']}"]
    if e.get("baca"):
        p.append(f"- **Cara baca:** {e['baca']}")
    return "\n".join(p)


def render(key: str, expanded: bool = False, st=None) -> None:
    if st is None:
        import streamlit as st  # noqa
    e = EXPLAIN.get(key)
    if not e:
        return
    with st.expander(f"💡 {e['judul']} — Kenapa · Tujuan · Dampak",
                     expanded=expanded):
        st.markdown(
            f"**🔎 Kenapa** — {e['kenapa']}\n\n"
            f"**🎯 Tujuan** — {e['tujuan']}\n\n"
            f"**📈 Dampak** — {e['dampak']}")
        if e.get("baca"):
            st.caption(f"👁️ Cara baca: {e['baca']}")


def audit(verbose: bool = True) -> bool:
    ok = True
    for k, v in EXPLAIN.items():
        miss = [f for f in ("kenapa", "tujuan", "dampak") if not v.get(f)]
        if miss:
            ok = False
            if verbose:
                print(f"  MISSING {k}: {miss}")
    if verbose:
        print(f"Penjelasan: {len(EXPLAIN)} | "
              f"{'SEMUA LENGKAP' if ok else 'ADA YANG KURANG'}")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if audit() else 1)
