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

def file_exists_and_non_empty(filepath):
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def get_links(local_driver):
    links = {}
    elements = local_driver.find_elements(By.XPATH, "//div[@class='news_list']//li[@class='list_title']/a")
    for element in elements:
        text = element.text
        href = element.get_attribute('href')
        links[text] = href
        print(text, href)
    return links

chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9040")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

base_url = 'http://ft.newdu.com/Search.asp?Field=Title&keyword=%CE%E2%BE%B4%E7%F6'
print('crawler 网站',base_url)
all_links = {}

for page in range(1, 10):
    url = f"{base_url}&page={page}"
    local_driver.get(url)
    print(f'正在处理第 {page} 页')
    
    try:
        WebDriverWait(local_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "news_list"))
        )
    except:
        print(f"第 {page} 页加载超时或没有找到元素")
        continue

    new_links = get_links(local_driver)
    all_links.update(new_links)

    time.sleep(10)

print(f"总共找到 {len(all_links)} 个链接")

for text, href in all_links.items():
    print(f"{text}: {href}")

with open('links.json', 'w', encoding='utf-8') as f:
    json.dump(all_links, f, ensure_ascii=False, indent=4)

os.makedirs('articles', exist_ok=True)

for link_text, link_href in all_links.items():
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text)
    valid_filename = valid_filename.strip()

    if valid_filename:
        txt_file_path = f"articles/{valid_filename}.md"
        
        if file_exists_and_non_empty(txt_file_path):
            print(f"文件 {txt_file_path} 已存在且不为空，跳过链接：{link_href}")
            continue

        local_driver.get(link_href)
        time.sleep(5)

        try:
            content_element = WebDriverWait(local_driver, 10).until(
                EC.presence_of_element_located((By.ID, 'news'))
            )
            content_text = content_element.text

            combined_content = f"# {valid_filename}\n\n{content_text}"
            combined_content = combined_content.replace(';', '.').replace('；', '.')

            # print(f'Combined content:\n{combined_content[:200]}...') # 只打印前200个字符
            print(f'Combined content:\n{combined_content}...') # 只打印前200个字符

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(combined_content)

        except Exception as e:
            print(f"处理链接 {link_href} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，链接文案：{link_text}")

local_driver.quit()
