import os
from bs4 import BeautifulSoup
from bs4.element import Tag
import uuid
import json
import re
from slugify import slugify

SOURCE_RAW_MERCADO = './data/raw/mercado/details/'

def parse_boat(boat_html: Tag):
    price = fetch_html_selector(boat_html, '#price > div > div > div > span > span.andes-money-amount__fraction')
    title = fetch_html_selector(boat_html, '#header > div > div.ui-pdp-header__title-container > h1')
    seller = fetch_html_selector(boat_html, '#seller_profile > div > div > a > h3')
    address = fetch_html_selector(boat_html, '#seller_profile > ul div > p')
    url = boat_html.find('meta', property="og:url")
    page_url = url['content'] if url else None
    
    characteristics_data = {}
    characteristics_html = boat_html.select_one('#technical_specifications > div > div.ui-pdp-specs__table > table > tbody')
    if characteristics_html:
        rows = characteristics_html.find_all('tr')
        for row in rows:
            label = row.find('th').get_text(strip=True)
            if label:
                value = row.find('td').get_text(strip=True)
                characteristics_data[slugify(label, separator="_")] = value if value else None
    extra_info = {}
    extra_info_html = boat_html.select_one('#tab-content-id-informações-gerais')
    if extra_info_html:
        rows = extra_info_html.find_all('p')
        for row in rows:
            label = row.find('span').get_text(strip=True)
            if label:
                value = row.get_text(strip=True).split(':')[1].strip()
                extra_info[slugify(label, separator="_")] = value if value else None
    description = fetch_html_selector(boat_html, '#description > div > p')
    details_dict = {
        'title': title,
        'price': price,
        'seller': seller,
        'address': address,
        'page_url': page_url,
        'description': description,
        **characteristics_data,
        **extra_info
    }
    return details_dict

def fetch_html_selector(boat_html: Tag, selector: str):
    value = boat_html.select_one(selector)
    if value:
        return value.get_text(strip=True)
    return None

def persist(boats_dicts: list[dict]):
    with open(f'./data/parsed/details/{uuid.uuid1()}.json', 'w', encoding='utf8') as file_json:
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

boats_dicts = []
for html_content in html_pages: 
    soup = BeautifulSoup(html_content, features='html.parser')
    boats_dicts.append(parse_boat(soup))
    #os.remove(file_page_full_path)

persist(boats_dicts)


    