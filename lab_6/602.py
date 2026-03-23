filename = "text.txt"

with open("text.txt", "a", encoding = "utf8") as file:
    a = input() 
    file.write(a)


numbers = list(map(int, input().split()))

result = list(filter(lambda x: x % 2 == 0, numbers))

print(len(result))