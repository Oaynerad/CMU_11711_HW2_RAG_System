import requests
from bs4 import BeautifulSoup
import os
def scrape_events(url):
    """抓取单个网页的所有活动信息，处理 recurring events"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"请求失败: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    for event_card in soup.find_all("article", class_="event-card"):
        # 获取标题
        title_tag = event_card.find("h2")
        title = title_tag.text.strip() if title_tag else "Unknown Title"

        # 处理 recurring events
        start_date = event_card.get("data-event-start", "Unknown Start Date")
        end_date = event_card.get("data-event-end", "Unknown End Date")

        if end_date == "Jan 1, 1970":
            # 说明是 recurring event，读取 <div class="event-card__date"> 内文本
            date_tag = event_card.find("div", class_="event-card__date")
            end_date = date_tag.text.strip() if date_tag else "Recurring Event"

        # 获取场馆信息
        venue_tag = event_card.find("div", class_="event-card__venue")
        venue = venue_tag.text.strip() if venue_tag else "Unknown Venue"

        # 获取活动类别
        category_tags = event_card.find_all("a", class_="event-card__event-type")
        categories = [cat.text.strip() for cat in category_tags] if category_tags else []

        # 存储活动信息
        event_data = {
            "title": title,
            "start_date": start_date,
            "end_date": end_date,
            "venue": venue,
            "categories": categories
        }
        events.append(event_data)

    return events


# 测试爬取单个页面
url = "https://carnegiemuseums.org/events/page/3/"
events = scrape_events(url)

# 打印结果

def save_to_txt(data, filename="events.txt"):
    """将爬取到的数据保存为 TXT 文件"""
    os.makedirs("data", exist_ok=True)  # 确保 data 目录存在
    file_path = os.path.join("data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        for event in data:
            f.write(f"Title: {event['title']}\n")
            f.write(f"Start Date: {event['start_date']}\n")
            f.write(f"End Date: {event['end_date']}\n")
            f.write(f"Venue: {event['venue']}\n")
            f.write(f"Categories: {', '.join(event['categories'])}\n\n\n")

    print(f"Data saved to {file_path}")

save_to_txt(events, filename="Carnegie_Museums_3.txt")