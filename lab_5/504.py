import re
txt = input()
x = re.findall("[0-9]", txt)
if x:
    for i in range (len(x)):
        print(x[i], end=" ")
else:
    print("")