import os
import secrets
import time
import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
from datetime import datetime

# 使用当前时间创建保存截图和HTML报告的主文件夹
current_time = datetime.now().strftime("%Y-%m-d_%H-%M-%S")
main_output_folder = f"screenshot_results_{current_time}"
os.makedirs(main_output_folder, exist_ok=True)

# 初始化Selenium WebDriver
service = Service("C:\Program Files\Google\Chrome\Application\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# 从文件中读取目标网站URL列表
with open("site_167_1697195804.txt", "r") as file:
    websites = file.read().splitlines()

# 创建HTML报告
html_report = f"{main_output_folder}/report.html"
with open(html_report, "w", encoding="utf-8") as report:
    report.write("<html>")
    report.write("<head>")
    report.write("<title>Screenshot Report</title>")
    report.write("<style>")
    report.write("body { display: grid; grid-template-columns: repeat(3, 1fr); grid-gap: 20px; }")
    report.write("img { max-width: 100%; height: auto; }")
    report.write("</style>")
    report.write("</head>")
    report.write("<body>")

# 定义一个函数来处理每个网站的截图
def process_website(website):
    # 在每个进程中创建一个子文件夹
    current_process_id = multiprocessing.current_process().pid
    process_output_folder = f"{main_output_folder}/process_{current_process_id}"
    os.makedirs(process_output_folder, exist_ok=True)

    process_driver = webdriver.Chrome(service=service)
    process_driver.get(website)

    # 获取页面标题
    title = process_driver.title

    try:
        # 生成随机字符串并添加到文件名
        random_string = secrets.token_hex(8)
        screenshot_filename = f"{process_output_folder}/{random_string}_{title}.png"

        # 使用Pillow来检查截图是否为空
        is_screenshot_empty = Image.open(screenshot_filename).size == (0, 0)

        url = process_driver.current_url

        # 使用Selenium来获取响应码，或者设置默认值
        performance_entries = process_driver.execute_script("return performance.getEntries()")

        if performance_entries and len(performance_entries) > 0:
            response_code = performance_entries[0].get("response", {}).get("status", 0)
        else:
            response_code = 200

        if not is_screenshot_empty:
            # 截图成功时输出成功消息、文件名、URL和响应码
            print(f"成功截图: {screenshot_filename}")
            print(f"URL: {url}")
            print(f"响应码: {response_code}")

            # 在HTML中添加标题、URL、响应码和截图，使用CSS Grid布局排列
            with open(html_report, "a", encoding="utf-8") as report_file:
                report_file.write(f'<div style="border: 1px solid #ccc; padding: 10px;">')
                report_file.write(f"<h1>{title}</h1>")
                report_file.write(f'<p>URL: {url}</p>')
                report_file.write(f'<p>Response Code: {response_code}</p>')
                report_file.write(f'<a href="{url}">')
                report_file.write(f'<img src="{random_string}_{title}.png" alt="{title} Screenshot">')
                report_file.write("</div>")
        else:
            # 截图失败时输出错误消息和URL
            print(f"截图失败: {screenshot_filename}")
            print(f"URL: {url}")

    except Exception as e:
        # 截图失败时输出错误消息和URL
        print(f"截图失败: {str(e)}")
        print(f"URL: {url}")

    process_driver.quit()

# 创建进程池，限制为10个进程
with multiprocessing.Pool(processes=10) as pool:
    pool.map(process_website, websites)

# 关闭
