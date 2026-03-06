import re

txt = input()
x = re.findall("cat|dog", txt)
if x:
    print("Yes")
else:
    print("No")