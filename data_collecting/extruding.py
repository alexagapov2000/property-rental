import requests
import time
from bs4 import BeautifulSoup
import re
import time
import random
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

#url = "https://realt.by/rent/flat-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&category=2&isNotAgency=true&leasePeriod=999&page=2&rooms=1&sortType=minPrice"
#url = "https://realt.by/rent/cottage-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&page=1"
url = "https://realt.by/rent/flat-for-long/?page=50"
response = requests.get(url, headers=headers)

print(response.status_code)
response.raise_for_status()
with open("./test_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "lxml")

# cards = soup.find_all("div", class_="flex flex-col w-full h-full p-5")
cards = soup.select('div[data-index*=""]')
print(f"Cards number: {len(cards)}")

for card in cards:
    # price = card.select_one("span.text-title.font-semibold").text
    # address = card.select_one("p.text-basic.w-full.text-subhead").text.strip()
    # container = card.select_one("p.flex.flex-wrap.text-headline")
    # spans = container.select("span")
    # rooms = spans[0].text.strip()
    # area = spans[1].text.strip()
    # floor = spans[2].text.strip()
    id = card.select_one('a[href*="/rent-flat-for-long/object/"]')['href'];
    full_href = f"https://realt.by{id}"
    response = requests.get(full_href, headers=headers)
    delay = random.uniform(0.5, 1.5)
    time.sleep(delay)
    # print(price, address, rooms, area, floor, id, sep='; ')
    print(f"{delay}")
    print(json.dumps(dict(response.headers), indent=4))
    print(response.headers.get("X-RateLimit-Remaining"))