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
from selenium.common.exceptions import TimeoutException

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

# 访问目标页面
url = 'https://www.chineseft.net/search/?keys=%E7%AC%91%E8%9C%80&ftsearchType=type_news'
print('打开链接 ',url)
local_driver.get(url)
time.sleep(10)

while True:

    # 查找当前页 所有文章链接
    articles = local_driver.find_elements(By.CSS_SELECTOR, "a.item-headline-link.unlocked")

    # 保存链接和标题信息
    for article in articles:
        try:
            url = article.get_attribute('href')
            title = article.text
            print('文章标题',title)

            all_articles_info.append({
                'url': url,
                'title': title
            })
        except Exception as e:
            print(f"处理文章时出错: {e}")

    # 查找"下一页"按钮
    try:
        next_button = local_driver.find_element(By.XPATH, "//a[contains(text(), '下一页')]")
        print('发现下一页 点击下一页')
        next_button.click()
        time.sleep(5)
    except:
        print("没有更多页面了")
        break

# 创建保存文章的文件夹
os.makedirs('FT中文网_文章集', exist_ok=True)

# 获取并保存文章内容
for article in all_articles_info:
    print('             ')
    print('             ')
    print('             ')
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", article['title'])
    valid_filename = valid_filename.strip()
    
    if valid_filename:
        print(valid_filename)
        md_file_path = os.path.join('FT中文网_文章集', f"{valid_filename}.md")

        if file_exists_and_non_empty(md_file_path):
            print(f"文件 {md_file_path} 已存在且不为空，跳过链接：{article['url']}")
            continue

        local_driver.get(article['url'])
        print(article['url'])
        time.sleep(6)

        # 等待标题出现 
        print('等待标题出现')
        while True:
            headline_element = local_driver.find_elements(By.CSS_SELECTOR, "h1.story-headline")
            if headline_element: 
                headline_element = local_driver.find_element(By.CSS_SELECTOR, "h1.story-headline")
                headline = headline_element.text
                print('找到标题',headline)
                break
            time.sleep(3)  

            print('找不到标题 刷新页面')
            local_driver.refresh()

       
        full_text_link = local_driver.find_elements(By.XPATH, "//a[contains(@href, '/story/') and text()='全文']")
        if full_text_link:
            print('找到 全文')
            full_text_link = local_driver.find_element(By.XPATH, "//a[contains(@href, '/story/') and text()='全文']")
            full_text_link.click()
            time.sleep(5)

            # 等待标题出现 
            print('等待标题出现')
            while True:
                headline_element = local_driver.find_elements(By.CSS_SELECTOR, "h1.story-headline")
                if headline_element: 
                    headline_element = local_driver.find_element(By.CSS_SELECTOR, "h1.story-headline")
                    headline = headline_element.text
                    print('找到标题',headline)
                    break
                time.sleep(3)  

                print('找不到标题 刷新页面')
                local_driver.refresh()
                
           
        time.sleep(3)   

        # 获取摘要
        lead = local_driver.find_element(By.CSS_SELECTOR, "div.story-lead").text
        print(lead)

        try:
            # 获取正文内容
            content = local_driver.find_element(By.CSS_SELECTOR, "div.story-container.show-sticky-tools").text

            # 组合Markdown内容
            md_content = f"# {headline}\n\n## 摘要\n\n{lead}\n\n## 正文\n\n{content}"
            print(md_content)
            
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"保存文章: {article['title']} 到 {md_file_path}") 

        except TimeoutException:
            print(f"尝试 {attempt + 1}/{max_attempts}: 未找到标题，刷新页面...")
            local_driver.refresh()
            attempt += 1
            
        # scroll_down(local_driver, 1) 

    else:
        print(f"警告：无效的文件名，链接文案：{article['title']}")

# 关闭WebDriver
local_driver.quit()



