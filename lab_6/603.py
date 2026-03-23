filename = "text.txt"

with open("text.txt", "a", encoding = "utf8") as file:
    a = input() 
    file.write(a)


numbers = list(map(str, input().split()))

for i, item in enumerate(numbers, start = 0):
    print(f"{i}:{item}", end = " " )