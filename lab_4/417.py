import math

def dist(x, y):
    return math.hypot(x, y)

def radar_coverage(R, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    seg_len2 = dx*dx + dy*dy

    a = seg_len2
    b = 2*(x1*dx + y1*dy)
    c = x1*x1 + y1*y1 - R*R

    disc = b*b - 4*a*c
    ts = []
    if disc >= 0:
        sqrt_disc = math.sqrt(disc)
        t1 = (-b - sqrt_disc) / (2*a)
        t2 = (-b + sqrt_disc) / (2*a)
        ts = [t1, t2]

    points = []
    for t in ts:
        if 0 <= t <= 1:
            points.append((x1 + t*dx, y1 + t*dy))

    inside1 = dist(x1, y1) <= R + 1e-9
    inside2 = dist(x2, y2) <= R + 1e-9

    if inside1 and inside2:
        return math.sqrt(seg_len2) 
    elif not points:
        return 0.0 
    elif inside1 and not inside2:
        px, py = points[0]
        return math.hypot(px - x1, py - y1)
    elif inside2 and not inside1:
        px, py = points[0]
        return math.hypot(px - x2, py - y2)
    else:
        (px1, py1), (px2, py2) = points
        return math.hypot(px2 - px1, py2 - py1)


R = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

print(f"{radar_coverage(R, x1, y1, x2, y2):.10f}")
