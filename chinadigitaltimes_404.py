# Step1:登陆好 让浏览器 有缓存 
# Step2:执行 下边的  指定缓存路径
# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9039 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
# Step3:上边的命令 直接会打开浏览器  不需要关闭这个浏览器  直接执行脚本 
import os
import time
import json
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
options.add_experimental_option("debuggerAddress", "127.0.0.1:9039")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# 保存所有文章信息
all_articles_info = []

# 打开固定地址
url = 'https://chinadigitaltimes.net/chinese/404-articles-archive'
local_driver.get(url)
time.sleep(10)

# 遍历前十页
for page in range(1, 11):
    print(page)
    # 查找所有文章行
    articles = local_driver.find_elements(By.CSS_SELECTOR, "tr[data-row_id]")
    print(articles)
    
    # 保存链接和日期信息
    for article in articles:
        try:
            title_element = article.find_element(By.CSS_SELECTOR, "td.ninja_column_0")
            date_element = article.find_element(By.CSS_SELECTOR, "td.ninja_column_2")
            link_element = article.find_element(By.CSS_SELECTOR, "td.ninja_clmn_nm_cdt a")
            
            url = link_element.get_attribute('href')
            title = title_element.text
            print(title)

            date_str = date_element.text
            print(date_str)
            
            # 解析日期
            date = date_str.replace('-', '_')  # 使用网站提供的日期格式，并替换连字符为下划线

            all_articles_info.append({
                'url': url,
                'title': title,
                'date': date
            })
        except Exception as e:
            print(f"处理文章时出错: {e}")

    # 点击下一页
    try:
        next_page = WebDriverWait(local_driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.footable-page-link[aria-label='next']"))
        )
        next_page.click()
        time.sleep(10)
    except Exception as e:
        print(f"无法点击下一页，可能已经到达最后一页: {e}")
        break

# 按日期分类保存文章
for article in all_articles_info:
    date_folder = os.path.join('中国数字时代_404', article['date'][:7])
    os.makedirs(date_folder, exist_ok=True)

    valid_filename = re.sub(r'[\\/*?:"<>|]', "", article['title'])
    valid_filename = valid_filename.strip()

    if valid_filename:
        md_file_path = os.path.join(date_folder, f"{valid_filename}.md")

        if file_exists_and_non_empty(md_file_path):
            print(f"文件 {md_file_path} 已存在且不为空，跳过链接：{article['url']}")
            continue

        local_driver.get(article['url'])
        time.sleep(6)

        scroll_down(local_driver, 5)

        try:
            content_elements = local_driver.find_elements(By.CSS_SELECTOR, "div.et_pb_extra_column_main") 

            content = "\n\n".join([element.text.replace('\n', '\n\n') for element in content_elements])
            
            content = content.replace(';', '.').replace('；', '.')

            md_content = f"# {article['title']}\n\n{content}"
            print(md_content)

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"保存文章: {article['title']} 到 {md_file_path}")

        except Exception as e:
            print(f"处理链接 {article['url']} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，链接文案：{article['title']}")

# 关闭WebDriver
local_driver.quit()
