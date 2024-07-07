import requests
from bs4 import BeautifulSoup
import json

url = "https://minfin.com.ua/articles/"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

news_items = soup.find_all("li", class_="item")[:7]

news_data = []

for idx, item in enumerate(news_items):
    date = item.find("span", class_="data").text.strip()
    title = item.find("span", class_="link").text.strip()
    url = 'https://minfin.com.ua'+item.find("a")["href"]

    news_item = {
        "title": title,
        "data": date,
        "url": url
    }
    news_data.append(news_item)

with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)

print("JSON file 'news_data.json' has been created successfully with the parsed news.")
