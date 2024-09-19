import os

# 设置要替换的文件名部分及其对应的新名称
replacements = {
    "Task1_": "",
    "Task2_": "",
    "Task3_": "",
    "Task4_": "",
    "Task5_": "",
    "Task6_": "",
    "Task7_": "",
    "Task8_": "",
    "Task9_": "",
    "Task10_": "",
}

# 遍历当前目录中的文件
for filename in os.listdir('.'):
    new_filename = filename
    for old, new in replacements.items():
        new_filename = new_filename.replace(old, new)
    if new_filename != filename:
        if os.path.exists(new_filename):
            print(f"Skipping renaming '{filename}' to '{new_filename}' because '{new_filename}' already exists.")
            continue
        print(f"Renaming '{filename}' to '{new_filename}'")
        os.rename(filename, new_filename)
