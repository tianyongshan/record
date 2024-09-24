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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

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
    url = f"https://www.reddit.com/search/?q={urllib.parse.quote(keyword)}&type=link"
    print(url)
    driver.get(url)
    time.sleep(8)

    # 滚动页面以加载更多结果
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 获取所有文章链接
    results = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='search-post-unit'] h2 a")
    print('results', results)
    for result in results:
        try:
            href = result.get_attribute("href")
            title = result.get_attribute("aria-label")

            print(title, href)

            if href and title:
                links[title] = href
        except:
            continue

    return links

def scrape_article(driver, link_href, link_text):
    print('文章详情链接', link_href)
    
    print('文章标题', link_text)

    valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
    print('MD文件名', valid_filename)

    md_file_path = f"articles/{valid_filename}.md"
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    if os.path.exists(md_file_path) and os.path.getsize(md_file_path) > 0:
        print(f"{md_file_path} 文件已存在 : {link_text}")
        return

    driver.get(link_href)
    time.sleep(8)

    article_content = ''
    
    content_elements = driver.find_elements(By.CLASS_NAME, "text-neutral-content")
    if content_elements:
        article_content = '\n\n'.join([elem.text for elem in content_elements])

    if not article_content:
        print("警告：未找到指定的元素或元素为空。请检查网页结构或元素类名是否正确。")
        with open("failed_links.txt", "a", encoding='utf-8') as f:
            f.write(f"{link_href}\n")
        return

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
    keywords = ["李承鹏","笑蜀",'余英时']
    ports = range(9050, 9053)  
    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = []
        for port, keyword in zip(ports, keywords):
            futures.append(executor.submit(scrape_task, port, keyword))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
