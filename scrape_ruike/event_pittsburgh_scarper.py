import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json

base_url = "https://pittsburgh.events/?pagenum="
base_url_tail = "&start_date=2025-03-20&end_date=2026-03-01"
all_events = []

# 遍历 pagenum 1 到 41
for page_num in range(1, 41):  
    url = f"{base_url}{page_num}{base_url_tail}"  # 构造 URL
    print(f"正在爬取: {url}")

    # 发送请求
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # 检查请求是否成功
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, "html.parser")
        
        ul = bs.find("ul", class_="dates-list")

        # 这里你可以提取所需数据，例如所有的活动标题
        scripts = ul.find_all("script", {"type": "application/ld+json"})
        
        for script in scripts:
            try:
                text = json.loads(script.string)  # 解析 JSON
                all_events.append(text)  # 添加到列表
            except json.JSONDecodeError:
                print("JSON 解析失败，可能格式不正确")
    
    else:
        print(f"无法访问 {url}，状态码: {response.status_code}")

    # 为了避免被封锁，添加一个小的延迟
    time.sleep(1)

txt_file_path = os.path.join("data", "pittsburgh_events.txt")
with open(txt_file_path, "w", encoding="utf-8") as f:
    for data in all_events:
        f.write(f'"name": "{data["name"]}",\n')
        f.write(f'"startDate": "{data["startDate"]}",\n')
        f.write(f'"endDate": "{data["endDate"]}",\n')
        location = data["location"]
        address = location.get("address", {})
        f.write(f'"location": "{data["location"]["name"]}"\n')
        f.write(f'"streetAddress": "{data["location"]["address"]["streetAddress"]}",\n')
        f.write(f'"addressLocality": "{data["location"]["address"]["addressLocality"]}",\n')
        f.write(f'"addressRegion": "{data["location"]["address"]["addressRegion"]}",\n')
        f.write(f'"postalCode": "{data["location"]["address"]["postalCode"]}",\n')
        f.write(f'"addressCountry": "{data["location"]["address"]["addressCountry"]}"\n\n\n')

print(f"所有页面的数据已保存到 '{txt_file_path}'")
