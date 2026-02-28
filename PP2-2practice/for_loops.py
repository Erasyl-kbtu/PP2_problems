#example 1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)

#example 2
for x in "banana":
  print(x)

#example 3
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  
#example 4
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)