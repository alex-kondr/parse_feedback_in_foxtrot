from typing import List

import requests
from bs4 import BeautifulSoup


def get_categories(url: str) -> List:

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    categories = soup.find_all("div", class_='catalog__category-item__wrap')

    return categories
