# Step1:登陆好 让浏览器 有缓存 
# Step2:执行 下边的  指定缓存路径
# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9040 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
# Step3:上边的命令 直接会打开浏览器  不需要关闭这个浏览器  直接执行脚本 


import os
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def file_exists_and_non_empty(filepath):
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def scroll_down(driver, scrolls):
    """向下滚动页面一定次数."""
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

# 浏览器准备工作
chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9040")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# 打开目标网页
url = 'https://news.sina.com.cn/m/nfzmgz/list.html'
local_driver.get(url)

time.sleep(10)

links_dict = {}
page_count = 1

# 遍历所有页面
while True:
    # 找到所有新闻链接
    news_links = local_driver.find_elements(By.XPATH, f"//div[@id='Page_{page_count}']//li/a")
    
    for link in news_links:
        link_text = link.text
        link_href = link.get_attribute('href')
        print(f"{page_count} 文字内容是啥：{link_text}  链接是啥：{link_href}")
        links_dict[link_text] = link_href

    # 点击下一页
    try:
        next_page_button = local_driver.find_element(By.XPATH, f"//div[@id='PageList_2']//a[text()='下一页']")
        next_page_button.click()
        time.sleep(2)  # 等待页面加载
    except NoSuchElementException:
        print("无法找到'下一页'按钮，可能已到达最后一页")
        break

    # 限制爬取的页数
    # if page_count >= 100:
    #     print("已达到100页，停止爬取")
    #     break

    page_count += 1

# 保存为JSON文件
with open('news_links.json', 'w', encoding='utf-8') as f:
    json.dump(links_dict, f, ensure_ascii=False, indent=4)

# # 确保 南方周末 文件夹存在
# os.makedirs('南方周末', exist_ok=True)

# # 循环所有保存的链接
# for link_text, link_href in links_dict.items():
#     # 创建适合文件名的文本
#     valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text)
#     valid_filename = valid_filename.strip()

#     if valid_filename:
#         md_file_path = f"南方周末/{valid_filename}.md"
        
#         # 检查文件是否已存在且不为空
#         if file_exists_and_non_empty(md_file_path):
#             print(f"文件 {md_file_path} 已存在且不为空，跳过链接：{link_href}")
#             continue

#         # 打开链接
#         local_driver.get(link_href)
#         time.sleep(6)

#         # 向下滚动
#         scroll_down(local_driver, 5)

#         try:
#             # 获取文章内容
#             article_content = local_driver.find_element(By.CLASS_NAME, "blkContainerSblk").text
            
#             # 创建 Markdown 内容
#             md_content = f"# {valid_filename}\n\n{article_content}"
#             print(f'文章内容: {md_content[:200]}...')  # 只打印前200个字符
            
#             with open(md_file_path, 'w', encoding='utf-8') as md_file:
#                 md_file.write(md_content)

#         except Exception as e:
#             print(f"处理链接 {link_href} 出现错误：{e}")

#     else:
#         print(f"警告：无效的文件名，链接文案：{link_text}")

# 关闭WebDriver
local_driver.quit()
