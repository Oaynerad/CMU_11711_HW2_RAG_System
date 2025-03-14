import requests
from bs4 import BeautifulSoup
import json
import os
def scrape_food_festivals(url):
    """爬取所有 Pittsburgh 餐饮节信息"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # 查找所有餐饮节活动的模块
    event_blocks = soup.find_all("div", class_="block text text--default layout")

    for event_block in event_blocks:
        # 获取活动标题
        title_tag = event_block.find("h2", class_="text_heading")
        title = title_tag.text.strip() if title_tag else "Unknown Title"
        title_2 = event_block.find("h3", class_="text_text")
        # 获取活动日期
        date_tag = event_block.select_one(".split-content-embed-code__intro em")
        date_info = date_tag.text.strip() if date_tag else "Unknown Date"

        # 获取活动描述
        description_tag = event_block.select_one(".split-content-embed-code__intro p:nth-of-type(2)")
        description = description_tag.text.strip() if description_tag else "No description available"

        # 获取官网链接
        link_tag = event_block.select_one(".split-content-embed-code__intro a")
        website = link_tag["href"] if link_tag else "No website available"

        # 存储活动信息
        event_data = {
            "title": title,
            "dates": date_info,
            "description": description,
            "website": website
        }
        events.append(event_data)

    return events


# **测试爬取多个餐饮节**
url = "https://www.visitpittsburgh.com/events-festivals/food-festivals/"  # 替换为实际URL
food_festivals = scrape_food_festivals(url)

def save_to_txt(data, filename="events.txt"):
    """将爬取到的数据保存为 TXT 文件"""
    os.makedirs("data", exist_ok=True)  # 确保 data 目录存在
    file_path = os.path.join("data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        for event in data:
            f.write(f"Title: {event['title']}\n")
            f.write(f"Date: {event['dates']}\n")
            f.write(f"Description: {event['description']}\n\n\n")

    print(f"Data saved to {file_path}")

save_to_txt(food_festivals, filename="food_festivals.txt")