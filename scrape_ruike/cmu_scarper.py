'''
    Auther: Ruike Chen
    
'''

import requests
from bs4 import BeautifulSoup
import os

class_name_1=['content', 
            'grid column2 grey js-list', 
            'grid column2 blue invert globe js-list',
            'grid column4 boxes js-list',
            'js-flickityCustom gold',
            'grid column4 photos js-list'
            ]

class_name_2=['grid column2 js-list',
              'grid column2 grey js-list']

class_name_3=['content',
              'grid column2 blue boxes js-list']
urls = {
    "about": ("https://www.cmu.edu/about/index.html", class_name_1),
    "leadership": ("https://www.cmu.edu/leadership/", "content"),
    "Vision,mission,value": ("https://www.cmu.edu/about/mission.html", "content"),
    "history": ("https://www.cmu.edu/about/history.html", class_name_2),
    "traditions": ("https://www.cmu.edu/about/traditions.html",class_name_3),
    "rankings": ("https://www.cmu.edu/about/rankings.html", "content"),
}

for file_name, (url, class_name) in urls.items():

    response = requests.get(url)

    bs = BeautifulSoup(response.text, 'html.parser')

    content_divs = bs.find_all('div', class_=class_name)

    # 结果存储
    extracted_content = {}

    # 遍历找到的 div
    for div in content_divs:
        div_class = " ".join(div.get("class", []))  # 获取 div 的 class 名称
        extracted_text = ""

        # 针对不同 class 进行不同的提取逻辑
        if "content" in div_class:
            h1_text = "\n".join([h1.text.strip() for h1 in div.find_all('h1')])  # 提取所有 h1
            p_text = "\n".join([p.text.strip() for p in div.find_all('p')])  # 提取所有 p
            extracted_text = f"{h1_text}\n\n{p_text}"  # 合并 h1 和 p

        elif "grid column2 js-list" in div_class:
            h1_text = "\n".join([h1.text.strip() for h1 in div.find_all('h1')])  # 提取所有 h1
            p_text = "\n".join([p.text.strip() for p in div.find_all('p')])  # 提取所有 p
            li_text = "\n".join([li.text.strip() for li in div.find_all('li')]) 
            extracted_text = f"{h1_text}\n\n{p_text}\n\n{li_text}"
            
        elif "grid column2 grey js-list" in div_class:
            if file_name == "about_cmu":
                # 2. 提取这个 div 里面所有其他 <div> 的文本
                all_div_text = "\n".join([d.text.strip() for d in div.find_all('div')])

                extracted_text = f"{all_div_text}"
                
            else:
                h1_text = "\n".join([h1.text.strip() for h1 in div.find_all('h1')])
                p_text = "\n".join([p.text.strip() for p in div.find_all('p')])
                li_text = "\n".join([li.text.strip() for li in div.find_all('li')]) 
                extracted_text = f"{h1_text}\n\n{p_text}\n\n{li_text}"

        elif "grid column2 blue invert globe js-list" in div_class:
            in_pitts = div.find('div', id='in-pittsburgh')
            h2_text_in_pitts = "\n".join([h2.text.strip() for h2 in in_pitts.find_all('h2')]) if in_pitts else ""
            p_text_in_pitts = "\n".join([p.text.strip() for p in in_pitts.find('p')])
            
            # 2. 提取这个 div 里面所有其他 <div> 的文本
            around = div.find('div', id='around-the-globe')
            h2_text_around = "\n".join([h2.text.strip() for h2 in around.find_all('h2')]) if around else ""
            p_text_around = "\n".join([p.text.strip() for p in around.find('p')])

            # 组合结果
            extracted_text = f"{h2_text_in_pitts}\n\n{p_text_in_pitts}\n\n{h2_text_around}\n\n{p_text_around}"

        elif "grid column4 boxes js-list" in div_class:
            extracted_text = "\n".join([h2.text.strip() for h2 in div.find_all('h2')])  # 提取所有 <h2> 作为标题

        elif "js-flickityCustom gold" in div_class:
            extracted_text = "\n".join([p.text.strip() for p in div.find_all('p')])  # 提取图片 alt 信息

        elif "grid column4 photos js-list" in div_class:
            h2_text_school = "\n".join([h2.text.strip() for h2 in div.find_all('h2')])  # 提取所有 h1
            p_text_school = "\n".join([p.text.strip() for p in div.find_all('p')])  # 提取所有 p
            extracted_text = f"{h2_text_school}\n\n{p_text_school}"  # 合并 h1 和 p
        
        elif "grid column2 blue boxes js-list" in div_class:
            h2_text = "\n".join([h2.text.strip() for h2 in div.find_all('h2')])  # 提取所有 h1
            p_text = "\n".join([p.text.strip() for p in div.find_all('p')])  # 提取所有 p
            extracted_text = f"{h2_text}\n\n{p_text}"  # 合并 h1 和 p

        # 存储结果
        extracted_content[div_class] = extracted_text

    if not os.path.exists("data"):
        os.makedirs("data")

    file_path = os.path.join("data", f"cmu_{file_name}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        for class_name, text in extracted_content.items():
            file.write(text + "\n\n\n")
            
    print(f"提取的内容已保存到 {file_path}")

print("All done!")