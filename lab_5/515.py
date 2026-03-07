import re

def double_digit(match):
    digit = match.group(0)
    return digit * 2

input_string = input()

result = re.sub(r'\d', double_digit, input_string)

print(result)