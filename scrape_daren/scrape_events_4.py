import requests
from bs4 import BeautifulSoup
import re

def scrape_blocks_starting_with_block_text(url, max_length=300):
    """
    1) 抓取页面中所有 <div>，class 属性 以 'block text text--default' 开头。
    2) 提取其纯文本，并自动按句子/标点进行拆分，保证每段 <= max_length 字符。
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 如果状态码不是200，抛出异常
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 1. 使用CSS选择器： 匹配 div，其 class 属性 以 'block text text--default' 开头
    blocks = soup.select("div[class^='block text text--default']")
    
    # 2. 收集所有块的“完整文本”，存进列表
    all_text_blocks = []
    for block in blocks:
        text_content = block.get_text(separator="\n", strip=True)
        # 如果需要先做一些清理（如去掉多余换行、空白等），可以在此进行
        all_text_blocks.append(text_content)

    # 3. 进一步把每个大文本拆分成更小的 chunk
    all_chunks = []
    for big_text in all_text_blocks:
        chunks = split_into_sentences(big_text, max_length)
        all_chunks.extend(chunks)
    
    return all_chunks


def split_into_sentences(text, max_length=300):
    """
    按句子/标点切分文本，再合并成 chunk，每个chunk长度不超过 max_length。
    你可以根据需要调整。
    """
    # 用正则按句号、问号、叹号等分割
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    
    chunks = []
    current_chunk = ""
    for s in sentences:
        if len(current_chunk) + len(s) <= max_length:
            current_chunk += (s + " ")
        else:
            # 当前chunk已达max_length，先存起来
            chunks.append(current_chunk.strip())
            current_chunk = s + " "

    # 别忘了最后剩余的一段
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ============== 测试用 ==============
if __name__ == "__main__":
    test_url = "http://visitpittsburgh.com/things-to-do/pittsburgh-sports-teams/"  # 替换为实际网址
    chunks_data = scrape_blocks_starting_with_block_text(test_url, max_length=250)
import os
def save_to_txt(data, filename="events.txt"):
    """将爬取到的数据保存为 TXT 文件"""
    os.makedirs("data", exist_ok=True)  # 确保 data 目录存在
    file_path = os.path.join("data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        for event in data:

            f.write(f"{event}\n\n")

    print(f"Data saved to {file_path}")

save_to_txt(chunks_data, filename="Sports.txt")
