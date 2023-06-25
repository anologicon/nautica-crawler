from requests import get
import os
import json
from time import sleep
from random import randint
from selenium import webdriver
from tqdm import tqdm

PAGE_LIST_JSON_PATH = './data/parsed/list'
driver = webdriver.Chrome()

page_list_files = os.listdir(PAGE_LIST_JSON_PATH)

def fetch_http_sys_path_files() -> list[dict]:
    page_address_list_not_processed = []
    for page_file in page_list_files:
        file_full_path = PAGE_LIST_JSON_PATH+'/'+page_file
        with open(file_full_path, 'r') as fp:
            json_loaded = json.load(fp)
            for json_data in json_loaded[:1]:
                page_address_list_not_processed.append({
                    'page_full_path': file_full_path,
                    'mercado_id': json_data['mercado_id'],
                    'http_url': json_data['page_address']
                })
            fp.close()
    return page_address_list_not_processed

for page_sys_http in tqdm(fetch_http_sys_path_files()):
    driver.get(page_sys_http['http_url'])
    sleep(randint(5, 60))
    content = driver.page_source
    with open('./data/raw/mercado/details/'+page_sys_http['mercado_id']+'.html', 'w') as fp:
        fp.write(content)
        fp.close()
    #os.remove(page_sys_http['page_full_path'])