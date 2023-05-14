class Item:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"THIS IS A STRING: {self.price} {self.thc_percentage} {self.weight}"

    def __repr__(self):
        return f"THIS IS A REPR: {self.price} {self.thc_percentage} {self.weight}"

    @property
    def name(self):
        return self.data["Name"]

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
    
    @property
    def category(self):
        #TODO Sometimes comes back as 'None', how to handle?
        return self.data['subcategory']
    
    @property
    def strain(self):
        return self.data['strainType']