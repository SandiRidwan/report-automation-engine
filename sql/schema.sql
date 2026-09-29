-- schema.sql — marts ringkas untuk dashboard preview & validasi.

CREATE TABLE IF NOT EXISTS mart_latest (
    country     VARCHAR,
    indicator   VARCHAR,
    category    VARCHAR,
    unit        VARCHAR,
    year        INTEGER,
    value       DOUBLE
);

CREATE TABLE IF NOT EXISTS mart_growth (
    country     VARCHAR,
    indicator   VARCHAR,
    y0          INTEGER,
    y1          INTEGER,
    v0          DOUBLE,
    v1          DOUBLE,
    growth_pct  DOUBLE
);

CREATE TABLE IF NOT EXISTS mart_category_avg (
    country     VARCHAR,
    category    VARCHAR,
    avg_value   DOUBLE,
    n           INTEGER
);
