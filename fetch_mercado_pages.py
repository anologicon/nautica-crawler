import requests
from selenium import webdriver
import uuid
from time import sleep
from selenium.webdriver.common.by import By
from random import randint

htmls = []

driver = webdriver.Chrome()
driver.get('https://lista.mercadolivre.com.br/veiculos/nautica/')
sleep(5)

pagination_max_text = driver.find_element(By.CLASS_NAME, 'andes-pagination__page-count').text
pagination_max_int = int(''.join(filter(str.isdigit, pagination_max_text)))

cookie_button = driver.find_element(By.CSS_SELECTOR, 'button.cookie-consent-banner-opt-out__action.cookie-consent-banner-opt-out__action--primary')
cookie_button.click()

for page_number in range(1, pagination_max_int):
    sleep(randint(5, 15))
    htmls.append({'page': page_number, 'content': driver.page_source})
    next_page = driver \
        .find_element(By.CSS_SELECTOR, '.andes-pagination__button--next.shops__pagination-button > a').get_attribute("href")
    driver.get(next_page)
    
for html in htmls:
    with open(f"./data/raw/mercado/page_{html['page']}.html", 'w') as f:
        f.write(html['content'])
        f.close()
        