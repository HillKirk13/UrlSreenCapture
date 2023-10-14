import os
import time
import secrets  # 导入secrets模块
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import Image
from datetime import datetime

# 使用当前时间创建保存截图和HTML报告的文件夹
current_time = datetime.now().strftime("%Y-%m-d_%H-%M-%S")
output_folder = f"screenshot_results_{current_time}"
os.makedirs(output_folder, exist_ok=True)

# 初始化Selenium WebDriver
service = Service("C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 请替换成你的Chromedriver路径
driver = webdriver.Chrome(service=service)

# 从文件中读取目标网站URL列表
with open("site_167_1697195804.txt", "r") as file:
    websites = file.read().splitlines()

# 创建HTML报告
html_report = f"{output_folder}/report.html"
with open(html_report, "w", encoding="utf-8") as report:
    report.write("<html>")
    report.write("<head>")
    report.write("<title>Screenshot Report</title>")
    # 添加响应式CSS样式
    report.write("<style>")
    report.write("body { display: flex; flex-wrap: wrap; }")
    report.write(".screenshot { flex: 0 0 33%; padding: 10px; box-sizing: border-box; }")
    report.write(".screenshot img { max-width: 100%; height: auto; }")
    report.write("</style>")
    report.write("</head>")
    report.write("<body>")

    # 循环遍历网站并生成截图，并将截图和信息添加到HTML中
    for website in websites:
        driver.get(website)

        # 获取页面标题
        title = driver.title

        try:
            # 生成随机字符串并添加到文件名
            random_string = secrets.token_hex(8)  # 生成8字节的随机字符串
            screenshot_filename = f"{output_folder}/{title}_{random_string}.png"  # 添加随机字符串
            driver.save_screenshot(screenshot_filename)

            # 使用Pillow来检查截图是否为空
            is_screenshot_empty = Image.open(screenshot_filename).size == (0, 0)

            url = driver.current_url  # 获取URL

            # 使用Selenium来获取响应码，或者设置默认值
            performance_entries = driver.execute_script("return performance.getEntries()")

            if performance_entries and len(performance_entries) > 0:
                response_code = performance_entries[0].get("response", {}).get("status", 0)
            else:
                response_code = 200  # 设置默认响应码为200（表示成功）

            # 在HTML中添加标题、URL、响应码和截图，使用CSS Flexbox布局排列
            report.write('<div class="screenshot">')
            report.write(f"<h1>{title}</h1>")
            report.write(f'<p>URL: <a href="{url}" target="_blank">{url}</a></p>')
            report.write(f'<p>Response Code: {response_code}</p>')
            if not is_screenshot_empty:
                report.write(f'<img src="{title}_{random_string}.png" alt="{title} Screenshot">')
            else:
                report.write("<p>截图失败</p>")
            report.write("</div>")

        except Exception as e:
            # 在HTML中添加错误消息和URL
            report.write('<div class="screenshot">')
            report.write(f"<h1>{title}</h1>")
            report.write(f'<p>URL: <a href="{url}">{url}</a></p>')
            report.write(f"<p>截图失败</p>")
            report.write(f"<p>{str(e)}</p>")
            report.write("</div>")

    report.write("</body>")
    report.write("</html>")

# 关闭浏览器
driver.quit()
