import re
from typing import List

import requests
from bs4 import BeautifulSoup

from helpers.base_url import BASE_URL


def get_subcategory_in_category(url: str) -> List:

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    subcategories = soup.find_all("div", class_=re.compile("category__item-title"))

    return subcategories


def new_subcategory(subcategories: List) -> List:

    for subcat in subcategories:
        subcat_url = subcat.a["href"]
        new_subcat = get_subcategory_in_category(BASE_URL+subcat_url)
        if new_subcat:
            return new_subcat


def subcategory(url: str, count: int = 1) -> List:
    i = 1
    subcategories = get_subcategory_in_category(url)
    while True:
        if not new_subcategory(subcategories) or i > count:
            break
        else:
            subcategories = new_subcategory(subcategories)
            i += 1

    return subcategories
