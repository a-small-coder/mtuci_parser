# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})

url = "https://mtuci.ru/time-table/"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
all_links = soup.find_all('a')
excel_links = []
for link in all_links:
    href = link.get('href')
    # print(href[-1:-5:-1])
    if href[-4:-1] == 'xls':
        excel_links.append(href)
        with open(r'' + href, "wb") as f:  # открываем файл для записи, в режиме wb
            print(href)
            ufr = requests.get(url+href)  # делаем запрос
            f.write(ufr.content)  # записываем содержимое в файл; как видите - content запроса
            f.close()
print(excel_links)

