import os
import shutil
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
import psutil  # Ensure you have psutil installed

def terminate_chrome_processes(port):
    for proc in psutil.process_iter(['pid', 'name']):
        # try:
        if 'chrome' in proc.name().lower():
            for conn in proc.connections(kind='tcp'):
                if conn.laddr.port == port:
                    print(f"终止 Chrome 进程: {proc.pid}")
                    proc.terminate()
                    proc.wait(timeout=10)
                    break
        # except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        #     print('出现异常')
        #     pass

def open_website(name, start_page, end_page, port):
    MIN_PORT = 9000
    MAX_PORT = 9999
    print(f"分配的端口: {port}")

    temp_user_data_dir = tempfile.mkdtemp()
    print("浏览器临时目录:", temp_user_data_dir)

    if os.path.exists(temp_user_data_dir):
        print("临时目录已存在 先删除:", temp_user_data_dir)
        shutil.rmtree(temp_user_data_dir)

    print("复制浏览器用户数据:", temp_user_data_dir)
    default_user_data_dir = r"C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
    shutil.copytree(default_user_data_dir, temp_user_data_dir)

    with open('temp_storage.txt', 'a') as file:
        file.write(temp_user_data_dir + '\n')

    command = f'"C:\\Users\\12703\Desktop\\chrome-win64\\chrome-win64\\chrome.exe" -remote-debugging-port={port} --user-data-dir="{temp_user_data_dir}"'
    print("设置浏览器的cookie:", command)
    subprocess.Popen(command, shell=True)
    time.sleep(7)

    chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
    chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

    options = Options()
    options.binary_location = chrome_binary_path
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    # First loop: extract all links
    saved_links = extract_links(start_page, end_page, local_driver)
  
    # Second loop: process each link
    process_links(saved_links, local_driver)
    
    #################################  删除临时数据并退出
    local_driver.quit()

    print('添加短暂延迟，确保浏览器进程完全退出1')
    time.sleep(2)

    # 终止 Chrome 浏览器进程
    terminate_chrome_processes(port)
    print('添加短暂延迟，确保浏览器进程完全退出2')
    time.sleep(2)
    
    shutil.rmtree(temp_user_data_dir, ignore_errors=True)
    print("删除临时用户数据目录", temp_user_data_dir)

    #################################  更新端口
    port += 1
    if port > MAX_PORT:
        port = MIN_PORT
    with open('port.txt', 'w') as file:
        file.write(str(port))
    print("将端口号加1并更新到port.txt文件中", port)

def extract_links(start_page, end_page, local_driver):
    all_links = []

    for page in range(start_page, end_page + 1):
        if page == 1:
            url = "http://m.dunjiaodu.com/dushu/index.html"
        else:
            url = f"http://m.dunjiaodu.com/dushu/index_{page}.html"

        print(f'{page} 打开链接中 {url}  {start_page} ~~ {end_page}')
        local_driver.get(url)
        time.sleep(35)
        print(f'打开链接结束 {url} {start_page} ~~ {end_page}')

        links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, '/dushu/') and substring(@href, string-length(@href) - 4) = '.html']")
        print(f"{page}页 包含的链接: {len(links)}")

        for link in links:
            link_href = link.get_attribute('href')
            print(f'保存链接: {link_href}')
            all_links.append(link_href)

    return all_links

def process_links(saved_links, local_driver):
    for link_href in saved_links:
        print('要打开的链接',link_href)
        local_driver.get(link_href)
        time.sleep(8)

        # try:
        read_more_button = local_driver.find_element(By.ID, 'input')
        if read_more_button.is_displayed():
            print('发现 "全文" 按钮')
            read_more_button.click()
            time.sleep(3)
        # except:
        #     print('不需要翻页')

        title_element = local_driver.find_element(By.ID, 'div1')
        link_text = title_element.text.strip()

        valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
        print('文件名', valid_filename)

        if valid_filename:
            md_file_path = f"articles/{valid_filename}.md"

            if os.path.exists(md_file_path) and os.path.getsize(md_file_path) > 0:
                print(f"{md_file_path} 文件已存在 : {link_text}")
                continue

            content_element = local_driver.find_element(By.ID, 'www_ecmsphp_com')
            show_text_content = content_element.text.replace('\n', '\n\n').replace(';', '.').replace('；', '.')

            md_content = f"# {link_text}\n\n{show_text_content}"
            print(f'全文内容: {md_content}')

            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

if __name__ == "__main__":
    tasks = [
        ("Task1", 1, 5),
        ("Task2", 6, 10),
        ("Task3", 11, 15),
        ("Task4", 16, 17),
    ]

    port_start = 9222

    os.makedirs('articles', exist_ok=True)

    with ThreadPoolExecutor(max_workers=4) as executor:
        for idx, (name, start_page, end_page) in enumerate(tasks):
            port = port_start + idx
            executor.submit(open_website, name, start_page, end_page, port)
