import re

txt = input()
x = re.findall(r"(\d{2}/\d{2}/\d{4})", txt)

print(len(x))
