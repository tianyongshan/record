import os
import time
import tempfile
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import re

def file_exists_and_non_empty(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0

def terminate_chrome_processes(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'chrome' in proc.name().lower():
                for conn in proc.connections(kind='tcp'):
                    if conn.laddr.port == port:
                        print(f"Terminating Chrome process: {proc.pid}")
                        proc.terminate()
                        proc.wait(timeout=10)
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def open_website(name, url, port):
    print(f"Task started: {name}")
    
    MIN_PORT = 9000
    MAX_PORT = 9999 

    print(f"Assigned port: {port}")

    temp_user_data_dir = tempfile.mkdtemp()
    print("Temporary user data directory:", temp_user_data_dir)

    if os.path.exists(temp_user_data_dir):
        print("Temporary directory exists, deleting it first:", temp_user_data_dir)
        shutil.rmtree(temp_user_data_dir)

    print("Copying default user data directory to temporary directory:", temp_user_data_dir)
    default_user_data_dir = r"C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
    shutil.copytree(default_user_data_dir, temp_user_data_dir)

    with open('temp_storage.txt', 'a') as file:
        file.write(temp_user_data_dir + '\n')

    command = f'"C:\\Users\\12703\\Desktop\\chrome-win64\\chrome-win64\\chrome.exe" -remote-debugging-port={port} --user-data-dir="{temp_user_data_dir}"'
    print("Set browser cookies:", command)
    subprocess.Popen(command, shell=True)
    time.sleep(10)  # Increased sleep time to ensure the browser launches correctly

    chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
    chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

    options = Options()
    options.binary_location = chrome_binary_path
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
    local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    
    try:
        local_driver.get(url)
        print('Opened URL', url)
        time.sleep(10)  # Wait for the page to load

        links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, '/data/') and substring(@href, string-length(@href) - 4) = '.html']")
        print(f"Initial links count: {len(links)}")
        
        while not links:  # Improve condition
            print('Waiting for links to appear...')
            time.sleep(5)
            links = local_driver.find_elements(By.XPATH, "//a[starts-with(@href, '/data/') and substring(@href, string-length(@href) - 4) = '.html']")
        
        links_dict = {link.text: link.get_attribute('href') for link in links}

        with open('links.json', 'w', encoding='utf-8') as f:
            json.dump(links_dict, f, ensure_ascii=False, indent=4)

        os.makedirs('articles', exist_ok=True)

        for link_text, link_href in links_dict.items():
            valid_filename = re.sub(r'[\\/*?:"<>|]', "", link_text).strip()
            if valid_filename:
                txt_file_path = f"articles/{name}_{valid_filename}.md"

                if file_exists_and_non_empty(txt_file_path):
                    print(f"File {txt_file_path} exists and is not empty, skipping link: {link_href}")
                    continue
                
                local_driver.get(link_href)
                print('Opened link', link_href)
                time.sleep(10)

                try:
                    show_text_elements = local_driver.find_elements(By.CLASS_NAME, 'show_text')
                    show_text_content = "\n\n".join([element.text.replace('\n', '\n\n') for element in show_text_elements])
                    show_text_content = show_text_content.replace(';', '.').replace('；', '.')
                    
                    md_content = f"# {valid_filename}\n\n{show_text_content}"

                    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(md_content)
                except Exception as e:
                    print(f"Error processing link {link_href}: {e}")

    finally:
        local_driver.quit()
        print('Closing browser')
        time.sleep(5)
    
        terminate_chrome_processes(port)
        print('Short delay to ensure browser processes are terminated')
        time.sleep(2)

        shutil.rmtree(temp_user_data_dir, ignore_errors=True)
        print("Deleted temporary user data directory:", temp_user_data_dir)

    with open('port.txt', 'w') as file:
        port = port + 1 if port < MAX_PORT else MIN_PORT
        file.write(str(port))
    print(f"Incremented port number to: {port}")

task_dict = {
    "张五常": "https://www.aisixiang.com/thinktank/zhangwuchang.html",
    "林达2": "https://www.aisixiang.com/data/search?searchfield=author&keywords=%e6%9e%97%e8%be%be&page=2",
    "林达3": "https://www.aisixiang.com/data/search?searchfield=author&keywords=%e6%9e%97%e8%be%be&page=3",
    "林达4": "https://www.aisixiang.com/data/search?searchfield=author&keywords=%e6%9e%97%e8%be%be&page=4"
}

port_start = 9222

with ThreadPoolExecutor(max_workers=10) as executor:
    for idx, (name, url) in enumerate(task_dict.items()):
        port = port_start + idx
        executor.submit(open_website, name, url, port)
