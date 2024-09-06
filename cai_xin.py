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
    elements = local_driver.find_elements(By.XPATH, "//a[contains(@class, 'ellipsis2')]")
    for element in elements:
        text = element.text
        href = element.get_attribute('href')
        # if "贺卫方" in text:
        #     links[text] = href
        #     print(text)
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

url = 'https://search.caixin.com/newsearch/caixinsearch?keyword=%E5%BC%A0%E5%8D%83%E5%B8%86'
url = 'https://search.caixin.com/newsearch/caixinsearch?keyword=%E9%92%B1%E7%90%86%E7%BE%A4&x=0&y=0'

local_driver.get(url)
print('开始等待10秒')
time.sleep(10)

all_links = {}

run_num = 0 
while True:
    run_num = run_num + 1  
    if run_num >= 3 :
        break

    new_links = get_links(local_driver)
    all_links.update(new_links)
    
    if not click_load_more(local_driver):
        break
    
    time.sleep(5)

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

        # 检查是否出现了包含“余下全文”文本的元素并点击
        try:
            # 等待指定时间内查找链接
            more_text_link = WebDriverWait(local_driver, 2).until(
                EC.presence_of_element_located((By.LINK_TEXT, '余下全文'))
            )

            # 如果链接被找到，则进行点击
            if more_text_link.is_displayed() and more_text_link.is_enabled():
                more_text_link.click()
                time.sleep(6)  # 点击后等待页面加载完成
        except Exception as e:
            print("元素未找到或未点击:", e)

        # 向下滚动10次
        scroll_down(local_driver, 5)


        # 第六步：取 class="show_text" 的所有文字内容 保存到txt
        try:
           # 获取 id 为 'content' 的元素
            content_elements = local_driver.find_elements(By.ID, 'content') 
            content_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in content_elements])


            # 获取 class 为 'blog-content' 的元素
            blog_content_elements = local_driver.find_elements(By.CLASS_NAME, 'blog-content')
            blog_content_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in blog_content_elements]) 

            # 获取 id 为 'the_content' 的元素
            the_content_elements = local_driver.find_elements(By.ID, 'the_content')
            the_content_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in the_content_elements])  

            # 如果 blog_content_elements 没有内容，获取 class 为 'blog-top-title' 和 'content' 的元素
            if not blog_content_text:
                blog_top_title_elements = local_driver.find_elements(By.CLASS_NAME, 'blog-top-title')
                blog_top_title_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in blog_top_title_elements])  
                
                content_class_elements = local_driver.find_elements(By.CLASS_NAME, 'content')
                content_class_text = "\n\n".join([element.text.replace('\n', '\n\n') for element in content_class_elements]) 
                
                blog_content_text = f"\n{blog_top_title_text}\n\ \n{content_class_text}"

            # 合并所有内容
            combined_content = f"# {valid_filename}  \n{content_text}\n\n\n{blog_content_text}\n\n\n{the_content_text}"

            combined_content = combined_content.replace(';', '.').replace('；', '.')

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









