import requests
from bs4 import BeautifulSoup


HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}


class ExtractBooksCategories:

    def __init__(self, url):
        self.url = url
        self.categories = []

        self.response = requests.get(self.url, headers=HEADERS)
        self.html_parse = self.parse_html_page()


    def parse_html_page(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, "html.parser")
            return {"error" : False, "soup" :soup}
        else:
            return {"error" : True, "soup" : self.response.status_code}

    def retrieve_all_categories(self):
        if self.html_parse["error"]:
            self.categories.append("RAS:" + str(self.html_parse["soup"]))
        else:
            ul_categories = self.html_parse["soup"].find("ul", class_="nav nav-list")
            li_categories = ul_categories.find_all("li")
            if li_categories:
                li_categories.pop(0)
                for cat in li_categories:
                    self.categories.append("http://books.toscrape.com/"+cat.find("a")["href"])
            else:
                self.categories.append("RAS:0")