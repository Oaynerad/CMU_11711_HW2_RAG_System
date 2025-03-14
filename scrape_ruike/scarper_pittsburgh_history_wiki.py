import requests
from bs4 import BeautifulSoup
import re
import os

wiki_URL='https://en.wikipedia.org/wiki/History_of_Pittsburgh'
page = requests.get(wiki_URL)

bs = BeautifulSoup(page.text, 'html.parser')

content_div = bs.find('div', class_='mw-content-ltr mw-parser-output')
paragraphs = content_div.find_all('p') if content_div else []

if not os.path.exists("data"):
    os.makedirs("data")

file_path = os.path.join("data", "pittsburgh_history_wiki.txt")
with open(file_path, "w", encoding="utf-8") as file:
    for p in paragraphs:
        text = re.sub(r'\[\d+\]', '', p.text)  # 去除 [数字]
        file.write(text + "\n\n")

print("文本已保存到 pittsburgh_history_wiki.txt")