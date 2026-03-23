filename = "text.txt"

with open("text.txt", "a", encoding = "utf8") as file:
    a = input() 
    file.write(a)


numbers = list(map(int, input().split()))

result = sum(map(lambda x: x**2, numbers))

print(result)