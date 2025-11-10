import requests
from bs4 import BeautifulSoup

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
