'''
    Auther: Ruike Chen
'''

import requests
import os
import calendar
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

def scarper(url):
    print(f"正在爬取: {url}")
    # 发送请求
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        all_events = data.get("events", []) 
    else:
        print(f"无法访问 {url}，状态码: {response.status_code}")

    # 为了避免被封锁，添加一个小的延迟
    return all_events

if __name__ == "__main__":
    
    base_url = "https://events.cmu.edu/live/calendar/view/day/date/2025"
    base_url_tail= "?user_tz=America%2FDetroit&template_vars=id,latitude,longitude,location,time,href,image_raw,title_link,summary,until,is_canceled,is_online,image_src,repeats,is_multi_day,is_first_multi_day,multi_day_span,tag_classes,category_classes,has_map&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22hide_repeats%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_groups%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_locations%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_tags%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22month_view_day_limit%22%3E2%3C%2Farg%3E%3Carg%20id%3D%22use_tag_classes%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22search_all_events_only%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22use_modular_templates%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22display_all_day_events_last%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3Eexclude%20from%20main%20calendar%3C%2Farg%3E%3C%2Fwidget%3E"
    all_events = []

    for month in range(3, 13):
        _, days_in_month = calendar.monthrange(2025, month)
        if month == 3:
            for day in range(20, days_in_month +1):
                url = f"{base_url}03{day}{base_url_tail}"
                events_sub = scarper(url)
                all_events.extend(events_sub)
    
        elif month in range(4, 10):
            for day in range(1, days_in_month +1 ):  
                if day in range (1, 10):
                    url = f"{base_url}0{month}0{day}{base_url_tail}"
                else :
                    url = f"{base_url}0{month}{day}{base_url_tail}"  # 构造 URL
                events_sub = scarper(url)
                all_events.extend(events_sub)
        
        elif month in range(10, 13):
            for day in range(1, days_in_month +1 ):  
                if day in range (1, 10):
                    url = f"{base_url}{month}0{day}{base_url_tail}"
                else :
                    url = f"{base_url}{month}{day}{base_url_tail}"
                events_sub = scarper(url)
                all_events.extend(events_sub)

    txt_file_path = os.path.join("data", "cmu_events.txt")
    with open(txt_file_path, "w", encoding="utf-8") as file:
        for event in all_events:
            ts_start = event.get('ts_start')
            if ts_start is None:
                print(f"跳过无效事件: {event.get('title', '未知标题')}")
                continue  # 如果没有开始时间，跳过该事件

            start = datetime.fromtimestamp(ts_start, pytz.timezone(event.get('tz', 'America/New_York')))
            ts_end = event.get('ts_end', ts_start)  # 处理缺少 ts_end 的情况
            end = datetime.fromtimestamp(ts_end, pytz.timezone(event.get('tz', 'America/New_York')))

            file.write(f'"title": "{event.get("title", "未知标题")}",\n')
            file.write(f'"startDate": "{start.isoformat()}",\n')
            file.write(f'"endDate": "{end.isoformat()}",\n')
            file.write(f'"timezone": "{event.get("tz", "America/New_York")}",\n')
            file.write(f'"location": "{event.get("location", "未知地点")}",\n')

            # 解析 HTML，提取摘要内容
            summary_html = event.get('summary', '')
            summary_text = BeautifulSoup(summary_html, 'html.parser').get_text(strip=True)
            if summary_text:
                file.write(f'"description": "{summary_text}",\n')

            # 处理重复信息
            repeats = event.get('custom_event_repeats', '')
            if repeats:
                file.write(f'"repeats": "{repeats}"\n')

            file.write("\n\n")  # 每个事件之间空两行

    print(f"所有页面的数据已保存到 '{txt_file_path}'")
