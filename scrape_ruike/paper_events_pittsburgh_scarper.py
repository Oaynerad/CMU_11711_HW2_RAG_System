import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 配置 Chrome 浏览器
options = Options()
options.add_argument("--headless")  # 无头模式
options.add_argument("--disable-blink-features=AutomationControlled")  # 防止被检测
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

# 启动浏览器
# 手动指定 ChromeDriver 路径（替换为你的实际路径）
chrome_driver_path = r"C:/Windows/System32/chromedriver.exe"

# 启动 ChromeDriver
service = Service(chrome_driver_path)

# 获取页面源代码
base_url = "https://www.pghcitypaper.com/pittsburgh/EventSearch?narrowByDate=2025-03-20-to-2025-12-31&page="
base_url_tail = "&sortType=date&v=d"

for page_num in range(1, 23):  
    url = f"{base_url}{page_num}{base_url_tail}"  # 构造 URL
    print(f"正在爬取: {url}")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html = driver.page_source
    # 检查请求是否成功
    
    bs = BeautifulSoup(html, "html.parser")
    div = bs.find("div", {"data-component-id": "EventSearchResultsDynamic"})   
    li_items = div.find_all("li", class_='fdn-pres-item uk-child-width-1-1@show-grid')
    
    txt_file_path = os.path.join("data", "paper_pittsburgh_events.txt")
    with open(txt_file_path, "a", encoding="utf-8") as file:
        for item in li_items:
            # 提取所有 <p> 标签的文本
            p_texts = [p.text.strip().replace("\n", "").replace("       ", "") for p in item.find_all("p")]
            # 提取指定的 <div> 内容
            div_desc = item.find("div", class_="fdn-teaser-description uk-text-break")
            if div_desc:
                div_text = div_desc.text.strip().replace("\n", "").replace("       ", "")
            # **写入文件**
            if p_texts:
                file.write("\n".join(p_texts) + "\n")
            file.write(div_text + "\n\n\n")
            
    driver.quit()
    time.sleep(1)

print(f"所有页面的数据已保存")
