import os

# 设置要替换的文件名部分及其对应的新名称
replacements = {
    "YuanWeishi": "袁伟时",
    "ZhangMing": "张鸣",
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
    "林达1_": "",
    "林达2_": "",
    "林达3_": "",
    "林达4_": "", 
    "陈丹青1_": "", 
    "梁文道1_": "", 
    "梁文道2_": "", 
    "梁文道3_": "", 
    "罗翔1_": "", 
    "QianLiqun": "钱理群"
}

# 遍历当前目录中的文件
for filename in os.listdir('.'):
    new_filename = filename
    for old, new in replacements.items():
        new_filename = new_filename.replace(old, new)
    if new_filename != filename:
        print(f"Renaming '{filename}' to '{new_filename}'")
        os.rename(filename, new_filename)
