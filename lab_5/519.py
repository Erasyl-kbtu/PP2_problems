import re

text = input()
p = re.compile(r'\b\w+\b')
x = p.findall(text)

print(len(x))