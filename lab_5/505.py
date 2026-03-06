import re
txt = input()
x = re.findall("^[A-Za-z].*[0-9]$", txt)
if x:
    print("Yes")
else:
    print("No")