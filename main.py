from extract_book_infos import Extract_book_infos
from extract_books_urls_category import Extract_books_urls_category


##----RECUPERATION DES URLS PRODUITS D UNE CATEGORIE----
# Instanciation de l'objet Extract_books_urls_category en lui passant en paramètre l'url d'une page catégorie.
infos_categorie = Extract_books_urls_category("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")

# J'appelle la méthode permettant de récupérer tous les urls produits de la catégorie
infos_categorie.find_urls_products_in_all_pages()

##----RECUPERATION DES INFOS PRODUITS----
# Instanciation de l'objet Extract_book_infos en lui passant la liste d'urls produits à scraper.
infos_produits = Extract_book_infos(infos_categorie.urls_products)

#Appel de la méthode to_csv utilisant la bibliothèque Pandas pour créer le fichier.csv formaté et contenant les informations de tous les livres d'une catégorie donnée.
infos_produits.to_csv('./csv/book_info.csv')
