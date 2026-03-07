import re

txt = input()
x = re.compile(r"^\d+$")

if x.match(txt):
    print("Match")
else:
    print("No match")