# -*- coding: utf-8 -*-
import io
from shutil import copyfileobj
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup


headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})

url = "https://www.imdb.com/title/tt0038890/?ref_=ttls_li_tt"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html.parser')
all_div = soup.find_all('div')
classes_div = []
text = ''
for div in all_div:
    class_div = div.get('class')

    if class_div:
        # print(class_div[0])
        if class_div[0] == 'title_wrapper':
            classes_div.append(class_div[0])
            h1 = div.find_all('h1')
            print(h1[0])
            text = h1[0].get_text()
with open('test_file.txt', 'w', encoding='utf-8', newline='') as f:
    f.write(text)


# with urlopen(url) as r, \
#      io.TextIOWrapper(r, encoding=r.headers.get_content_charset('unknown'),
#                       newline='') as input_file, \
#      open('test_file.txt', 'w', encoding='utf-8', newline='') as output_file:
#     copyfileobj(input_file, output_file)
