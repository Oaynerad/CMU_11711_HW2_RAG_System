import json
import os
from datetime import datetime

# 读取文件
path = "scrape_ruike/"
path_tail = "_event_visitpittsburgh.txt"


# 解析 events 数据
for i in range(1,6):
    
    file_path = f"{path}{i}{path_tail}"
    
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        
    events = []
    for result in data.get("results", []):  # 遍历 results 数组
        for event in result.get("hits", []):  # 访问每个 results 内部的 hits
            event_info = {
                "Title": event.get("title", "N/A"),
                "Category": ", ".join(event.get("eventCategories", [])),
                "Start Date": event.get("startDate", "N/A"),
                "End Date": event.get("endDate", "N/A"),
                "Address": ", ".join(event.get("address", [])) if event.get("address") else "N/A",
                "Phone": event.get("phone", "N/A"),
                "Website": event.get("website", "N/A")
            }
            events.append(event_info)
            
    txt_file_path = os.path.join("data", "events_visitpittsburgh.txt")
    with open(txt_file_path, "w", encoding="utf-8") as f:
        for event in events:
            try:
                start_date = datetime.utcfromtimestamp(int(event["Start Date"])).strftime('%Y-%m-%d')
            except ValueError:
                start_date = "N/A"

            try:
                end_date = datetime.utcfromtimestamp(int(event["End Date"])).strftime('%Y-%m-%d')
            except ValueError:
                end_date = "N/A"
            # 写入基本事件信息
            f.write(f'"name": "{event["Title"]}",\n')
            f.write(f'"startDate": "{start_date}",\n')
            f.write(f'"endDate": "{end_date}",\n')

            # 处理地址信息
            address_parts = event["Address"].split(", ") if event["Address"] != "N/A" else []
            location_name = address_parts[0] if address_parts else "Unknown Location"
            street_address = address_parts[1] if len(address_parts) > 1 else "N/A"
            address_locality = address_parts[2] if len(address_parts) > 2 else "N/A"
            address_region = address_parts[3] if len(address_parts) > 3 else "N/A"
            postal_code = address_parts[4] if len(address_parts) > 4 else "N/A"
            address_country = "USA"  # 假设所有地址都在美国

            # 写入地址信息
            f.write(f'"location": "{location_name}",\n')
            f.write(f'"streetAddress": "{street_address}",\n')
            f.write(f'"addressLocality": "{address_locality}",\n')
            f.write(f'"addressRegion": "{address_region}",\n')
            f.write(f'"postalCode": "{postal_code}",\n')
            f.write(f'"addressCountry": "{address_country}"\n\n\n')

print("All done")