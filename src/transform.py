# Топ-10 самых загруженных остановок с названиями
import duckdb

# Подключаемся к базе (если файла нет, он создастся)
con = duckdb.connect("data/transport.db")

# количество заездов всех маршрутов на все остановки с таким названием за весь период расписания
result = con.execute(
    """
    SELECT 
        s.stop_name,
        COUNT(*) as visits
    FROM stop_times st
    JOIN stops s ON st.stop_id = s.stop_id
    GROUP BY s.stop_name
    ORDER BY visits DESC
    LIMIT 10
"""
).fetchall()

# for row in result:
#     print(f"{row[0]}: {row[1]:,}")


# . Самые загруженные маршруты

result = con.execute(
    """
SELECT 
r.route_short_name,  r.route_long_name,
COUNT(st.stop_id) as total_stops
FROM routes r
JOIN trips t ON r.route_id = t.route_id
JOIN stop_times st ON t.trip_id = st.trip_id
GROUP BY r.route_short_name, r.route_long_name
ORDER BY total_stops DESC
LIMIT 10
"""
).fetchall()

# for row in result:
#     print(f"{row[0]} - {row[1]}: {row[2]} загруженность по остановкам")

# Час пик (Временной анализ)
result = con.execute(
    """
    SELECT 
        -- Берем подстроку до первого двоеточия и превращаем в целое число
        -- А затем применяем % 24, чтобы 24 превратилось в 0, 25 в 1 и т.д.
        (CAST(split_part(arrival_time, ':', 1) AS INTEGER) % 24) as arrival_hour,
        COUNT(*) as num_buses
    FROM stop_times
    GROUP BY arrival_hour
    ORDER BY arrival_hour
"""
).fetchall()

for row in result:
    print(f"Час {row[0]:02d}: {row[1]:,d} прибытий")

# 3. Количество маршрутов на одной остановке

result = con.execute(
    """
SELECT 
    s.stop_name, 
    COUNT(DISTINCT t.route_id) as unique_routes
FROM stops s
JOIN stop_times st ON s.stop_id = st.stop_id
JOIN trips t ON st.trip_id = t.trip_id
GROUP BY s.stop_name
ORDER BY unique_routes DESC
LIMIT 10
"""
).fetchall()


# for row in result:
#     # row[0] это stop_name (строка), row[1] это unique_routes (число)
#     print(f"Остановка: {row[0]}, Маршрутов: {row[1]:,d}")
