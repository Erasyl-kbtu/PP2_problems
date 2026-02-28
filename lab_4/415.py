from datetime import datetime, timedelta, timezone

def parse(dt_str):
    date, tz = dt_str.split(" UTC")
    y, m, d = map(int, date.split("-"))
    sign = 1 if tz[0] == "+" else -1
    h, mm = map(int, tz[1:].split(":"))
    offset = timezone(sign * timedelta(hours=h, minutes=mm))
    return datetime(y, m, d, tzinfo=offset)

birth = parse(input().strip())
current = parse(input().strip())

month, day = birth.month, birth.day
year = current.year

try:
    target = datetime(year, month, day, tzinfo=birth.tzinfo)
except ValueError:
    target = datetime(year, 2, 28, tzinfo=birth.tzinfo)

if target.astimezone(timezone.utc) < current.astimezone(timezone.utc):
    year += 1
    try:
        target = datetime(year, month, day, tzinfo=birth.tzinfo)
    except ValueError:
        target = datetime(year, 2, 28, tzinfo=birth.tzinfo)

delta = (target.astimezone(timezone.utc) - current.astimezone(timezone.utc)).total_seconds()

print(0 if delta == 0 else (int(delta // 86400) + (1 if delta % 86400 else 0)))
