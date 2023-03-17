from extract_book_infos import Extract_book_infos

# Instanciation de l'objet infos en lui passant l'url de la page d'un livre à scraper.
infos = Extract_book_infos("https://books.toscrape.com/catalogue/soumission_998/index.html")

#Appel de la méthode to_csv utilisant la bibliothèque Pandas pour créer le fichier.csv formaté et contenant les informations comme demandé.
infos.to_csv('./csv/book_info.csv')


"""print(infos.url)
print("Description :", infos.product_description)
print("Titre :", infos.title)
print("UPC :", infos.universal_product_code_upc)
print("Available :", infos.number_available)
print("price excluding tax :", infos.price_excluding_tax)
print("price including tax :", infos.price_including_tax)
print("Review(s) :", infos.review_rating)
print("Category :", infos.category)
print("image URL :", infos.image_url)"""