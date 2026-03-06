import re
txt = input()
p = input()
x = re.search(p, txt)
if x:
    print("Yes")
else:
    print("No")