import math

def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def tangent_points(x, y, R):
    d = math.hypot(x, y)
    angle = math.atan2(y, x)
    alpha = math.acos(R / d)
    return [
        (R * math.cos(angle + alpha), R * math.sin(angle + alpha)),
        (R * math.cos(angle - alpha), R * math.sin(angle - alpha))
    ]

def shortest_path(R, x1, y1, x2, y2):
    # Если оба вне и отрезок не пересекает круг
    if dist(0, 0, x1, y1) >= R and dist(0, 0, x2, y2) >= R:
        # Проверим пересечение
        dx, dy = x2 - x1, y2 - y1
        a = dx*dx + dy*dy
        b = 2*(x1*dx + y1*dy)
        c = x1*x1 + y1*y1 - R*R
        disc = b*b - 4*a*c
        if disc < 0:
            return dist(x1, y1, x2, y2)

    # Иначе считаем путь через касательные
    tA = tangent_points(x1, y1, R)
    tB = tangent_points(x2, y2, R)

    best = float("inf")
    for xa, ya in tA:
        for xb, yb in tB:
            d1 = dist(x1, y1, xa, ya)
            d2 = dist(x2, y2, xb, yb)
            ang1 = math.atan2(ya, xa)
            ang2 = math.atan2(yb, xb)
            diff = abs(ang1 - ang2)
            diff = min(diff, 2*math.pi - diff)
            arc = R * diff
            best = min(best, d1 + arc + d2)
    return best

R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

print(f"{shortest_path(R, x1, y1, x2, y2):.10f}")
