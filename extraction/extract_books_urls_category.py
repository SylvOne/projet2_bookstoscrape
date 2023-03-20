import requests
from bs4 import BeautifulSoup
import math

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


class ExtractBooksUrlsCategory:
    def __init__(self, url):
        self.url_category = url
        self.html_parse = None

        self.urls_products = []
        self.nbr_pages = ""
        self.nbr_products_total = ""
        self.nbr_products_in_page = ""

        self.parse_html_page()

    # Methode qui permet de charger la page web contenant les produits d'une catégorie
    def parse_html_page(self):
        if requests.get(self.url_category, headers=HEADERS).status_code == 200:
            soup = BeautifulSoup(requests.get(self.url_category, headers=HEADERS).text, "html.parser")
            self.html_parse = {"error": False, "soup": soup}
        else:
            self.html_parse = {"error": True, "soup": requests.get(self.url_category, headers=HEADERS).status_code}

    # Cette methode permet d'initialiser les variables nbr_products_in_page, nbr_products_total et nbr_pages, elle sera appelée dans la méthode find_urls_products_in_all_pages()
    def nbr_product_in_page_and_in_category_and_nbr_pages(self):
        if self.html_parse["error"]:
            self.nbr_products_total = "RAS:" + str(self.html_parse["soup"])
            self.nbr_products_in_page = "RAS:" + str(self.html_parse["soup"])
            self.nbr_pages = "RAS:" + str(self.html_parse["soup"])
        else:
            products_infos_pages = self.html_parse["soup"].find("form", class_="form-horizontal")
            strong_list = products_infos_pages.find_all("strong")
            # Si il y a plusieurs pages alors on enregistre le nbr_products_total et nbr_products_in_page
            if strong_list and len(strong_list) > 2:
                self.nbr_products_total = strong_list[0].text
                self.nbr_products_in_page = strong_list[2].text
                self.nbr_pages = str(math.ceil(int(strong_list[0].text) / 20))
            # Si il n'y a qu'une seule page produit alors forcément nbr_products_total et nbr_products_in_page seront identiques
            elif strong_list and len(strong_list) == 1:
                self.nbr_products_total = strong_list[0].text
                self.nbr_products_in_page = strong_list[0].text
                self.nbr_pages = "1"
            else:
                self.nbr_products_total = "RAS:0"
                self.nbr_products_in_page = "RAS:0"
                self.nbr_pages = "RAS:0"

    # Cette méthode permet de recuperer toutes les URLs des produits, présentes sur une page donnée
    def find_urls_in_one_page_product(self):
        if self.html_parse["error"]:
            self.urls_products.append("RAS:" + str(self.html_parse["soup"]))
        else:
            products_infos_pages = self.html_parse["soup"].find_all("div", class_="image_container")

            if products_infos_pages:
                for product in products_infos_pages:
                    url_of_product = product.find("a")["href"].split("/")[-2] + "/" + \
                                     product.find("a")["href"].split("/")[-1]
                    self.urls_products.append("https://books.toscrape.com/catalogue/" + url_of_product)
            else:
                self.urls_products.append("RAS:0")

    # Cette methode vient executer la méthode self.nbr_product_in_page_and_in_category_and_nbr_pages(),
    # puis en fonctions du nombres de page présent dans une catégorie, elle appel autant de fois qu'il faut,
    # la méthode find_urls_in_one_page_product ( en changeant l'url de self.url_category ) afin de récupérer tous les produits présents sur chaque page.
    def find_urls_products_in_all_pages(self):
        # j'initialise dans un premiers les variable self.nbr_products_total self.nbr_products_in_page et self.nbr_pages
        # en executant la méthode self.nbr_product_in_page_and_in_category_and_nbr_pages()
        self.nbr_product_in_page_and_in_category_and_nbr_pages()

        # si il n'y a qu'une seule page alors on execute une fois la méthonde self.find_urls_in_one_page_product()
        if self.nbr_pages == 1:
            self.find_urls_in_one_page_product()

        # sinon si il y a plusieurs pages alors on execute une 1ere fois self.find_urls_in_one_page_product()
        # en réinitialisant l'url de la catégorie
        else:
            self.find_urls_in_one_page_product()

            for index_page in range(int(self.nbr_pages) - 1):

                if index_page == 0 and "index.html" in self.url_category:
                    index_page_suivante = index_page + 2
                    self.url_category = self.url_category.replace("index.html",
                                                                  "page-" + str(index_page_suivante) + ".html")
                    self.parse_html_page()
                    self.find_urls_in_one_page_product()

                else:
                    index_page_suivante = index_page + 2
                    self.url_category = self.url_category.replace("page-" + str(index_page + 1) + ".html",
                                                                  "page-" + str(index_page_suivante) + ".html")
                    self.parse_html_page()
                    self.find_urls_in_one_page_product()
