import json
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import urllib.parse

chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

def create_driver(port):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.binary_location = chrome_binary_path
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    return webdriver.Chrome(executable_path=chrome_driver_path, options=options)

def scrape_search_results(driver, keyword):
    links = {}
    for page in range(5):
        url = f"https://www.google.com/search?q=ifeng.com+{urllib.parse.quote(keyword)}&start={page * 10}"
        print(url)
        driver.get(url)
        time.sleep(8)

        results = driver.find_elements(By.CLASS_NAME, "yuRUbf")
        for result in results:
            try:
                link = result.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                print(href)
                title = link.find_element(By.TAG_NAME, "h3").text
                print(title)
                if "ifeng.com" in href:
                    links[title] = href
            except:
                continue

    return links

def scrape_article(driver, link_href, link_text):
    print('文章详情链接', link_href)
    driver.get(link_href)
    time.sleep(8)

    print('文章标题', link_text)

    valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
    print('MD文件名', valid_filename)

    md_file_path = f"articles/{valid_filename}.md"
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    if os.path.exists(md_file_path) and os.path.getsize(md_file_path) > 0:
        print(f"{md_file_path} 文件已存在 : {link_text}")
        return

    try:
        article_content = driver.find_element(By.ID, "article").text
    except:
        print('找不到文本内容 article', link_text)
        return False

    md_content = f"# {link_text}\n\n{article_content}"
    print(f'全文内容: {md_content}')

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

def scrape_task(port, keyword):
    driver = create_driver(port)
    links = scrape_search_results(driver, keyword)
    for link_text, link_href in links.items():
        scrape_article(driver, link_href, link_text)
    driver.quit()

def main():
    keywords = ["秦晖", "吴思", "钱理群", "梁文道", "陈丹青", "张鸣", "贺卫方", "张千帆"]
    ports = range(9040, 9048)  # 假设有8个可用的端口

    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = []
        for port, keyword in zip(ports, keywords):
            futures.append(executor.submit(scrape_task, port, keyword))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
