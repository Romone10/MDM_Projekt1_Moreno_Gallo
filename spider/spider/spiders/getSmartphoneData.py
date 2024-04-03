# crawl gpx spider, limit to 10 and store output in json line format file
# new terminal, cd spider
# scrapy crawl gpx -s CLOSESPIDER_PAGECOUNT=10 -o file.jl

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

class GpxSpider(scrapy.Spider):
    # Pfad zum ChromeDriver und Initialisierung des WebDriver
    chromedriver_path = '/Users/morenogallo/Desktop/ZHAW/Test_Environment_Python/chromedriver-mac-arm64/chromedriver'
    service = ChromeService(executable_path=chromedriver_path)
    browser = webdriver.Chrome(service=service)

    # Zugriff auf die Webseite
    browser.get('https://www.smartprix.com/mobiles')
    time.sleep(2)  # Wartezeit für das Laden der Seite

    # Interaktion mit der Webseite
    browser.find_element(By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[1]/input').click()
    browser.find_element(By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[2]/input').click()
    time.sleep(1)

    # Klickt auf den Button, um mehr Inhalte zu laden
    load_more_button_xpath = '//*[@id="app"]/main/div[1]/div[2]/div[3]'
    browser.find_element(By.XPATH, load_more_button_xpath).click()
    time.sleep(2)

    # Scrollen bis zum Ende der Seite
    old_height = browser.execute_script('return document.body.scrollHeight')
    while True:
        browser.find_element(By.XPATH, load_more_button_xpath).click()
        time.sleep(1)
        new_height = browser.execute_script('return document.body.scrollHeight')

        if new_height == old_height:
            break
        old_height = new_height

    # Speichert die aktuelle Seite als HTML-Datei
    html = browser.page_source
    with open('smartprix.html', 'w', encoding='utf-8') as file:
        file.write(html)
    
    # HTML-Datei öffnen und Data Preparation
    
    with open('../smartprix.html','r',encoding='utf-8') as file:
        html = file.read()
        
    html
    
    soup=BeautifulSoup(html,'html.parser')
    
    print(soup.prettify)
    
    name=[]
    price=[]
    specs=[]
    
    # Folgende Zeile neu weil containers in der for-Schlaufe gelb markiert war
    containers = soup.find_all('div', {'class': 'sm-product has-tag has-features has-actions'})

    for i in containers:
        name.append(i.find('h2').text)
        price.append(i.find('span',{'class':'price'}).text)
        try:
            specs.append(i.find('div',{'class':'score rank-2-bg'}).find('b').text)
        except:
            specs.append(np.nan)


    products = []

    for i in soup.find_all('div', {'class': 'sm-product has-tag has-features has-actions'}):
        specs = i.find('ul', {'class': 'sm-feat specs'}).find_all('li') if i.find('ul', {'class': 'sm-feat specs'}) else [None] * 8
        product = {
            'model': i.find('h2').text if i.find('h2') else np.nan,
            'price': i.find('span', {'class': 'price'}).text if i.find('span', {'class': 'price'}) else np.nan,
            'rating': i.find('div', {'class': 'score rank-2-bg'}).find('b').text if i.find('div', {'class': 'score rank-2-bg'}) and i.find('div', {'class': 'score rank-2-bg'}).find('b') else np.nan,
            'sim': specs[0].text if len(specs) > 0 and specs[0] else np.nan,
            'processor': specs[1].text if len(specs) > 1 and specs[1] else np.nan,
            'ram': specs[2].text if len(specs) > 2 and specs[2] else np.nan,
            'battery': specs[3].text if len(specs) > 3 and specs[3] else np.nan,
            'display': specs[4].text if len(specs) > 4 and specs[4] else np.nan,
            'camera': specs[5].text if len(specs) > 5 and specs[5] else np.nan,
            'card': specs[6].text if len(specs) > 6 and specs[6] else np.nan,
            'os': specs[7].text if len(specs) > 7 and specs[7] else np.nan,
        }
        products.append(product)

    df = pd.DataFrame(products)


    # JSON-File machen
    df.to_json('produkte.json', orient='records', lines=True, force_ascii=False)
    
    
    
    