import requests
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = "https://realt.by/rent/flat-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&category=2&isNotAgency=true&leasePeriod=999&page=2&rooms=1&sortType=minPrice"
response = requests.get(url, headers=headers)

print(response.status_code)  # должно быть 200
# with open("./test_page.html", "w", encoding="utf-8") as f:
#     f.write(response.text)


soup = BeautifulSoup(response.text, "lxml")

# Примерная структура — нужно смотреть реальные классы на сайте!
cards = soup.find_all("div", class_="flex flex-col w-full h-full p-5")  # замени на реальный класс

for card in cards:
    try:
        price = card.find("span", class_="text-title font-semibold text-info-500").text.strip()
        address = card.find("div", class_="address").text.strip()
        rooms = card.find("span", class_="rooms").text.strip()
        print(price, address, rooms)
    except AttributeError:
        continue  # пропускаем карточки с неполными данными
