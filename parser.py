import argparse
from pathlib import Path
from typing import List, Dict
import json

import requests

from helpers.base_url import BASE_URL
from helpers.categories import get_categories
from helpers.products import get_products, get_product_name, get_comments
from helpers.subcategories import subcategory


parser = argparse.ArgumentParser(
                    prog='Parse foxtrot',
                    description='Parse comments on site foxtrot'
)
parser.add_argument('-cc', '--count_categories', type=int, default=1, help="How many categories parse. Default 1")
parser.add_argument('-cs', '--count_subcategories', type=int, default=1, help="How many subcategories parse. Default 1")
parser.add_argument('-cp', '--count_products', type=int, default=1, help="How many products parse. Default 1")
args = parser.parse_args()


def save_all_comments(path: Path, comments: List[Dict]) -> None:
    with open(f"{path}.json", mode="w", encoding="utf-8") as fd:
        json.dump(comments, fd, ensure_ascii=False, indent=2)


def main():

    categories = get_categories(BASE_URL)

    for category in categories[:args.count_categories]:
        category_url = category.a["href"]
        print("category: ", category.a.text)

        try:
            subcategories = subcategory(BASE_URL+category_url, args.count_categories)
        except requests.exceptions.InvalidURL:
            continue

        for subcategory_ in subcategories[:args.count_subcategories]:
            subcategory_url = subcategory_.a["href"]
            subcategory_name = subcategory_.a.text
            path = Path("reviews").joinpath(subcategory_name)
            path.mkdir(exist_ok=True)
            products = get_products(BASE_URL+subcategory_url)

            for k, product in enumerate(products[:args.count_products]):
                product_url = product.a["href"]
                product_name = get_product_name(BASE_URL+product_url)
                comments = get_comments(BASE_URL + product_url)

                print(f"product_name+{k}: ", product_name)

                save_all_comments(path.joinpath(product_name), comments)


if __name__ == "__main__":
    main()
