import re

S = input()
P = input()

escape = re.escape(P)
x = re.findall(escape, S)

print(len(x))