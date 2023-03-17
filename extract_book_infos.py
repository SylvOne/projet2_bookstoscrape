import requests
from bs4 import BeautifulSoup
import pandas as pd


HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


class Extract_book_infos :
    def __init__(self, url ):
        self.url = url
        self.product_page_url = ""
        self.universal_product_code_upc = ""
        self.title = ""
        self.price_including_tax = ""
        self.price_excluding_tax = ""
        self.number_available = ""
        self.product_description = ""
        self.category = ""
        self.review_rating = ""
        self.image_url = ""
        self.response = requests.get(self.url, headers=HEADERS)
        self.html_parse = self.parse_html_page()

        # J'appelle toutes les méthodes dans le constructeur de classe afin d'initialiser automatiquement les variables ci-dessus
        self.info_title()
        self.info_description()
        self.info_code_upc_price_tax_available_review()
        self.info_category()
        self.info_img_url()

    #Cette methode stocke un dictionnaire dans la variable self.html_parse du type {"error":Boolean, "soup":Resultat_de_beautifulsoup} cela me permettra pour chaque méthode de verifier rapidement si la requete à aboutie ou non.
    def parse_html_page(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, "html.parser")
            return {"error" : False, "soup" :soup}
        else:
            return {"error" : True, "soup" : self.response.status_code}

    # Methode qui recupere le titre
    def info_title(self):
        if self.html_parse["error"]:
            self.title = "RAS:"+ str(self.html_parse["soup"])
        else:
            self.title = self.html_parse["soup"].find("h1").text

    # Methode qui recupere la description
    def info_description(self):
        if self.html_parse["error"]:
            self.product_description = "RAS:"+ str(self.html_parse["soup"])
        else:
            article = self.html_parse["soup"].find("article", class_="product_page")
            product_infos = article.find_all("p")
            if product_infos and len(product_infos) > 3:
                self.product_description = product_infos[3].text.encode('latin1').decode('utf8')
            else:
                self.product_description = "RAS:0"

    # Methode qui recupere le code UPC, les prix avec et sans taxe, le nbr de produits en stock, et le Review rating
    def info_code_upc_price_tax_available_review(self):
        if self.html_parse["error"]:
            self.universal_product_code_upc = "RAS:"+ str(self.html_parse["soup"])
        else:
            table_product = self.html_parse["soup"].find("table", class_="table table-striped")
            tr_product = table_product.find_all("tr")
            if tr_product and len(tr_product) > 6:
                self.universal_product_code_upc = tr_product[0].find("td").text
                self.number_available = str(int(''.join(filter(str.isdigit, tr_product[5].find("td").text))))
                self.price_excluding_tax = tr_product[2].find("td").text.split("£")[1]
                self.price_including_tax = tr_product[3].find("td").text.split("£")[1]
                self.review_rating = tr_product[6].find("td").text
            else:
                self.product_description = "RAS:0"
                self.universal_product_code_upc = "RAS:0"
                self.number_available = "RAS:0"
                self.price_excluding_tax = "RAS:0"
                self.price_including_tax = "RAS:0"
                self.review_rating = "RAS:0"

    # Methode qui recupere la catégorie du produit
    def info_category(self):
        if self.html_parse["error"]:
            self.category = "RAS:" + str(self.html_parse["soup"])
        else:
            ul_product = self.html_parse["soup"].find("ul", class_="breadcrumb")
            li_product = ul_product.find_all("li")
            if li_product and len(li_product) > 3:
                self.category = li_product[2].find("a").text
            else:
                self.category = "RAS:0"

    # Methode qui récupère l'url de l'image
    def info_img_url(self):
        if self.html_parse["error"]:
            self.image_url = "RAS:" + str(self.html_parse["soup"])
        else:
            div_product = self.html_parse["soup"].find("div", class_="item active")
            img_product = div_product.find("img")
            if img_product:
                self.image_url = "https://books.toscrape.com/media" + img_product["src"].split("/media")[1]
            else:
                self.image_url = "RAS:0"

    # Méthode qui va enregistrer les données récupérées dans un fichier CSV.
    def to_csv(self, filepath):
        book = {
            'product_page_url': [self.url],
            'universal_product_code_upc': [self.universal_product_code_upc],
            'title': [self.title],
            'price_including_tax': [self.price_including_tax],
            'price_excluding_tax': [self.price_excluding_tax],
            'number_available': [self.number_available],
            'product_description': [self.product_description],
            'category': [self.category],
            'review_rating': [self.review_rating],
            'image_url': [self.image_url]
        }


        df = pd.DataFrame(book)
        df.to_csv(filepath, index=False)