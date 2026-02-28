from datetime import datetime, timedelta, timezone

def parse_datetime(dt_str):
    date_str, tz_str = dt_str.split(" UTC")
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    sign = 1 if tz_str[0] == "+" else -1
    hours, minutes = map(int, tz_str[1:].split(":"))
    offset = timezone(sign * timedelta(hours=hours, minutes=minutes))
    return datetime(dt.year, dt.month, dt.day, 0, 0, 0, tzinfo=offset)

dt1 = parse_datetime(input().strip())
dt2 = parse_datetime(input().strip())

diff_seconds = abs((dt1.astimezone(timezone.utc) - dt2.astimezone(timezone.utc)).total_seconds())

print(int(diff_seconds // 86400))
