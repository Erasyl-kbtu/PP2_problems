from datetime import datetime, timedelta, timezone

def parse(dt_str):
    date, tz = dt_str.split(" UTC")
    dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    sign = 1 if tz[0] == "+" else -1
    h, m = map(int, tz[1:].split(":"))
    offset = timezone(sign * timedelta(hours=h, minutes=m))
    return dt.replace(tzinfo=offset)

start = parse(input().strip())
end = parse(input().strip())

duration = (end.astimezone(timezone.utc) - start.astimezone(timezone.utc)).total_seconds()

print(int(duration))
