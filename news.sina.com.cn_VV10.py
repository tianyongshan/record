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

chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

def create_driver(port):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.binary_location = chrome_binary_path
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    return webdriver.Chrome(executable_path=chrome_driver_path, options=options)

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

    full_content = ""

    while True:
        try:
            # 获取当前页面的文章内容
            if driver.find_elements(By.CLASS_NAME, "blkContainerSblk"):
                article_content = driver.find_element(By.CLASS_NAME, "blkContainerSblk").text
                full_content += article_content + "\n\n"
            
            if driver.find_elements(By.CLASS_NAME, "lcBlk"):
                article_content2 = driver.find_element(By.CLASS_NAME, "lcBlk").text 
                full_content += article_content2 + "\n\n"

            if driver.find_elements(By.ID, "article"):
                article_content3 = driver.find_element(By.ID, "article").text 
                full_content += article_content3 + "\n\n"
            
        except:
            print('找不到文本内容 blkContainerSblk', link_text)
            return False

        # 检查是否有下一页
        try:
            next_page = driver.find_element(By.XPATH, "//a[contains(text(), '下一页')]")
            print('下一页',next_page)
            next_page.click()
            time.sleep(5)  # 等待新页面加载
        except:
            # 如果找不到下一页按钮，说明已经是最后一页
            print('没找到 下一页')
            break

    md_content = f"# {link_text}\n\n{full_content}"
    print(f'全文内容: {md_content}')

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

def scrape_task(port, links):
    driver = create_driver(port)
    for link_text, link_href in links.items():
        scrape_article(driver, link_href, link_text)
    driver.quit()

def main():
    with open('news_links.json', 'r', encoding='utf-8') as f:
        all_links = json.load(f)

    ports = range(9040, 9060)
    chunk_size = len(all_links) // len(ports)
    link_chunks = [dict(list(all_links.items())[i:i + chunk_size]) for i in range(0, len(all_links), chunk_size)]

    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = []
        for port, links in zip(ports, link_chunks):
            futures.append(executor.submit(scrape_task, port, links))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
