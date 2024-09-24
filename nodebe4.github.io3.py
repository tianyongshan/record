# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9050 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"


import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def file_exists_and_non_empty(filepath):
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def scroll_down(driver, scrolls):
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9051")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

os.makedirs('articles', exist_ok=True)

def get_page_content(driver):
    scroll_down(driver, 1)
    
    show_text_elements = driver.find_elements(By.CLASS_NAME, 'viewbox') 
    txt =  "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements])
    print('viewbox',txt)
    
    show_text_elements2 = driver.find_elements(By.CLASS_NAME, 'page_2mid.page_mid_dzzq01')
    txt2 = "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements2])
    print('page_2mid.page_mid_dzzq01',txt2)

    return txt + txt2

with open('extracted_links3.txt', 'r') as file:
    for line in file:
        url = line.strip()
        print(f"正在获取内容：{url}")

        local_driver.get(url)

        print('找标题')
        needs_continue = False
        num = 1
        while True:
            if num >= 16:
                needs_continue = True
                print('找不到标题  有异常')
                print('找不到标题  有异常')
                print('找不到标题  有异常')
                break  

            if num % 8 == 0:  
                print(f"已等待 {num} 秒，刷新页面")
                local_driver.refresh()    

            title_elements = local_driver.find_elements(By.CLASS_NAME, 'title')
            if len(title_elements)>=2:
                title_element = title_elements[1]
                link_text = title_element.text
                print('找到标题 文章加载完成1',link_text)
                break
            else:
                title_elements = local_driver.find_elements(By.XPATH, "//dt/p[1]")
                if len(title_elements):
                    title_element = local_driver.find_element(By.XPATH, "//dt/p[1]")
                    link_text = title_element.text
                    print('找到标题 文章加载完成2',link_text)
                    break

            time.sleep(1)
            num = num + 1

        if needs_continue:
            continue

        valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
        txt_file_path = os.path.join('articles', f"{valid_filename}.md")

        if file_exists_and_non_empty(txt_file_path):
            print(f"文件 {txt_file_path} 已存在且不为空，跳过链接：{url}")
            continue

        full_content = ""
        page_num = 1
        last_url = '' 

        while True:

            show_text_elements = local_driver.find_elements(By.CLASS_NAME, 'viewbox') 
            txt =  "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements])
            full_content = full_content + txt
            print('viewbox', txt[:300])
            
            show_text_elements2 = local_driver.find_elements(By.CLASS_NAME, 'page_2mid.page_mid_dzzq01')
            txt2 = "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements2])
            full_content = full_content + txt2
            print('page_2mid.page_mid_dzzq01', txt2[:300])


            next_page_elements = local_driver.find_elements(By.XPATH, "//a[contains(text(), '下一页')]")
            if len(next_page_elements) > 0:
                next_page_element = next_page_elements[0]
                href = next_page_element.get_attribute('href')
                print('下一页  href', href)
                print('下一页  text', next_page_element.text)

                if href and '#' not in href: 
                    
                    if last_url == href:
                        break

                    local_driver.execute_script("arguments[0].click();", next_page_element)
                    print('点击下一页 ')
                    time.sleep(6)
                    last_url = href
                    
                else:
                    print("到达最后一页")
                    break
            else:
                print("没有找到下一页")
                break

        full_content = full_content.replace(';', '.').replace('；', '.')
        md_content = f"# {valid_filename}\n\n{full_content}"

        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(md_content)

        print(f"文章 '{valid_filename}' 已保存")

local_driver.quit()

# keyboard click page Down 
# scroll_down(local_driver, 1)
    
            