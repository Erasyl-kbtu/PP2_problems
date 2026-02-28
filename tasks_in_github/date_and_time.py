from datetime import date, timedelta
from datetime import datetime

# вычитаем 5 дней из сегодня
result_date = date.today() - timedelta(days=5)

print(f"Сегодня: {date.today()}")
print(f"Пять дней назад было: {result_date}")

# вчера, сегодня, завтра

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Вчера: {yesterday}")
print(f"Сегодня: {today}")
print(f"Завтра: {tomorrow}")

# вычитаем микросекунды

dt_with_ms = datetime.now()
dt_no_ms = dt_with_ms.replace(microsecond=0)

print(f"С микросекундами: {dt_with_ms}")
print(f"Без микросекунд:   {dt_no_ms}")

# разница в секундах

date1 = datetime(2026, 2, 28, 12, 0, 0) 
date2 = datetime(2026, 2, 27, 12, 0, 0) 

difference = date1 - date2

print(f"Разница в секундах: {difference.total_seconds()}")