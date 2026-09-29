"""
scheduler.py — penjadwalan laporan (cron-style, tanpa dependensi).

Menjalankan pipeline laporan pada jadwal harian/mingguan/bulanan, atau sekali.
Reproducible & portabel (tidak butuh library eksternal).

Pemakaian:
  python src/scheduler.py --once                 # generate sekali
  python src/scheduler.py --daily 06:00          # tiap hari jam 06:00
  python src/scheduler.py --weekly mon 06:00     # tiap Senin 06:00
  python src/scheduler.py --monthly 1 06:00      # tiap tgl-1 jam 06:00
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent


def run_report() -> bool:
    """Jalankan ingest (bila perlu) lalu build Excel."""
    print(f"[sched] {datetime.now():%Y-%m-%d %H:%M:%S} — generate laporan")
    for step in ["ingest.py", "build_excel.py"]:
        r = subprocess.run([sys.executable, str(SRC / step)], cwd=str(ROOT))
        if r.returncode != 0:
            print(f"[sched] GAGAL di {step}")
            return False
    print("[sched] selesai")
    return True


def _next_daily(hh: int, mm: int) -> datetime:
    now = datetime.now()
    t = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    return t if t > now else t + timedelta(days=1)


def _next_weekly(day: str, hh: int, mm: int) -> datetime:
    days = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
    target = days.get(day.lower(), 0)
    now = datetime.now()
    t = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    delta = (target - now.weekday()) % 7
    if delta == 0 and t <= now:
        delta = 7
    return t + timedelta(days=delta)


def _next_monthly(day: int, hh: int, mm: int) -> datetime:
    now = datetime.now()
    y, m = now.year, now.month
    t = datetime(y, m, min(day, 28), hh, mm)
    if t <= now:
        m = m + 1 if m < 12 else 1
        y = y if m > 1 else y + 1
        t = datetime(y, m, min(day, 28), hh, mm)
    return t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="generate sekali lalu keluar")
    ap.add_argument("--daily", nargs=1, metavar="HH:MM")
    ap.add_argument("--weekly", nargs=2, metavar=("DAY", "HH:MM"))
    ap.add_argument("--monthly", nargs=2, metavar=("DAY", "HH:MM"))
    args = ap.parse_args()

    if args.once or not (args.daily or args.weekly or args.monthly):
        return 0 if run_report() else 1

    def parse_hm(s: str) -> tuple[int, int]:
        h, m = s.split(":")
        return int(h), int(m)

    if args.daily:
        hh, mm = parse_hm(args.daily[0])
        print(f"[sched] mode HARIAN @ {hh:02d}:{mm:02d}")
        nxt = lambda: _next_daily(hh, mm)
    elif args.weekly:
        day = args.weekly[0]
        hh, mm = parse_hm(args.weekly[1])
        print(f"[sched] mode MINGGUAN @ {day} {hh:02d}:{mm:02d}")
        nxt = lambda: _next_weekly(day, hh, mm)
    else:
        d = int(args.monthly[0])
        hh, mm = parse_hm(args.monthly[1])
        print(f"[sched] mode BULANAN @ tgl-{d} {hh:02d}:{mm:02d}")
        nxt = lambda: _next_monthly(d, hh, mm)

    print("[sched] Ctrl+C untuk berhenti.")
    while True:
        target = nxt()
        wait = (target - datetime.now()).total_seconds()
        print(f"[sched] laporan berikutnya: {target:%Y-%m-%d %H:%M} "
              f"({wait/3600:.1f} jam)")
        try:
            time.sleep(max(1, wait))
        except KeyboardInterrupt:
            print("\n[sched] dihentikan.")
            return 0
        run_report()


if __name__ == "__main__":
    raise SystemExit(main())
