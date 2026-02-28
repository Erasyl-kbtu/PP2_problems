def squeres(n):
    for i in range(0, n + 1):
        yield i * i

n = int(input())
gen = squeres(n)

for val in gen:
    print(val, end = " ")