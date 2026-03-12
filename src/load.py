import duckdb

# Подключаемся к базе (если файла нет, он создастся)
con = duckdb.connect("data/transport.db")

# Создаем таблицу прямо из CSV-файла
# con.execute("CREATE TABLE stops AS SELECT * FROM read_csv_auto('data/gtfs/stops.txt')")

# Делаем быстрый запрос
# print(con.execute("SELECT stop_name FROM stops LIMIT 5").fetchall())

result = con.execute("SELECT DISTINCT COUNT(*) FROM stops").fetchone()
print(f"Всего остановок: {result[0]}")
