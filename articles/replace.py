import os

# 设置要替换的文件名部分及其对应的新名称
replacements = {
    "YuanWeishi": "袁伟时",
    "ZhangMing": "张鸣",
    "林达1_": "",
    "林达2_": "",
    "林达3_": "",
    "林达4_": "",
    # "_": "",
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
