import requests
from bs4 import BeautifulSoup


url = "https://www.foxtrot.com.ua"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
catalog_category = soup.find_all("div", class_='catalog__category-item__wrap')
smartphone = catalog_category[1].a["href"]

print("first found: ", smartphone)

response = requests.get(url+smartphone)
soup = BeautifulSoup(response.text, "lxml")
category = soup.find_all("div", class_="category__item")
all_phone = category[0].a["href"]
print('all phone: ', all_phone)

response = requests.get(url+all_phone)
soup = BeautifulSoup(response.text, "lxml")
all_smartphone = soup.find_all("div", class_="card__body")
first_smartphone = all_smartphone[0].a["href"]
print("first_smartphone: ", first_smartphone)


