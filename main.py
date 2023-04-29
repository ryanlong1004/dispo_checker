import json


class Item:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"THIS IS A STRING: {self.price} {self.thc_percentage} {self.weight}"

    def __repr__(self):
        return f"THIS IS A REPR: {self.price} {self.thc_percentage} {self.weight}"

    @property
    def price(self):
        return self.data["medicalPrices"][0]

    @property
    def thc_percentage(self):
        return self.data["THCContent"]["range"][0]

    @property
    def weight(self):
        return self.data["weight"]

    @property
    def brandname(self):
        return self.data["brandName"]

    @property
    def quantity_available(self):
        return self.data["POSMetaData"]["children"][0]["quantityAvailable"]


def main():
    with open("./response.json", "r") as _file:
        result = json.load(_file)["data"]["filteredProducts"]["products"]

        # Cool kids way
        items = [Item(item_data) for item_data in result]
        print(len(items))


if __name__ == "__main__":
    main()
