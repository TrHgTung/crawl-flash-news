import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
import schedule
import time
from datetime import datetime
import pytz  # để dùng múi giờ Việt Nam

# lấy biến môi trường từ file .env
load_dotenv()

# get SHEET_ID từ .env
SHEET_ID = os.getenv("SHEET_ID")

# kết nối với GG sheet
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(creds)

# cấu hình trong file shêt
sheet = client.open_by_key(SHEET_ID).sheet1

# crawl datâ
def crawl_news():
    # Lấy danh sách title đã có để chống trùng
    existing_titles = sheet.col_values(1)  # cột A phải là Title: nó sẽ kiểm tra dữ liệu tin tức trong cột A của file Gg sheet

    url = 'https://vi.theblockbeats.news/newsflash'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tìm tất cả các khối tin tức
        news_items = soup.find_all('div', class_='news-flash-wrapper')

        new_count = 0

        for item in news_items:
            title = item.find('div', class_='news-flash-title-text')
            content = item.find('div', class_='news-flash-item-content')

            title_text = title.get_text(strip=True) if title else "Không có tiêu đề tin nhanh"
            content_text = content.get_text(" ", strip=True) if content else "Nội dung được tạo bởi NivexHub"
            # nếu nội dung có chứa BlockBeats thì thay bằng NivexHub
            content_text = content_text.replace("BlockBeats", "NivexHub")
            # Lấy thời gian hiện tại (múi giờ Việt Nam)
            vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
            current_time = datetime.now(vn_tz).strftime("%Y-%m-%d %H:%M:%S")

            # kiểm tra chống trùng : bỏ qua bài tin nếu title đã tồn tại trong file gg shêt
            if title_text in existing_titles:
                continue

            print("Tiêu đề:", title_text)
            print("Nội dung:", content_text)
            print("Thời gian:", current_time)
            print()

            sheet.append_row([title_text, content_text, current_time])

# tự đôgnj chạy mỗi 3 tiếng
schedule.every(3).hours.do(crawl_news)

print("Tryng to crawl new data...")
crawl_news()  # chạy lần đầu tiên ngay khi start container

while True:
    schedule.run_pending()
    time.sleep(60)
