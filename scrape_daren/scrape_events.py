import os
import json

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://trustarts.org/calendar"

def scrape_single_page(page_num=1):
    """抓取单个页码的所有活动信息"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0 Safari/537.36"
        )
    }
    url = f"{BASE_URL}?page={page_num}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    articles = soup.find_all('article', class_=re.compile(r'^event'))
    events_data = []
    for art in articles:
        title_tag = art.find('h3', class_='title')
        title = title_tag.get_text(strip=True) if title_tag else ''
        link = title_tag.find('a').get('href', '') if title_tag else ''
        
        time_tag = art.find('time', class_='range')
        date_text = time_tag.get_text(strip=True) if time_tag else ''
        
        venue_tag = art.find('div', class_='venue')
        venue = venue_tag.get_text(strip=True) if venue_tag else ''
        
        org_tag = art.find('div', class_='organization')
        organization = org_tag.get_text(strip=True) if org_tag else ''
        
        category_tags = art.select('ul.category-group li.category')
        categories = [c.get_text(strip=True) for c in category_tags]
        # JSON file
        events_data.append({
            'title': title,
            'url': link,
            'date': date_text,
            'venue': venue,
            'organization': organization,
            'categories': categories
        })
        # txt file

    return events_data
def save_to_txt(data, filename="events.txt"):
    """将爬取到的数据保存为 TXT 文件"""
    os.makedirs("data", exist_ok=True)  # 确保 data 目录存在
    file_path = os.path.join("data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        for event in data:
            f.write(f"Title: {event['title']}\n")
            f.write(f"Date: {event['date']}\n")
            f.write(f"Venue: {event['venue']}\n")
            f.write(f"Organization: {event['organization']}\n")
            f.write(f"Categories: {', '.join(event['categories'])}\n")
            f.write(f"URL: {event['url']}\n\n\n")


    print(f"Data saved to {file_path}")



def scrape_all_pages(max_page=6):
    """循环从1抓到max_page"""
    all_events = []
    for page in range(1, max_page + 1):
        print(f"Scraping page {page}...")
        events = scrape_single_page(page)
        all_events.extend(events)
    return all_events

if __name__ == "__main__":
    events = scrape_all_pages(max_page=6)  # 假设有6页
    print(f"Total events found: {len(events)}")
    save_to_txt(events,'events_Pitt_Cultral_TRUST.txt')  # 存储数据
