def count(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())

for num in count(n):
    print(num)
