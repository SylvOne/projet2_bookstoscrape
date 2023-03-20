import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


class ExtractBookInfos:
    def __init__(self, urls ):
        self.urls = urls
        self.universal_product_code_upc = []
        self.title = []
        self.price_including_tax = []
        self.price_excluding_tax = []
        self.number_available = []
        self.product_description = []
        self.category = []
        self.review_rating = []
        self.image_url = []

        for one_url in self.urls:
            self.response = requests.get(one_url, headers=HEADERS)
            self.html_parse = self.parse_html_page()

            # J'appelle toutes les méthodes directement dans le constructeur de classe afin de récupérer d'emblée les informations des livres
            self.info_title()
            self.info_description()
            self.info_code_upc_price_tax_available_review()
            self.info_category()
            self.info_img_url()

    # Cette methode stocke un dictionnaire dans la variable self.html_parse du type {"error":Boolean, "soup":Resultat_de_beautifulsoup},
    # cela me permettra pour chaque méthode de verifier rapidement si la requete à aboutie ou non, avant d'aller plus loin dans l'implémentation.
    def parse_html_page(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, "html.parser")
            return {"error" : False, "soup" :soup}
        else:
            return {"error" : True, "soup" : self.response.status_code}

    # Methode qui recupere le titre
    def info_title(self):
        if self.html_parse["error"]:
            self.title.append("RAS:"+ str(self.html_parse["soup"]))
        else:
            self.title.append(self.html_parse["soup"].find("h1").text)

    # Methode qui recupere la description
    def info_description(self):
        if self.html_parse["error"]:
            self.product_description.append("RAS:"+ str(self.html_parse["soup"]))
        else:
            article = self.html_parse["soup"].find("article", class_="product_page")
            product_infos = article.find_all("p")
            if product_infos and len(product_infos) > 3:
                self.product_description.append(product_infos[3].text)
            else:
                self.product_description.append("RAS:0")

    # Methode qui recupere le code UPC, les prix avec et sans taxe, le nbr de produits en stock, et le Review rating
    def info_code_upc_price_tax_available_review(self):
        if self.html_parse["error"]:
            self.universal_product_code_upc.append("RAS:"+ str(self.html_parse["soup"]))
        else:
            table_product = self.html_parse["soup"].find("table", class_="table table-striped")
            tr_product = table_product.find_all("tr")
            if tr_product and len(tr_product) > 6:
                self.universal_product_code_upc.append(tr_product[0].find("td").text)
                self.number_available.append(tr_product[5].find("td").text)
                self.price_excluding_tax.append(tr_product[2].find("td").text)
                self.price_including_tax.append(tr_product[3].find("td").text)
                self.review_rating.append(tr_product[6].find("td").text)
            else:
                self.product_description.append("RAS:0")
                self.universal_product_code_upc.append("RAS:0")
                self.number_available.append("RAS:0")
                self.price_excluding_tax.append("RAS:0")
                self.price_including_tax.append("RAS:0")
                self.review_rating.append("RAS:0")

    # Methode qui recupere la catégorie du produit
    def info_category(self):
        if self.html_parse["error"]:
            self.category.append("RAS:" + str(self.html_parse["soup"]))
        else:
            ul_product = self.html_parse["soup"].find("ul", class_="breadcrumb")
            li_product = ul_product.find_all("li")
            if li_product and len(li_product) > 3:
                self.category.append(li_product[2].find("a").text)
            else:
                self.category.append("RAS:0")

    # Methode qui récupère l'url de l'image
    def info_img_url(self):
        if self.html_parse["error"]:
            self.image_url.append("RAS:" + str(self.html_parse["soup"]))
        else:
            div_product = self.html_parse["soup"].find("div", class_="item active")
            img_product = div_product.find("img")
            if img_product:
                self.image_url.append(img_product["src"])
            else:
                self.image_url.append("RAS:0")

    def download_image(self, urls_images):
        for url_image in urls_images:
            response = requests.get(url_image)
            filename = url_image.split("/")[-1]
            if response.status_code == 200:
                with open("./images/"+filename, 'wb') as f:
                    f.write(response.content)