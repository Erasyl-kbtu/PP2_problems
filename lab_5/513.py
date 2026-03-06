import re

txt = input()
x = re.findall(r"\w+", txt)
print(len(x))