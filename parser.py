from pathlib import Path
import re
from typing import List, Dict
import json

import requests
from bs4 import BeautifulSoup


# all_comments = []


base_url = "https://www.foxtrot.com.ua"


def get_categories(url: str) -> List:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    categories = soup.find_all("div", class_='catalog__category-item__wrap')
    return categories
    # smartphone = catalog_category[1].a["href"]


def get_subcategory_in_category(url: str) -> List:
    # print("first found: ", smartphone)
    # response = requests.get(url+smartphone)
    subcategories_ = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    subcategories = soup.find_all("div", class_=re.compile("category__item-title"))

    if subcategories[0].find_all("div", class_=re.compile("category__item-title")):
        print("RECURSIVE")
        for subcat in subcategories:
            print("RECURSIVE+++++")
            subcat_url = subcat.a["href"]
            subcategories_ += get_subcategory_in_category(base_url+subcat_url)
    else:
        subcategories_ += subcategories

    return subcategories_
    # all_phone = category[0].a["href"]
    # print('all phone: ', all_phone)


def get_products(url: str) -> List:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    products = soup.find_all("div", class_="card__body")
    return products
    # first_smartphone = all_smartphone[0].a["href"]
    # print("first_smartphone: ", first_smartphone)


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

    # print(f"product_name: ", product_name)

    return product_name


def get_comments(url: str) -> List:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    comments = []

    all_comments = soup.find("div", class_=re.compile("comments-container"))

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


def save_all_comments(path: Path, comments: List[Dict]) -> None:
    with open(f"{path}.json", mode="w", encoding="utf-8") as fd:
        json.dump(comments, fd, ensure_ascii=False)


def main():
    categories = get_categories(base_url)
    print("len categories: ", len(categories))

    for i, category in enumerate(categories[1:3]):
        category_url = category.a["href"]
        print("category: ", category.a.text)
        subcategories = get_subcategory_in_category(base_url+category_url)

        print(f"len subcategories+{i}: ", len(subcategories))

        for j, subcategory in enumerate(subcategories[:3]):
            # print(f"{subcategory=}")
            subcategory_url = subcategory.a["href"]
            subcategory_name = subcategory.a.text
            path = Path("reviews").joinpath(subcategory_name)
            path.mkdir(exist_ok=True)
            products = get_products(base_url+subcategory_url)

            print(f"len products+{j}: ", len(products))

            for k, product in enumerate(products[:3]):
                product_url = product.a["href"]
                product_name = get_product_name(base_url+product_url)
                comments_url = base_url + product_url[:-5] + "/otzyvy.html"
                print("comments_url: ", comments_url)
                comments = get_comments(comments_url)

                print(f"product_name+{k}: ", product_name)

                save_all_comments(path.joinpath(product_name), comments)


if __name__ == "__main__":
    main()






