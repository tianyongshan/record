import os
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

def scrape_pages(start_page, end_page, port):
    driver = create_driver(port)
    all_links = {}

    for page in range(start_page, end_page + 1):
        url = f"https://www.artda.cn/renwenlishi-{page}.html"

        print(f'{page}  打开链接中{url}  {start_page} ~~ {end_page}   {port}')
        
        driver.get(url)
        
        num = 1    
        while True:
            links = driver.find_elements(By.XPATH, "//ul[@class='list']/li/a")
            if len(links):
                print('页面加载完毕 跳出死循环 ')
                break
            
            if num % 10 == 0:
                driver.refresh()

            print('页面加载中 ')

            num = num + 1 
            time.sleep(1)
            
        
        links = driver.find_elements(By.XPATH, "//ul[@class='list']/li/a")
        print(f"{page}页 包含的链接总数: {len(links)}")

        for link in links:
            link_href = link.get_attribute('href')
            link_text = link.text
            print('文本',link_text)
            print('链接',link_href)

            if not link_text or link_text.isdigit() or link_text in ['下一页', '尾页','首页']:
                print('文本是无效的  continue')
                continue

            all_links[link_text] = link_href

    for link_text, link_href in all_links.items():
        scrape_article(driver, link_href,link_text)

    driver.quit()

def scrape_article(driver, link_href,link_text):
    print('文章详情链接', link_href)
    driver.get(link_href)
    time.sleep(8)

    print('文章标题', link_text)

    valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
    print('MD文件名', valid_filename)

    md_file_path = f"articles/{valid_filename}.md"
    if os.path.exists(md_file_path) and os.path.getsize(md_file_path) > 0:
        print(f"{md_file_path} 文件已存在 : {link_text}")
        return

    content_elements = driver.find_elements(By.CLASS_NAME, 'read-content')
    if content_elements:
        content_element = content_elements[0]
    else:
        print('找不到文本内容 read-content',link_text)
        return False
    
    show_text_content = content_element.text.replace('\n', '\n\n').replace(';', '.').replace('；', '.')

    md_content = f"# {link_text}\n\n{show_text_content}"
    print(f'全文内容: {md_content}')

    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(md_content)

def main():
    start_page = 1
    end_page = 9
    num_tasks = 3   
    ports = range(9040, 9043)

    pages_per_task = (end_page - start_page + 1) // num_tasks
    
    with ThreadPoolExecutor(max_workers=len(ports)) as executor:
        futures = []
        for i, port in enumerate(ports):
            task_start = start_page + i * pages_per_task
            task_end = task_start + pages_per_task - 1 if i < num_tasks - 1 else end_page
            futures.append(executor.submit(scrape_pages, task_start, task_end, port))
        
        for future in futures:
            future.result()

if __name__ == "__main__":
    main()
