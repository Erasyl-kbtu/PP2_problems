import re

txt = input()
x = re.findall(r"[0-9]{2,}", txt)

for i in range(len(x)):
    print(x[i])