import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json

base_url_head = "https://downtownpittsburgh.com/events/?n=3&d="
base_url_tail = "&y=2025"

all_events = []
all_texts = []
for page_num in range(20, 31):  
    url = f"{base_url_head}{page_num}{base_url_tail}"  # 构造 URL
    print(f"正在爬取: {url}")

    # 发送请求
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # 检查请求是否成功
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, "html.parser")
        
        div = bs.find("div", class_="column60")
        
        # 这里你可以提取所需数据，例如所有的活动标题
        scripts = div.find_all("script", {"type": "application/ld+json"})
        
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

url_base_month_head = 'https://downtownpittsburgh.com/events/?n='
url_base_month_tail = '&y=2025&cat=0'
for page_num in range(4, 12):  
    url = f"{url_base_month_head}{page_num}{url_base_month_tail}"  # 构造 URL
    print(f"正在爬取: {url}")

    # 发送请求
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    # 检查请求是否成功
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, "html.parser")
        
        div = bs.find("div", class_="column60")
        
        
        # 这里你可以提取所需数据，例如所有的活动标题
        scripts = div.find_all("script", {"type": "application/ld+json"})
        
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

txt_file_path = os.path.join("data", "downtownpittsburgh_events.txt")
with open(txt_file_path, "w", encoding="utf-8") as f:
    for descrition, data in zip(all_texts, all_events):
        f.write(f'"name": "{data["name"]}",\n')
        f.write(f'"startDate": "{data["startDate"]}",\n')
        f.write(f'"address": "{data["location"]["address"]}",\n\n\n')

print(f"所有页面的数据已保存到 '{txt_file_path}'")
