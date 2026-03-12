import duckdb
from pathlib import Path

ROOT = Path().resolve().parent
con = duckdb.connect(
    "/home/nvmaxim/Projects/moscow-transport-pipeline/data/transport.db"
)

# Ограничиваем данные чтобы не было слишком много
limits = {
    "agency": 15,
    "routes": 60,
    "stops": 90,
    "trips": 90,
    "stop_times": 150,
    "calendar": 30,
}

output = []

for table, limit in limits.items():
    # Получаем структуру
    cols = con.execute(f"DESCRIBE {table}").fetchall()

    # CREATE TABLE
    col_defs = ", ".join([f"{c[0]} {c[1]}" for c in cols])
    output.append(f"CREATE TABLE {table} ({col_defs});")

    # INSERT INTO
    rows = con.execute(f"SELECT * FROM {table} LIMIT {limit}").fetchall()
    col_names = ", ".join([c[0] for c in cols])

    for row in rows:
        values = ", ".join(
            [
                (
                    "NULL"
                    if v is None
                    else (
                        f"'{str(v).replace(chr(39), chr(39)*2)}'"
                        if isinstance(v, str)
                        else str(v)
                    )
                )
                for v in row
            ]
        )
        output.append(f"INSERT INTO {table} ({col_names}) VALUES ({values});")

    output.append("")  # пустая строка между таблицами

# Сохраняем в файл
with open(
    "/home/nvmaxim/Projects/moscow-transport-pipeline/data/gtfs_sample.sql", "w"
) as f:
    f.write("\n".join(output))

print("Готово! Файл: gtfs_sample.sql")
print(f"Строк SQL: {len(output)}")
