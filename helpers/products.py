import re
from typing import List

import requests
from bs4 import BeautifulSoup


def get_products(url: str) -> List:
    print("get_products_url: ", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find_all("div", class_="card__body")
    return products


def get_product_name(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    product_name = (
        soup.find("h2", class_="page__title nowrap js-toggle-card-box")
            .label
            .text
            .replace("/", "_")
            .replace('"', "")
            .strip()
    )

    return product_name


def get_comments(url: str) -> List:
    print("product_url: ", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    comments = []

    all_comments = soup.find("div", class_=re.compile("main-reviews__body"))

    if not all_comments:
        return comments

    all_comments = all_comments.find_all("article")

    for comment in all_comments:
        author_name = comment.find(class_="product-comment__item-title").text.strip()
        grade = comment.find_all("i", class_="icon icon-star-filled icon_orange")
        date = comment.find("div", class_="product-comment__item-date").text.strip()
        text = comment.find("div", class_="product-comment__item-text").text.strip()

        comments.append(
            {
                "title": "",
                "author_name": author_name,
                "url": url,
                "grade": len(grade),
                "date": date,
                "text": text
            }
        )

    return comments


