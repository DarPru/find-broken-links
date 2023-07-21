import requests
from bs4 import BeautifulSoup

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

report = open('log.txt', 'w')

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

with open('links.txt', 'r', encoding='utf-8') as file:
    links = [f.strip('\n') for f in file]
    counter = 1
    for link in links:
        no_errors = True
        r = session.get(link)
        soup = BeautifulSoup(r.text, 'lxml')
        images = soup.findAll('img')
        for image in images:
            image_link = image.get('src')
            try:
                if session.get(image_link, allow_redirects=False).status_code != 200:
                    no_errors = False
                    print(f'{link}: ошибка {requests.get(image_link)} у изображения {image_link}', file=report)
            except Exception as ex:
                print(f'Изображение {image_link} в файле {link}: Ошибка [{str(ex).upper()}]')
        if no_errors:
            print(f'{link}: ошибок не найдено', file=report)
        print(f'Обработано {counter} из {len(links)}')
        counter += 1