"""
build_marts.py — bangun marts DuckDB dari panel World Bank (untuk dashboard).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import duckdb

from config import DB_FILE, MARTS, STAGING

MARTS = [
    "mart_latest", "mart_growth", "mart_category_avg",
]


def main() -> None:
    panel = STAGING / "wb_panel.parquet"
    if not panel.exists():
        raise SystemExit("panel belum ada — jalankan ingest.py")
    con = duckdb.connect(str(DB_FILE))
    con.execute((Path(__file__).resolve().parent.parent / "sql" / "schema.sql")
                .read_text(encoding="utf-8"))

    con.execute("DROP TABLE IF EXISTS wb_panel")
    con.execute(f"""CREATE TABLE wb_panel AS
        SELECT * FROM read_parquet('{panel.as_posix()}')""")

    con.execute("DELETE FROM mart_latest")
    con.execute("""INSERT INTO mart_latest
        SELECT country, indicator, category, unit, year, value
        FROM wb_panel WHERE year = (SELECT max(year) FROM wb_panel)""")

    con.execute("DELETE FROM mart_growth")
    con.execute("""INSERT INTO mart_growth
        WITH mn AS (SELECT min(year) y0, max(year) y1 FROM wb_panel)
        SELECT a.country, a.indicator, a.year AS y0, b.year AS y1,
               a.value AS v0, b.value AS v1,
               CASE WHEN a.value <> 0
                    THEN round((b.value - a.value)/a.value*100, 2) END AS growth_pct
        FROM wb_panel a
        JOIN wb_panel b ON a.country = b.country
            AND a.indicator = b.indicator
            AND a.year = (SELECT y0 FROM mn) AND b.year = (SELECT y1 FROM mn)""")

    con.execute("DELETE FROM mart_category_avg")
    con.execute("""INSERT INTO mart_category_avg
        SELECT country, category, round(avg(value), 2) AS avg_value, count(*) n
        FROM wb_panel GROUP BY country, category""")

    for t in MARTS:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"[marts] {t:22} {n:5} baris")
        con.execute(f"""COPY {t} TO '{(MARTS_DIR := (Path(__file__).resolve().parent.parent / 'data' / 'marts') / (t + '.parquet')).as_posix()}'
            (FORMAT PARQUET)""")
    con.close()


if __name__ == "__main__":
    main()
