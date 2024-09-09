import os
import pyautogui
import pyperclip
import time
import re

# 设置文件夹路径
folder_path = os.path.join(os.getcwd(), '大家谈')  
print('文件夹',folder_path)

# 确保文件夹存在，如果不存在就创建
os.makedirs(folder_path, exist_ok=True)

# 等待一段时间，以给自己准备时间切换到目标窗口，单位是秒
time.sleep(5)

# 初始位置
x = 752
start_y = 415

# 定义一个函数来清理文件名
def sanitize_filename(title):
    # 用下划线替换特殊字符和所有空白字符
    title = re.sub(r'[<>:"/\\|?*]', '_', title)   
    title = re.sub(r'\s+', '_', title)  
    print('清理后的文件名',title.strip('_'))
    return title.strip('_') 

def truncate_filename(title, max_length=160):
    # 限制文件名长度，确保标题加扩展名不超过 max_length
    if len(title) > max_length:
        title = title[:max_length]   
    print('截取后的标题',title)
    return title


# 每页20 
# 点击19次

for i in range(1800):
    # 计算当前 y 坐标
    y = start_y + (i % 18) * 23   

    # 点击指定坐标
    pyautogui.click(x, y)

    time.sleep(0.5)
    
    # 按住 Shift 键，按下向下箭头，然后按下 End 键
    pyautogui.keyDown('shift')  # 按住 Shift
    pyautogui.press('down')      # 按下 Down 键
    pyautogui.press('end')       # 按下 End 键
    pyautogui.keyUp('shift')     # 释放 Shift 键
    time.sleep(1.5)

    # 模拟 Ctrl + C 复制内容
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)  # 等待内容复制完毕

    # 从剪贴板读取复制的内容并打印（文章标题）
    copied_title = pyperclip.paste()
    
    # 清理文件名，删除不允许的特殊字符
    sanitized_title = sanitize_filename(copied_title)
    # 处理文件名过长的情况
    truncated_title = truncate_filename(sanitized_title)
    
    print(f"这是文章的标题: {truncated_title}")

    # 每循环 6 次后点击一次坐标 (1063, 853)
    if (i + 1) % 18 == 0:
        for _ in range(5):
            pyautogui.click(1063, 853)
            time.sleep(0.5)

    # 模拟 Ctrl+A
    pyautogui.hotkey('ctrl', 'a')

    # 模拟 Ctrl + C 复制内容
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)  # 等待内容复制完毕

    # 从剪贴板读取复制的内容并打印（文章内容）
    copied_content = pyperclip.paste()
    print(f"这是文章的内容: {copied_content}")

    # 写入内容到 md 文件
    md_file_name = f"{truncated_title}.md"  # 使用处理后的标题作为文件名
    md_file_path = os.path.join(folder_path, md_file_name)  # 拼接生成文件完整路径

    if i > 1:
        try:
            with open(md_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {truncated_title}\n\n")  # 文件内容为标题，前面加 #
                f.write(copied_content)  # 然后写入文章内容
            print(f"文章已写入文件: {md_file_path}")
        except OSError as e:
            print(f"写入文件时发生错误: {e}")
        except Exception as e:
            print(f"发生未知错误: {e}")

    time.sleep(2.5)  # 点击后等待 2.5 秒（可根据需要调整）

print("所有操作完成！")
