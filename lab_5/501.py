import re
txt = input()
x = re.search("^Hello", txt)
if x:
    print("Yes")
else:
    print("No")