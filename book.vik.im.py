# Step1:登陆好 让浏览器 有缓存 
# Step2:执行 下边的  指定缓存路径
# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9039 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
# Step3:上边的命令 直接会打开浏览器  不需要关闭这个浏览器  直接执行脚本 

import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
import subprocess
import tempfile
import shutil
import os
import base64
import json
import requests
import chardet
import subprocess
import smtplib
import random
import chardet
import pymysql
import time
import pyperclip
import pyautogui
import calendar 
import psutil
import subprocess
import shutil 
from PIL import Image 
from datetime import datetime  
from datetime import datetime, timedelta 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException 
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import time 
from selenium.webdriver.chrome.service import Service 
from dateutil.relativedelta import relativedelta  
from selenium.webdriver.common.keys import Keys    
import re 
 

def file_exists_and_non_empty(filepath):
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def scroll_down(driver, scrolls):
    """向下滚动页面一定次数."""
    for _ in range(scrolls):
        # 向下滚动页面
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # 每次滚动后等待一秒


################################# [浏览器 准备工作 S]  ########################################  


chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'  # 替换为你的 Chrome 安装路径

# 创建浏览器对象
options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress",  "127.0.0.1:9039")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options) 

# 第一步：浏览器打开该地址
url = 'https://book.vik.im/index.php?id=141706888666&display=menu'
local_driver.get(url)

time.sleep(10) 


links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://book.vik.im/index.php?id=')]")
while True:
    if len(links) > 0:
        break
    links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://book.vik.im/index.php?id=')]")

    print('循环等待中')
    time.sleep(5)

# 向下滚动  
scroll_down(local_driver, 2)


# 第三步：把所有链接保存到数组里
links_dict = {}
for link in links:
    link_text = link.text
    link_href = link.get_attribute('href')
    print(f"文字内容是啥：{link_text}  链接是啥：{link_href}")
    links_dict[link_text] = link_href

# 保存为JSON文件，方便后续使用
with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(links_dict, f, ensure_ascii=False, indent=4)

# 确保 大家谈 文件夹存在
os.makedirs('大家谈', exist_ok=True)

# 第四步：循环所有保存的链接
for link_text, link_href in links_dict.items():
    # 创建适合文件名的文本
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text)
    valid_filename = valid_filename.strip()

    if valid_filename:
        

        # 第五步：打开链接 然后sleep 8秒
        local_driver.get(link_href)
        time.sleep(6)

        # 向下滚动 
        scroll_down(local_driver, 2)


        # 第六步：取 class="show_text" 的所有文字内容 保存到txt
        try:
            title = local_driver.find_element(By.CLASS_NAME, 'calibre1').text

            txt_file_path = f"大家谈/{title}.md"
        
            # 检查文件是否已存在且不为空
            if file_exists_and_non_empty(txt_file_path):
                print(f"文件 {txt_file_path} 已存在且不为空，跳过链接：{link_href}")
                continue
            

            show_text_elements = local_driver.find_elements(By.ID, 'adsense')
            show_text_content = "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements])
            # 创建 Markdown 内容，将 valid_filename 作为标题
            # md_content = f"# {valid_filename}\n\n{show_text_content}"
            md_content = f"# {title}\n\n{show_text_content}"

            md_content = md_content.replace(';', '.').replace('；', '.')

            print(f'show_text_content: {md_content}')

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(md_content)

        except Exception as e:
            print(f"处理链接 {link_href} 出现错误：{e}")


    else:
        print(f"警告：无效的文件名，链接文案：{link_text}")

# 关闭WebDriver
local_driver.quit()