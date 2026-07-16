import requests
import time
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = "https://realt.by/rent/flat-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&category=2&isNotAgency=true&leasePeriod=999&page=2&rooms=1&sortType=minPrice"
url = "https://realt.by/rent/cottage-for-long/?addressV2=%5B%7B%22townUuid%22%3A%224cb07174-7b00-11eb-8943-0cc47adabd66%22%7D%5D&page=1"
url = "https://realt.by/rent/flat-for-long/"
response = requests.get(url, headers=headers)

print(response.status_code)  # должно быть 200
with open("./test_page.html", "w", encoding="utf-8") as f:
    f.write(response.text)


soup = BeautifulSoup(response.text, "lxml")

# Примерная структура — нужно смотреть реальные классы на сайте!
cards = soup.find_all("div", class_="flex flex-col w-full h-full p-5")  # замени на реальный класс

for card in cards:
    #try
        price = card.find("span", class_="text-title font-semibold text-info-500").text.strip()
        address = card.find("p", class_="text-basic w-full text-subhead md:text-body").text.strip()
        # rooms = card.find("span", class_="flex flex-wrap text-headline items-center font-semibold md:font-bold -mr-2 -order-2 md:-order-none mb-2  md:mb-4")
        container = card.find(class_=lambda x: x and "flex flex-wrap text-headline" in x)
        spans = container.find_all("span")
        rooms = spans[0].text.strip()
        area = spans[1].text.strip()
        floor = spans[2].text.strip()
        print(price, address, rooms, area, floor, end='; ')
        print()
    #except AttributeError:
    #    continue  # пропускаем карточки с неполными данными
