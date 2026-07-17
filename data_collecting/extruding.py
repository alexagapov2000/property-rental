import requests
import time
from bs4 import BeautifulSoup
import re

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

for i, card in enumerate(cards):
    print(f"\n--- АНАЛИЗ КАРТОЧКИ №{i+1} ---")
    
    # ТЕСТ 1: Пробуем найти через CSS-селектор по ОДНОМУ классу
    price_el = card.select_one("span.text-title")
    
    # ТЕСТ 2: Пробуем найти вообще любой тег, содержащий "р./мес." во всей карточке
    price_by_text = card.find(string=re.compile(r"р\./мес\."))
    
    if price_el:
        print(f"Тест 1 (Класс) СРАБОТАЛ: {price_el.text.strip()}")
    else:
        print("Тест 1 (Класс) ВЫДАЛ NONE")
        
    if price_by_text:
        print(f"Тест 2 (Текст) СРАБОТАЛ: {price_by_text.strip()}")
    else:
        print("Тест 2 (Текст) ВЫДАЛ NONE")
        
    # ЕСЛИ ОБА NONE: выводим кусок HTML этой карточки, чтобы понять, что пошло не так
    if not price_el and not price_by_text:
        print("КРИТИЧЕСКАЯ ОШИБКА: BeautifulSoup не видит цену в этой карточке вообще.")
        # Выведет первые 500 символов внутренностей карточки
        print("Вот что внутри карточки на самом деле:")
        print(card.prettify()[:500]) 
        break # Останавливаем цикл на первой проблемной карточке


for card in cards:
    #price = card.find("span", class_="text-title font-semibold").text.strip()
    price = card.select_one("text-title font-semibold")
    address = card.find("p", class_="text-basic w-full text-subhead md:text-body").text.strip()
    # rooms = card.find("span", class_="flex flex-wrap text-headline items-center font-semibold md:font-bold -mr-2 -order-2 md:-order-none mb-2  md:mb-4")
    container = card.find(class_=lambda x: x and "flex flex-wrap text-headline" in x)
    spans = container.find_all("span")
    rooms = spans[0].text.strip()
    area = spans[1].text.strip()
    floor = spans[2].text.strip()
    href = card.find(class_="z-1 absolute top-0 left-0 w-full h-full cursor-pointer").href;
    print(price, address, rooms, area, floor, end='; ')
    print()