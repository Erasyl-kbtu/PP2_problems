import re

x = re.findall(r"Name: (.*), Age: (.*)", input())
print(*x[0])