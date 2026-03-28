from pathlib import Path

#creating a directory
nested_dir = Path("my_directory/nested_directory")
nested_dir.mkdir(parents=True, exist_ok=True)

#listing files and folders
for item in Path("my_directory").iterdir():
    type_set = "Directory" if item.is_dir() else "File"
    print(f"{item}: ({type_set})")

#finding files by extension
txt_files = list(Path("my_directory").rglob("*.txt"))
for item in txt_files:
    print(item) 

#moving files between directories
import shutil
from pathlib import Path

# Define paths
source = Path("sample.txt")
destination = Path("project/data/sample_moved.txt")

# 1. To MOVE:
if source.exists():
    source.rename(destination)
    print("File moved successfully.")

shutil.copy(destination, "project/data/logs/backup_sample.txt")
print("File copied to logs folder.")