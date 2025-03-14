'''
    Auther: Ruike Chen
'''

import requests
from bs4 import BeautifulSoup
import os

URL='https://www.cmu.edu/engage/alumni/events/campus/index.html'
page = requests.get(URL)

bs = BeautifulSoup(page.text, 'html.parser')

content_div = bs.find('div', class_='grid column3 darkgrey boxes js-list')
paragraphs = content_div.find_all('p') if content_div else []

if not os.path.exists("data"):
    os.makedirs("data")

file_path = os.path.join("data", "cmu_events_page.txt")
with open(file_path, "w", encoding="utf-8") as file:
    for p in paragraphs:
        file.write(p.text + "\n\n")
        
print("文本已保存到cmu_event_page.txt")
