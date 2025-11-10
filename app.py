import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

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
url = 'https://vi.theblockbeats.news/newsflash'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm tất cả các khối tin tức
    news_items = soup.find_all('div', class_='news-flash-wrapper')

    for item in news_items:
        title = item.find('div', class_='news-flash-title-text')
        content = item.find('div', class_='news-flash-item-content')

        title_text = title.get_text(strip=True) if title else "No title"
        content_text = content.get_text(" ", strip=True) if content else "No content"

        print("=== 📰 Tin tức mới ===")
        print("Tiêu đề:", title_text)
        print("Nội dung:", content_text)
        print()

        sheet.append_row([title_text, content_text])
