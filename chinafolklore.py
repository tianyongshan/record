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
    print('向下滚动 ',scrolls)
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

def scrape_article(driver, article_url):
    print('打开地址',article_url)
    driver.get(article_url)
    time.sleep(6)

    title = driver.find_element(By.CLASS_NAME, "news_title").text.strip()
    print('标题',title)

    date = driver.find_element(By.CLASS_NAME, "news_title").get_attribute('title').split('发表时间：')[-1].strip()
    print('时间',date)

    # 收集所有页面链接
    all_links = [article_url]
    pagination_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/web/index.php?Page=')]")
    for link in pagination_links:
        print('链接地址',link.get_attribute('href'))
        print('文案',link.text)
        all_links.append(link.get_attribute('href'))

    content = ""
    
    # 遍历所有链接并获取内容
    for link in all_links:
        print('打开地址',link)
        driver.get(link)
        time.sleep(5)
        content_element = driver.find_element(By.CLASS_NAME, "text-12")
        # print('content_element',content_element.text)
        print('内容元素',content_element)
        content += content_element.text.replace('\n', '\n\n') + "\n\n"

    return title, date, content.strip()


# 浏览器准备工作
chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9039")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# 保存所有文章信息
all_articles_info = []

# 打开初始页面
url = 'https://www.chinafolklore.org/web/index.php?_MULTI_PAGE_START=0&NewsKeyword=%B9%F9%D3%DA%BB%AA&Search_x=0&Search_y=0&IndexSearch=chinesefolklore.org.cn'
local_driver.get(url)
time.sleep(10)

# 遍历页面
while True:
    # 查找所有文章链接
    articles = local_driver.find_elements(By.CSS_SELECTOR, "a.news")

    # 保存链接和日期信息
    for article in articles:
        try:
            url = article.get_attribute('href')
            title = article.text
            date_str = article.get_attribute('title').split('发表时间：')[-1].strip()
            
            print(f"标题: {title}")
            print(f"日期: {date_str}")

            all_articles_info.append({
                'url': url,
                'title': title,
                'date': date_str
            })
        except Exception as e:
            print(f"处理文章时出错: {e}")

    # 查找下一页按钮
    try:
        next_page = local_driver.find_element(By.XPATH, "//a[text()='下页']")
        print('找到 下一页 点击')
        next_page.click()
        time.sleep(7)
    except:
        print("没有下一页了，结束遍历")
        break

# 创建单一目录保存所有文章
articles_folder = '中国民俗学网_文章集'
os.makedirs(articles_folder, exist_ok=True)

# 保存文章
for article in all_articles_info:
    valid_filename = re.sub(r'[\\/*?:"<>|]', "", article['title'])
    valid_filename = valid_filename.strip()

    if valid_filename:
        md_file_path = os.path.join(articles_folder, f"{valid_filename}.md")

        if file_exists_and_non_empty(md_file_path):
            print(f"文件 {md_file_path} 已存在 且内容不为空，跳过链接：{article['url']}")
            continue

        try:
            title, date, content = scrape_article(local_driver, article['url'])
            
            content = content.replace(';', '.').replace('；', '.')

            md_content = f"# {title}\n\n发表时间：{date}\n\n{content}"
            print(md_content)

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"保存文章: {title} 到 {md_file_path}")

        except Exception as e:
            print(f"处理链接 {article['url']} 出现错误：{e}")

    else:
        print(f"警告：无效的文件名，链接文案：{article['title']}")

# 关闭WebDriver
local_driver.quit()










