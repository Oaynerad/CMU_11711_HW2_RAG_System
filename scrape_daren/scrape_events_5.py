import re
from bs4 import BeautifulSoup

def scrape_mlb_schedule_from_file():
    with open("schedule_pirates_SEP.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # 拿到所有比赛容器 div
    # 注意：这行用的正则跟以前一样，也可以根据你的实际情况再微调
    game_divs = soup.find_all(
        "div", 
        class_=re.compile(r"list-mode-table-wrapper list-wrapper-\d+.*tracking-game-data")
    )

    all_games = []

    # 遍历每个比赛容器
    for game_div in game_divs:
        # 找到该容器下的所有表格（而不是只找第一个）
        tables = game_div.find_all("table")

        # 遍历每个表格，因为一个 game_div 里可能有多场比赛
        for table in tables:
            # 把想要的<td>都找出来
            date_td = table.find("td", class_="date-td")
            matchup_td = table.find("td", class_="matchup-td")
            time_td = table.find("td", class_="time-or-score-td-large")

            # 尝试获取日期
            month_date = ""
            weekday = ""
            if date_td:
                md_elem = date_td.find("div", class_="month-date")
                month_date = md_elem.get_text(strip=True) if md_elem else ""
                wd_elem = date_td.find("div", class_="weekday")
                weekday = wd_elem.get_text(strip=True) if wd_elem else ""

            # 尝试获取两队名称
            away_team_name = ""
            home_team_name = ""
            if matchup_td:
                away_elem = matchup_td.find("div", class_="xref-away-name")
                away_team_name = away_elem.get_text(strip=True) if away_elem else ""
                opp_elem = matchup_td.find("div", class_="opponent-name")
                home_team_name = opp_elem.get_text(strip=True) if opp_elem else ""

            # 尝试获取开球时间
            start_time = ""
            if time_td:
                time_link = time_td.find("a", class_="time")
                if time_link:
                    primary_time_div = time_link.find("div", class_="primary-time")
                    start_time = primary_time_div.get_text(strip=True) if primary_time_div else ""

            # 整合到一个dict
            if (away_team_name or home_team_name or start_time):
                game_info = {
                    "date": f"{month_date} ({weekday})",
                    "Pirates playing against": home_team_name,
                    "start_time": start_time
                }
                all_games.append(game_info)

    return all_games
import os
def save_to_txt(data, filename="events.txt"):
    """将爬取到的数据保存为 TXT 文件"""
    os.makedirs("data", exist_ok=True)  # 确保 data 目录存在
    file_path = os.path.join("data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        for event in data:
            f.write(f"date: {event['date']}\n")
            f.write(f"Pirates playing against: {event['Pirates playing against']}\n")
            f.write(f"start time: {event['start_time']}\n\n\n")

    print(f"Data saved to {file_path}")



if __name__ == "__main__":
    games_data = scrape_mlb_schedule_from_file()
    save_to_txt(games_data, filename="schedule_pirates_9.txt")