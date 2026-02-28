def mirror_reflection(x1, y1, x2, y2):
    x2_ref, y2_ref = x2, -y2

    if x2_ref == x1:  
        x = x1
    else:
        slope = (y2_ref - y1) / (x2_ref - x1)
        x = x1 - y1 / slope
    return x, 0.0

x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

x, y = mirror_reflection(x1, y1, x2, y2)
print(f"{x:.10f} {y:.10f}")
