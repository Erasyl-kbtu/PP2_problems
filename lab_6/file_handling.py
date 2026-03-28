#creating file and writing to it

with open("text.txt", "w") as file:
    a = input("Enter the text: ")
    file.write(a)

#reading from the file
with open("text.txt", "r") as file:
    content = file.read()
    print(content)

#appending to the file
with open("text.txt", "a") as file:
    b = input("Enter the text to append:")
    file.write(b)

#copying the file
from pathlib import Path
source = Path("text.txt")
backup = Path("copy_text.txt")
backup.write_bytes(source.read_bytes())

#deleting the file
import os
if os.path.exists("text.txt"):
    os.remove("text.txt")