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
    url = f"https://so.ifeng.com/?q={urllib.parse.quote(keyword)}&c=1"
    print(url)
    driver.get(url)
    time.sleep(8)

    # 按5次"Page Down"键
    actions = ActionChains(driver) 
    for _ in range(5):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1) 


    # 获取所有文章链接
    results = driver.find_elements(By.CSS_SELECTOR, ".news-stream-newsStream-news-item-infor h2 a")
    print('results',results)
    for result in results:
        try:
            href = result.get_attribute("href")
            title = result.text

            print(title,href)

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

    if driver.find_elements(By.CLASS_NAME, "index_unfoldIcon_6tI7k"):
        element = driver.find_element(By.CLASS_NAME, "index_unfoldIcon_6tI7k")
        driver.execute_script("arguments[0].click();", element)

        print('找到 展开按钮 点击')
        time.sleep(2)

    article_content = ''
    
    if driver.find_elements(By.CLASS_NAME, "index_containerBox_VAavP"):
        article_content = driver.find_element(By.CLASS_NAME, "index_containerBox_VAavP").text

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
    keywords = ["秦晖", "吴思", "钱理群", "梁文道", "陈丹青", "张鸣", "贺卫方", "张千帆"]
    ports = range(9050, 9058)  

    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = []
        for port, keyword in zip(ports, keywords):
            futures.append(executor.submit(scrape_task, port, keyword))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
