# Step1:登陆好 让浏览器 有缓存 
# Step2:执行 下边的  指定缓存路径
# "C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe" -remote-debugging-port=9039 --user-data-dir="C:\Users\12703\AppData\Roaming\Google\Chrome\User Data\Default"
# Step3:上边的命令 直接会打开浏览器  不需要关闭这个浏览器  直接执行脚本 
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 浏览器准备工作
chrome_driver_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chromedriver-win64\chromedriver.exe'
chrome_binary_path = r'C:\Users\12703\Desktop\chrome-win64\chrome-win64\chrome.exe'

options = Options()
options.binary_location = chrome_binary_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9039")
local_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

# 打开固定地址
url = 'https://chinadigitaltimes.net/chinese/chronicle-of-major-events'
local_driver.get(url)
time.sleep(10)

# 创建已保存事件的数组
saved_events = []

# 创建或打开大事记.md文件
with open('中国数字时代-大事记.md', 'w', encoding='utf-8') as md_file:
    md_file.write("# 中国数字时代大事记\n\n")

    while True:
        # 查找特定DIV元素
        table_div = local_driver.find_element(By.CSS_SELECTOR, "div.footable_parent.ninja_table_wrapper.wp_table_data_press_parent.bootstrap4.colored_table")
        
        # 在该DIV元素中查找所有行
        rows = table_div.find_elements(By.CSS_SELECTOR, "tr[data-row_id]")

        # 保存每行的信息
        for row in rows:
            try:
                time_v = row.find_element(By.CSS_SELECTOR, "td.ninja_column_0").text
                event = row.find_element(By.CSS_SELECTOR, "td.ninja_column_1").text
                
                # 检查事件是否已存在
                if event not in saved_events:
                    md_content = f" {time_v}\n\n"
                    md_content += f"{event}\n\n"
                    md_content += "\n\n"

                    md_file.write(md_content)
                    print(f"已保存事件：{time_v} - {event}")
                    
                    # 将事件添加到已保存事件数组中
                    saved_events.append(event)
                else:
                    print(f"事件已存在，跳过：{time_v} - {event}")

            except Exception as e:
                print(f"处理行时出错: {e}")

        # 检查是否有下一页
        try:
            next_button = local_driver.find_element(By.XPATH, "//a[@class='footable-page-link' and @aria-label='next']")
            next_button.click()
            time.sleep(5)
        except:
            print("没有下一页了，结束爬取。")
            break

# 关闭WebDriver
local_driver.quit()

print("所有事件已保存到 大事记.md 文件中。")
print(f"共保存了 {len(saved_events)} 个独特事件。")

