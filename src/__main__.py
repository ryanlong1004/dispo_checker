"""Main point of execution"""
import json
import logging

import click
import requests

# from src.notifier_text import send_email
from src.dbb import create_table, find_best_available, get_db_connection, insert_item
from src.item import Item

headers = {
    "content-type": "application/ld+json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
}

logging.basicConfig(
    filename="./dispo_checker.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

# pylint: disable=line-too-long
URL = "https://dutchie.com/graphql?operationName=FilteredProducts&variables=%7B%22includeEnterpriseSpecials%22%3Afalse%2C%22includeCannabinoids%22%3Atrue%2C%22productsFilter%22%3A%7B%22dispensaryId%22%3A%225f07ab86d0b0134ca75fa12b%22%2C%22option%22%3A%221g%22%2C%22pricingType%22%3A%22rec%22%2C%22strainTypes%22%3A%5B%5D%2C%22subcategories%22%3A%5B%5D%2C%22Status%22%3A%22Active%22%2C%22types%22%3A%5B%22Concentrate%22%5D%2C%22useCache%22%3Afalse%2C%22sortDirection%22%3A1%2C%22sortBy%22%3A%22price%22%2C%22isDefaultSort%22%3Afalse%2C%22bypassOnlineThresholds%22%3Afalse%2C%22isKioskMenu%22%3Afalse%2C%22removeProductsBelowOptionThresholds%22%3Atrue%7D%2C%22page%22%3A0%2C%22perPage%22%3A50%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%220e884328c01ef8ed540d4bbd27101ee58fedaf5cddda6c499169209b53fdf574%22%7D%7D"


def load_items(data):
    """instantiates data individually into item instances"""
    logging.info("loading items")
    return [Item(item_data) for item_data in data]


def fetch_data():
    """fetch live data from url"""
    logging.info("fetching data")
    return requests.get(URL, headers=headers, timeout=60).text


def fetch_items():
    """fetch current data and instantiate item list"""
    logging.info("loading items")
    return [
        Item(item_data)
        for item_data in json.loads(fetch_data())["data"]["filteredProducts"][
            "products"
        ]
    ]


@click.command()
@click.option("-b", "--best-price", default=None, show_default=True, type=float)
def main(best_price):
    """Collects information from a Dutchie dispensary"""
    connection = get_db_connection("./dispo_checker.db")
    cursor = connection.cursor()
    create_table(cursor)

    for _item in fetch_items():
        insert_item(cursor, _item)
    connection.commit()

    logging.info("finding best available")
    ignored_categories = [
        "hash",
        "sugar",
        "rso",
        "diamonds",
        "applicators",
        "infused-flower",
    ]
    best = find_best_available(cursor, ignored_categories)

    if best_price:
        if best["price"] < best_price:
            print(best)
