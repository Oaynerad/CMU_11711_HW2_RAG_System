import requests
from bs4 import BeautifulSoup
import re
import os

URL='https://www.cmu.edu/about/awards.html'
page = requests.get(URL)

bs = BeautifulSoup(page.text, 'html.parser')

content_divs = bs.find_all('div', class_='content')

all_results = []
for div in content_divs:
    h2_text = div.find('h2').get_text(strip=True) if div.find('h2') else ""
    p_texts = [p.get_text(strip=True) for p in div.find_all('p')]
    # 存储每个div提取出的h2和p的文本内容
    all_results.append({
        'h2': h2_text,
        'paragraphs': p_texts
    })

if not os.path.exists("data"):
    os.makedirs("data")

file_path = os.path.join("data", "cmu_awards.txt")

# 确保data文件夹存在
os.makedirs("data", exist_ok=True)

with open(file_path, "w", encoding="utf-8") as file:
    for result in all_results:
        file.write(result['h2'] + "\n")
        for paragraph in result['paragraphs']:
            file.write(paragraph + "\n")
        file.write("\n\n\n")  # 每个div的内容之间加两个空行

print("文本已保存到 cmu_awards.txt")