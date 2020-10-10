import requests
from bs4 import BeautifulSoup as BS

university_translitor_dict = {
    "vavt": "ВАВТ",
    "hse": "ВШЭ",
    "gaugn": "ГАУГН",
    "guu": "ГУУ",
    "mai": "МАИ",
    "mgavm": "МГАВМИБ",
    "mgimo": "МГИМО",
    "mglu": "МГЛУ",
    "mgppu": "МГППУ",
    "mgpu": "МГПУ",
    "stankin": "МГТУ СТАНКИН",
    "bmstu": "МГТУ ИМ. БАУМАНА",
    "msu": "МГУ",
    "miigaik": "МИИГАИК",
    "mirea": "МИРЭА",
    "misis": "МИСИС",
    "mephi": "МИФИ",
    "miet": "МИЭТ",
    "mpgu": "МПГУ",
    "msha": "МСХА",
    "mtuci": "МТУСИ",
    "mipt": "МФТИ",
    "mei": "МЭИ",
    "mospoly": "МОСКОВСКИЙ ПОЛИТЕХ",
    "ranepa": "РАНХИГС",
    "ranepa0": "РАНХИГС - ЭМИТ",
    "rggru": "РГГРУ (МГРИ)",
    "rggu": "РГГУ",
    "rgung": "РГУНГ",
    "rudn": "РУДН",
    "miit": "РУТ (МИИТ)",
    "muctr": "РХТУ",
    "rea": "РЭУ",
    "fu": "ФУ",
    "hse-spb": "ВШЭ-СПБ",
    "itmo": "ИТМО",
    "leti": "ЛЭТИ",
    "ranepa1": "РАНХИГС - СЕВЕРО-ЗАПАДНЫЙ ИНСТИТУТ УПРАВЛЕНИЯ - ФИЛИАЛ",
    "herzenspb": "РГПУ ИМ. ГЕРЦЕНА",
    "spbu": "СПБГУ",
    "spbguap": "СПБГУАП",
    "spbgeu": "СПБГЭУ",
    "spbstu": "СПБПУ",
    "kpfu": "КФУ",
    "hse-nn": "ВШЭ-НН",
    "nnsu": "ННГУ",
    "ranepa2": "РАНХИГС - НИЖЕГОРОДСКИЙ ИНСТИТУТ УПРАВЛЕНИЯ - ФИЛИАЛ",
    "samsu": "САМАРСКИЙ УНИВЕРСИТЕТ",
    "ranepa3": "РАНХИГС - СИБИРСКИЙ ИНСТИТУТ УПРАВЛЕНИЯ",
    "ranepa5": "РАНХИГС - ЮЖНО-РОССИЙСКИЙ ИНСТИТУТ УПРАВЛЕНИЯ - ФИЛИАЛ",
    "ranepa4": "РАНХИГС - УРАЛЬСКИЙ ИНСТИТУТ УПРАВЛЕНИЯ - ФИЛИАЛ",
    "hse-perm": "ВШЭ-ПЕРМЬ",
    "ranepa6": "РАНХИГС - ПЕРМСКИЙ ФИЛИАЛ"
}


class Person:
    universities = []
    profile = ''
    first_name = ''
    surname = ''
    father_name = ''


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def get_person_data():
    person1 = Person()
    SnFnFn = input("введите свое ФИО").split(' ')
    person1.surname, person1.first_name, person1.father_name = SnFnFn[0], SnFnFn[1], SnFnFn[2]
    universities_on_rus = input("введите ваши вузы").split(' ')
    universities_on_eng = []
    for univer in universities_on_rus:
        universities_on_eng.append(get_key(university_translitor_dict, univer))
    person1.universities = universities_on_eng
    return person1


def parser_start_page():
    URL = 'http://admlist.ru/index.html'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    response = requests.get(URL, headers=HEADERS)
    soup = BS(response.content, 'html.parser')
    items = soup.findAll('a')
    universities = []
    for item in items:
        university_href = item.get('href')
        university_href_last_symbol_name = university_href.find('/')
        is_href_to_university = university_href[-10:-1: 1] + university_href[-1]
        if is_href_to_university == 'index.html':  # taking universities name and href
            universities.append({
                'name': university_href[:university_href_last_symbol_name:],
                'rusname': item.get_text(strip=True),
                'href': university_href
            })
    print(universities)

    person1 = get_person_data()
    right_universities_links = []
    for university in person1.universities:
        for point in universities:
            if point['name'] == university:
                right_universities_links.append(point['href'])

    return right_universities_links

def parser_university_page(universities_links_list):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    all_vectors_links = []
    for university_link in universities_links_list:
        URL = 'http://admlist.ru/index.html' + university_link
        response = requests.get(URL, header=HEADERS)
        soup = BS(response, 'html.parser')
        items = soup.findAll('a')
        all_vectors_links.append({
            'university_link': university_link,
            'links': []
        })
        for item in items:
            all_vectors_links['links'].append({
                'name': item.get_text(strip=True),
                'link': item.get('href')
            })
    return all_vectors_links


right_universities_links = parser_start_page()
all_vectors_links = parser_university_page(right_universities_links)
