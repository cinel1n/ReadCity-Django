from bs4 import BeautifulSoup
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Категории книг
urls_catalog = [
    'https://www.chitai-gorod.ru/catalog/books/iskusstvo-110338',
    'https://www.chitai-gorod.ru/catalog/books/komiksy-110063',
    'https://www.chitai-gorod.ru/catalog/books/manga-110064',
    "https://www.chitai-gorod.ru/catalog/books/filologiya-110081",
    'https://www.chitai-gorod.ru/catalog/books/medicina-i-zdorove-110207',
    'https://www.chitai-gorod.ru/catalog/books/nauka-tekhnika-it-110282',
    'https://www.chitai-gorod.ru/catalog/books/filosofiya-110316',
    'https://www.chitai-gorod.ru/catalog/books/psihologiya-110321',
    'https://www.chitai-gorod.ru/catalog/books/ehkonomika-menedzhment-marketing-110356',
    'https://www.chitai-gorod.ru/catalog/books/istoriya-obshchestvo-110388',
]

book_url = []       # Тут хранятся все ссылки


# Собирает ссылки книг на одной странице
def SearchUrlBooks(url):
    urls_books = []
    response_base = requests.get(url)
    soup_base = BeautifulSoup(response_base.text, 'lxml')

    soup = soup_base.find('section')
    books = soup.find('div', class_="products-list").find_all('article')
    for book in books:
        urls_books.append(book.find('a').get('href'))

    return urls_books


# Собирет все ссылки книг в переменную book_url
def CollectsLinks():
    for url in urls_catalog:
        for num_page in range(1, 5):
            books = SearchUrlBooks(url + f'?page={num_page}')
            for i in books:
                book_url.append(i)


# Сохранение ссылок в txt файл
def SavesLinks():
    file = open('url book.txt', 'w')
    for i in book_url:
        file.write(f'{i}\n')


def SearchInfo():
    # сюда будут заноситься данные книг
    file = open('book_json.jsonlines', 'a', encoding='utf-8')

    count = 0
    url_books = []
    # Для удобства. добавление в список ссылок из txt файла
    for book_link in open('url book.txt', 'r').readlines():
        if len(book_link.split()) != 0:
            url_books.append(book_link)


    for book_link in url_books:
        data = {}
        print('https://www.chitai-gorod.ru' + book_link.split()[0])
        try:

            response = requests.get('https://www.chitai-gorod.ru' + book_link.split()[0], verify=False)

            soup = BeautifulSoup(response.text, 'lxml')

            title = soup.find('h1', class_="detail-product__header-title", itemprop="name").text
            img = soup.find('img', class_="product-info-gallery__poster").get('src')
            author = soup.find('a', class_="product-info-authors__author").text
            price = soup.find('span', class_="product-offer-price__current product-offer-price__current--discount",
                              itemprop="price").text
            description = soup.find('article', class_="detail-description__text").text

            chars = {}
            characteristics = soup.find('section',
                                        class_="product-detail-features product-detail-features--full detail-product__features info-anchor").find_all(
                class_="product-detail-features__item")
            for char in characteristics:
                left_char = char.find(class_="product-detail-features__item-title").text.strip()
                right_char = char.find(class_="product-detail-features__item-value").text.strip()
                chars[left_char] = right_char

            id = chars['ID товара']

            category_ = soup.find(class_="product-breadcrumbs detail-product__breadcrumbs").find_all('li')
            l = []
            for cat in category_:
                l.append(cat.find(class_="product-breadcrumbs__link").text)

            category = l[0]
            if len(l) >= 2:
                subcategory1 = l[1]
            else:
                subcategory1 = ''
            if len(l) >= 3:
                subcategory2 = l[2]
            else:
                subcategory2 = ''

            data[id] = {
                'title': title.strip(),
                'img': img,
                'author': author.strip(),
                'price': price.strip(),
                'description': description.strip(),
                'chars': chars,
                'category': category.strip(),
                'subcategory1': subcategory1.strip(),
                'subcategory2': subcategory2.strip(),
            }

            json.dump(data, file, ensure_ascii=False)
            file.write('\n')
            count += 1
            url_books.remove(book_link)
            print(count)

        except Exception as e:
            print(e)
            # когда прерву сбор данных
            url_book_text = open('url book.txt', 'w')
            # Перезапись txt файла с сылками для того, чтобы избавится от лишних ссылок
            for i in url_books:
                url_book_text.write(f'{i}\n')

    # когда закончится сбор данных
    url_book_text = open('url book.txt', 'w')
    # Перезапись txt файла с ссылками для того, чтобы избавится от лишних ссылок
    for i in url_books:
        url_book_text.write(f'{i}\n')


# SearchInfo()



