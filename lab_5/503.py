import re
txt = input()
p = input()
x = re.findall(p, txt)
y = len(x)
print(y)
