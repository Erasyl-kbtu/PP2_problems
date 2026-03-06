import re

txt = input().strip()
match = re.search(r"\S+@\S+\.\S+", txt)

if match:
    print(match.group())
else:
    print("No email")
