class TransformBookInfos:

    def __init__(self, books_to_transform):
        self.books_to_transform = books_to_transform
        self.books_transformed = None

        self.title = []
        self.price_including_tax = []
        self.price_excluding_tax = []
        self.number_available = []
        self.product_description = []
        self.image_url = []

        # Pas de transformation nécessaire pour :
        # les urls, les ratings, les category, les code UPC car ils sont déjà très bien comme tel.
        # (Si nécessaire il sera bien sûr possible de rajouter un traitement via l'implémention de méthodes)
        self.category = books_to_transform["category"]
        self.review_rating = books_to_transform["review_rating"]
        self.product_page_url = books_to_transform["product_page_url"]
        self.universal_product_code_upc = books_to_transform["universal_product_code_upc"]
        self.title = books_to_transform["title"]

    def transform_info_description(self):
        for description_to_transform in self.books_to_transform["product_description"]:
            if "RAS" in description_to_transform:
                self.product_description.append(description_to_transform)
            else:
                self.product_description.append(description_to_transform.encode('latin1').decode('utf8'))

    def transform_number_available(self):
        for number_available in self.books_to_transform["number_available"]:
            if "RAS" in number_available:
                self.number_available.append(number_available)
            else:
                self.number_available.append(str(int(''.join(filter(str.isdigit, number_available)))))

    def transform_exclude_tax(self):
        for exclude_tax in self.books_to_transform["price_excluding_tax"]:
            if "RAS" in exclude_tax:
                self.price_excluding_tax.append(exclude_tax)
            else:
                self.price_excluding_tax.append(exclude_tax.split("£")[1])

    def transform_include_tax(self):
        for include_tax in self.books_to_transform["price_including_tax"]:
            if "RAS" in include_tax:
                self.price_including_tax.append(include_tax)
            else:
                self.price_including_tax.append(include_tax.split("£")[1])

    def transform_url_image(self):
        for url_image in self.books_to_transform["image_url"]:
            if "RAS" in url_image:
                self.price_including_tax.append(url_image)
            else:
                self.image_url.append("https://books.toscrape.com/media" + url_image.split("/media")[1])

    def transform_books_for_load(self):
        self.books_transformed = {
            'product_page_url': self.product_page_url,
            'universal_product_code_upc': self.universal_product_code_upc,
            'title': self.title,
            'price_including_tax': self.price_including_tax,
            'price_excluding_tax': self.price_excluding_tax,
            'number_available': self.number_available,
            'product_description': self.product_description,
            'category': self.category,
            'review_rating': self.review_rating,
            'image_url': self.image_url
        }