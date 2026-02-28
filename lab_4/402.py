def even_generator(n):
    for i in range(0, n + 1, 2):
        yield str(i)

try:
    n = int(input())
    gen = even_generator(n)

    # Берем первое число отдельно, чтобы не ставить запятую перед ним
    first = next(gen, None)
    if first is not None:
        print(first, end="")
        # Все остальные числа печатаем с запятой перед ними
        for val in gen:
            print(",", val, sep = "", end = "")
    
except ValueError:
    print("idi v pen")