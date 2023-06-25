import os
from bs4 import BeautifulSoup
from bs4.element import Tag
import uuid
import json
import re

SOURCE_RAW_MERCADO = './data/raw/mercado/'

def parse_boat(boat_html: Tag):
    price = boat_html.find('span', class_='price-tag-text-sr-only').text
    year = boat_html.select_one('.ui-search-item__group--attributes > ul').text
    description = boat_html.select_one('.ui-search-item__group--title.shops__items-group > a > h2').text
    address = boat_html.select_one('.ui-search-item__group--location.shops__items-group > span').text
    page_address = boat_html.select_one('.ui-search-item__group--title.shops__items-group > a').attrs['href']
    mercado_id = re.findall(r'MLB-\d+', page_address)[0]
    return {
        'mercado_id':  mercado_id,
        'price': price,
        'year': year,
        'description': description,
        'address': address,
        'page_address': page_address
    }

def persist(boats_dicts: list[dict]):
    with open(f'./data/parsed/list/{uuid.uuid1()}.json', 'w', encoding='utf8') as file_json:
        json.dump(boats_dicts, file_json, ensure_ascii=False)
        file_json.close()

raw_files_path = os.listdir(SOURCE_RAW_MERCADO)
file_page_full_paths = []

for file_page in raw_files_path:
    file_page_full_paths.append(SOURCE_RAW_MERCADO+file_page)

html_pages = []
for file_page_full in file_page_full_paths:
    with open(file_page_full, 'r') as file_boat_raw:
        html_pages.append(file_boat_raw.read())
        file_boat_raw.close()

for html_content in html_pages: 
    soup = BeautifulSoup(html_content, features='html.parser')
    boats = soup.find_all('li', class_='ui-search-layout__item')
    boats_dicts = []
    for boat in boats:
        boats_dicts.append(parse_boat(boat))
    persist(boats_dicts)
    os.remove(file_page_full_path)


    