import re

text = input()
matches = re.findall(r"\b[a-zA-Z]{3}\b", text)

print(len(matches))
