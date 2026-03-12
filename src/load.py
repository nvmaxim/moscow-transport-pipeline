import duckdb

# Подключаемся к базе (если файла нет, он создастся)
con = duckdb.connect("data/transport.db")

# Создаем таблицу прямо из CSV-файла

tables = ["agency", "calendar", "routes", "stop_times", "stops", "trips"]
for t in tables:
    con.execute(
        f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('data/gtfs/{t}.txt')"
    )

# Показать все таблицы в базе
print(con.execute("SHOW TABLES").fetchall())

# Быстрая проверка каждой таблицы
for t in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {count} строк")
