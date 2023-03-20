from extraction.extract_book_infos import ExtractBookInfos
from extraction.extract_books_urls_category import ExtractBooksUrlsCategory
from extraction.extract_books_categories import ExtractBooksCategories
from transformation.transform_book_infos import TransformBookInfos
from load.load_datas import LoadDatas

# #########################################################################################
#----RECUPERATION DE TOUTES LES CATEGORIES PRESENTES SUR LE SITE http://books.toscrape.com/
# #########################################################################################
categories = ExtractBooksCategories("http://books.toscrape.com/")
categories.retrieve_all_categories()

# ----RECUPERATION DE TOUS LES URLS PRODUITS DE TOUTES LES CATEGORIES,
# AINSI QUE TOUTES LES DATAS DE TOUS LES PRODUITS SELON LA METHODE E.T.L.
for i in range(len(categories.categories)):
    # Instanciation de l'objet ExtractBooksUrlsCategory en lui passant en paramètre l'url d'une page catégorie.
    infos_categorie = ExtractBooksUrlsCategory(categories.categories[i])

    # J'appelle la méthode permettant de récupérer tous les urls produits de la catégorie
    infos_categorie.find_urls_products_in_all_pages()

    # #############################
    # DEMARRAGE DU PROCESSUS E.T.L.
    # #############################

    # ----EXTRACTION DES DATAS PRODUITS----
    # Instanciation de l'objet ExtractBookInfos et extractions des datas produits, en lui donnant en paramètre une liste d'urls produits à scraper.
    extraction_infos_produits = ExtractBookInfos(infos_categorie.urls_products)
    books = {
        'product_page_url': extraction_infos_produits.urls,
        'universal_product_code_upc': extraction_infos_produits.universal_product_code_upc,
        'title': extraction_infos_produits.title,
        'price_including_tax': extraction_infos_produits.price_including_tax,
        'price_excluding_tax': extraction_infos_produits.price_excluding_tax,
        'number_available': extraction_infos_produits.number_available,
        'product_description': extraction_infos_produits.product_description,
        'category': extraction_infos_produits.category,
        'review_rating': extraction_infos_produits.review_rating,
        'image_url': extraction_infos_produits.image_url
    }

    # ----TRANSFORMATION DES DATAS PRODUITS (en appelant les différentes méthode de l'objet TransformBookInfos) ----
    transformation_infos_produits = TransformBookInfos(books)

    transformation_infos_produits.transform_info_description()
    transformation_infos_produits.transform_number_available()
    transformation_infos_produits.transform_exclude_tax()
    transformation_infos_produits.transform_include_tax()
    transformation_infos_produits.transform_url_image()
    transformation_infos_produits.transform_books_for_load()
    datas_to_load = transformation_infos_produits.books_transformed

    # ---- CHARGEMENT DES DATAS VERS DES FICHIERS CSV. ----
    chargement_des_donnees = LoadDatas(datas_to_load)
    chargement_des_donnees.to_csv()