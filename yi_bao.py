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


def get_links(local_driver):
    links = {}
    elements = local_driver.find_elements(By.XPATH, "//a[@class='et-accent-color']")
    for element in elements:
        text = element.text
        href = element.get_attribute('href')
        links[text] = href
        print(text)
    return links

def click_load_more(local_driver):
    try:
        load_more = WebDriverWait(local_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sr_loadmore')]"))
        )
        scroll_down(local_driver, 3)
        load_more.click()
        time.sleep(5)  # 等待新内容加载
        return True
    except:
        return False

#https://yibaochina.com/?s=%E8%B5%84%E4%B8%AD%E7%AD%A0&et_pb_searchform_submit=et_search_proccess&et_pb_include_posts=yes&et_pb_include_pages=yes
base_url = 'https://yibaochina.com/?s=%E8%B4%BA%E5%8D%AB%E6%96%B9&et_pb_searchform_submit=et_search_proccess&et_pb_include_posts=yes&et_pb_include_pages=yes'
base_url = 'https://yibaochina.com/?s=%E7%A7%A6%E6%99%96&et_pb_searchform_submit=et_search_proccess&et_pb_include_posts=yes&et_pb_include_pages=yes'

all_links = {}

# for page in range(1, 14):  # 从1到13页
for page in range(1, 12):   
    url = f"{base_url}&paged={page}"
    local_driver.get(url)
    print(f'正在处理第 {page} 页')
    
    # 等待页面加载完成
    try:
        WebDriverWait(local_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='et-accent-color']"))
        )
    except:
        print(f"第 {page} 页加载超时或没有找到元素")
        continue

    new_links = get_links(local_driver)
    all_links.update(new_links)

    time.sleep(2)  # 在每页之间添加短暂延迟，避免请求过于频繁

print(f"总共找到 {len(all_links)} 个链接")

print("找到的所有链接:")
for text, href in all_links.items():
    print(f"{text}: {href}")

links_dict = all_links
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
        txt_file_path = f"大家谈/{valid_filename}.md"
        
        # 检查文件是否已存在且不为空
        if file_exists_and_non_empty(txt_file_path):
            print(f"文件 {txt_file_path} 已存在且不为空，跳过链接：{link_href}")
            continue

        # 第五步：打开链接 然后sleep 8秒
        local_driver.get(link_href)
        time.sleep(8)

        # 向下滚动10次
        scroll_down(local_driver, 5)


        # 第六步：取 class="show_text" 的所有文字内容 保存到txt
        try:
           # 获取 id 为 'content' 的元素
            content_elements = local_driver.find_elements(By.ID, 'content-area') 
            content_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in content_elements])

            # 合并所有内容
            combined_content = f"# {valid_filename}  \n{content_text}"

            print(f'Combined content:\n{combined_content}')

            # 保存到文件
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(combined_content)

        except Exception as e:
            print(f"处理链接 {link_href} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，链接文案：{link_text}")

# 关闭WebDriver
local_driver.quit()









