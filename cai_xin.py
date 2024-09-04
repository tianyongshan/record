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
url = 'https://search.caixin.com/newsearch/caixinsearch?keyword=%E8%B4%BA%E5%8D%AB%E6%96%B9&x=0&y=0'
local_driver.get(url)
print('等待10秒')
time.sleep(10)

all_links = {}

run_num = 0 
while True:
    run_num = run_num + 1  
    if run_num >= 5 :
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




# 帮我继续往下吧 谢谢 我已经打开网址了  
# 网址里 是 新闻链接  新闻链接下边  是  加载更多的按钮 

# 取元素示例：
# local_driver.find_elements(By.XPATH,

# 需要做的是  把 所有a链接 都找到  如果 链接包含文字 张千帆  则保存起来：链接文本为Key  链接为Value
  
# 示例  
# <a class="ellipsis2" href="https://zousicong.blog.caixin.com/archives/64181?originReferrer=caixinsearch_pc" data-articleid="64181" data-articletitle="张千帆：薄熙来“唱红遗产”的危害"><font color="red"><b>张千帆</b></font>：薄熙来“唱红遗产”的危害</a>

# 当前的链接保存好了之后  看看最后有没有“加载更多”
# <button class="sr_loadmore" style="">加载更多 <i class="el-icon is-loading" style="display: none;"><svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M512 64a32 32 0 0 1 32 32v192a32 32 0 0 1-64 0V96a32 32 0 0 1 32-32zm0 640a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V736a32 32 0 0 1 32-32zm448-192a32 32 0 0 1-32 32H736a32 32 0 1 1 0-64h192a32 32 0 0 1 32 32zm-640 0a32 32 0 0 1-32 32H96a32 32 0 0 1 0-64h192a32 32 0 0 1 32 32zM195.2 195.2a32 32 0 0 1 45.248 0L376.32 331.008a32 32 0 0 1-45.248 45.248L195.2 240.448a32 32 0 0 1 0-45.248zm452.544 452.544a32 32 0 0 1 45.248 0L828.8 783.552a32 32 0 0 1-45.248 45.248L647.744 692.992a32 32 0 0 1 0-45.248zM828.8 195.264a32 32 0 0 1 0 45.184L692.992 376.32a32 32 0 0 1-45.248-45.248l135.808-135.808a32 32 0 0 1 45.248 0zm-452.544 452.48a32 32 0 0 1 0 45.248L240.448 828.8a32 32 0 0 1-45.248-45.248l135.808-135.808a32 32 0 0 1 45.248 0z"></path></svg></i></button>
# 有的话  点击 然后等待几秒 然后 重新抓链接  知道把链接抓完









# while True:







# # 第二步：找到所有以下规律的链接
# links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, '/book/') and substring(@href, string-length(@href) - 3) = '.htm']")
# while True:
#     if len(links)>0:
#         break
#     links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, '/book/') and substring(@href, string-length(@href) - 3) = '.htm']")
#     print('循环等待中')    
#     time.sleep(5)

# moreEle = local_driver.find_element(By.ID, 'more_dir')
# if links:
#     moreEle.click()


# # 第三步：把所有链接保存到数组里
# links_dict = {}
# for link in links:
#     link_text = link.text
#     link_href = link.get_attribute('href')
#     print(f"文字内容是啥：{link_text}  链接是啥：{link_href}")
#     links_dict[link_text] = link_href

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
        txt_file_path = f"大家谈/{valid_filename}.txt"
        
        # 检查文件是否已存在且不为空
        if file_exists_and_non_empty(txt_file_path):
            print(f"文件 {txt_file_path} 已存在且不为空，跳过链接：{link_href}")
            continue

        # 第五步：打开链接 然后sleep 8秒
        local_driver.get(link_href)
        time.sleep(8)

        # 向下滚动10次
        scroll_down(local_driver, 10)


        # 第六步：取 class="show_text" 的所有文字内容 保存到txt
        try:
            show_text_elements = local_driver.find_elements(By.ID, 'content')
            show_text_content = "\n".join([element.text for element in show_text_elements])
            print(f'show_text_content: {show_text_content}')

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(show_text_content)

        except Exception as e:
            print(f"处理链接 {link_href} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，链接文案：{link_text}")

# 关闭WebDriver
local_driver.quit()