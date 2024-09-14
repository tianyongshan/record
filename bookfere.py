# Step1:登陆好 让浏览器 有缓存 
# Step2:执行 下边的  指定缓存路径
# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9039 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
# Step3:上边的命令 直接会打开浏览器  不需要关闭这个浏览器  直接执行脚本 

import os
import time
import re
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

# 遍历5页
for page in range(1, 6):
    url = f'https://bookfere.com/category/essay/page/{page}'
    local_driver.get(url)
    time.sleep(10)

    # 查找所有文章链接
    articles = local_driver.find_elements(By.CSS_SELECTOR, "a[href^='https://bookfere.com/post/'][href$='.html']")

    # 保存链接和标题信息
    for article in articles:
        try:
            url = article.get_attribute('href')
            title = article.text
            print(f"标题: {title}")
            print(f"链接: {url}")

            if "年" in title and "月" in title and "日" in title:
                print(f"跳过包含日期的文章: {title}")
                continue

            all_articles_info.append({
                'url': url,
                'title': title
            })
        except Exception as e:
            print(f"处理文章时出错: {e}")

# 创建保存文章的文件夹
os.makedirs('Bookfere_文章集', exist_ok=True)

# 抓取并保存文章内容
for article in all_articles_info:
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", article['title'])
    valid_filename = valid_filename.strip()

    if valid_filename:
        md_file_path = os.path.join('Bookfere_文章集', f"{valid_filename}.md")

        if file_exists_and_non_empty(md_file_path):
            print(f"文件 {md_file_path} 已经存在  且文件不为空，跳过链接：{article['url']}")
            continue

        local_driver.get(article['url'])
        time.sleep(6)

        scroll_down(local_driver, 5)

        try:
            content_element = local_driver.find_element(By.ID, "article")
            content = content_element.text.replace('\n', '\n\n')
            
            content = content.replace(';', '.').replace('；', '.')

            md_content = f"# {article['title']}\n\n{content}"
            print(md_content)

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"保存文章: {article['title']} 到 {md_file_path}")

        except Exception as e:
            print(f"处理链接 {article['url']} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，   链接文案：{article['title']}")

# 关闭WebDriver
local_driver.quit()


# 
