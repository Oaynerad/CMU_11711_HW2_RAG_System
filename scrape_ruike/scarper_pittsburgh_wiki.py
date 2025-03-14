import requests
from bs4 import BeautifulSoup
import re
import os

wiki_URL='https://en.wikipedia.org/wiki/Pittsburgh'
page = requests.get(wiki_URL)

bs = BeautifulSoup(page.text, 'html.parser')

content_div = bs.find('div', class_='mw-content-ltr mw-parser-output')
paragraphs = content_div.find_all('p') if content_div else []

div_col = bs.find_all('div', class_='div-col')
div_col_paragraphs = div_col[1].find_all('li')

if not os.path.exists("data"):
    os.makedirs("data")

file_path = os.path.join("data", "pittsburgh_wiki.txt")
with open(file_path, "w", encoding="utf-8") as file:
    for p in paragraphs:
        text = re.sub(r'\[\d+\]', '', p.text)  # 去除 [数字]
        file.write(text + "\n\n")

    # 处理 'div-col' 里的内容
    for li in div_col_paragraphs:
        text = re.sub(r'\[\d+\]', '', li.text)  # 处理列表项
        file.write(text + "\n\n")

print("文本已保存到 pittsburgh_wiki.txt")
