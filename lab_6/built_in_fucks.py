#using map and filter functions
numbers = [1, 2, 3, 4, 5, 6]
squared = list(map(lambda x: x**2, numbers)) 
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Squared:", squared)
print("Evens:", evens)

#using reduce function
from functools import reduce            
product = reduce(lambda x, y: x * y, numbers)
print("Product:", product)

#using enumerate function
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("\nScoreboard:")


zipped = list(zip(names, scores))
for name, score in zipped:
    print(f"{name}: {score}")

zipped.sort(key=lambda x: x[1], reverse=True)

print("Rankings:")
for index, (name, score) in enumerate(zipped, start=1):
    print(f"{index}. {name}: {score}")