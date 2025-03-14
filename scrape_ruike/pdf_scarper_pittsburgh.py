from pypdf import PdfReader
import requests
import io
import os
import re

if not os.path.exists("data"):
    os.makedirs("data")
    
pdf_url= {
    'amusement tax':('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9622_amusement_tax_regulations.pdf', 3),
    'payroll tax': ('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9626_payroll_tax_regulations.pdf', 2),
    'institution and service privilege tax' : ('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9623_isp_tax_regulations.pdf', 4),
    'local services tax' : ('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9624_local_services_tax_regulations.pdf', 3),
    'parking tax': ('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9625_parking_tax_regulations.pdf', 3),
    'non-resident sports facility tax': ('https://www.pittsburghpa.gov/files/assets/city/v/1/finance/documents/tax-forms/9627_uf_regulations.pdf', 3),
    '2024 budget operation': ('https://apps.pittsburghpa.gov/redtail/images/23255_2024_Operating_Budget.pdf', 6)
}

for filename, (url, start_page) in pdf_url.items():
    print(f"正在处理 {filename} ...")
    
    reponse = requests.get(url, verify= False)
    pdf_stream = io.BytesIO(reponse.content)

    reader = PdfReader(pdf_stream)
    number_of_pages = len(reader.pages)

    text_content = []

    for i in range(start_page, number_of_pages):
        page = reader.pages[i]
        page_text = page.extract_text()

        # 使用正则表达式以换行或段落标记进行分割，再过滤空白的段落
        page_paragraphs = [para.strip() for para in re.split(r'\n\s*\n+', page_text) if para.strip()]
        
        # 收集段落
        text_content.extend(page_paragraphs)

    file_path = os.path.join("data", f"{filename}.txt")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n\n\n".join(text_content))

    print(f"清理后的文本已保存到 {file_path}")
    
print("所有 PDF 处理完成！ 🚀")