import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

class Smartphone(scrapy.Spider):
    name = 'smartphone_spider'
    chromedriver_path = '/Users/morenogallo/Desktop/ZHAW/Test_Environment_Python/chromedriver-mac-arm64/chromedriver'

    def __init__(self):
        service = ChromeService(executable_path=self.chromedriver_path)
        self.browser = webdriver.Chrome(service=service)

    def scrape(self):
        # Zugriff auf die Webseite
        self.browser.get('https://www.smartprix.com/mobiles')
        time.sleep(2)  # Wartezeit für das Laden der Seite
        
        # Interaktionen und Scrollen (könnte angepasst werden basierend auf der Webseite)
        # Hier können Sie den Prozess des Klickens und Scrollens entsprechend der Webseite anpassen
        # Interaktion mit der Webseite
        self.browser.find_element(By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[1]/input').click()
        self.browser.find_element(By.XPATH, '//*[@id="app"]/main/aside/div/div[5]/div[2]/label[2]/input').click()
        time.sleep(1)

        # Klickt auf den Button, um mehr Inhalte zu laden
        load_more_button_xpath = '//*[@id="app"]/main/div[1]/div[2]/div[3]'
        self.browser.find_element(By.XPATH, load_more_button_xpath).click()
        time.sleep(2)

        # Scrollen bis zum Ende der Seite
        old_height = self.browser.execute_script('return document.body.scrollHeight')
        while True:
            self.browser.find_element(By.XPATH, load_more_button_xpath).click()
            time.sleep(1)
            new_height = self.browser.execute_script('return document.body.scrollHeight')

            if new_height == old_height:
                break
            old_height = new_height

        # Speichert die aktuelle Seite als HTML
        html = self.browser.page_source
        with open('smartprix.html', 'w', encoding='utf-8') as file:
            file.write(html)

    def parse_html(self):
        with open('smartprix.html', 'r', encoding='utf-8') as file:
            html = file.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        
        products = []
        for product in soup.find_all('div', {'class': 'sm-product has-tag has-features has-actions'}):
            specs = product.find('ul', {'class': 'sm-feat specs'}).find_all('li') if product.find('ul', {'class': 'sm-feat specs'}) else [None] * 8
            product_details = {
                'model': product.find('h2').text.strip() if product.find('h2') else np.nan,
                'price': product.find('span', {'class': 'price'}).text.strip() if product.find('span', {'class': 'price'}) else np.nan,
                'rating': product.find('div', {'class': 'score'}).text.strip() if product.find('div', {'class': 'score'}) else np.nan,
                'sim': specs[0].text.strip() if len(specs) > 0 else np.nan,
                'processor': specs[1].text.strip() if len(specs) > 1 else np.nan,
                'ram': specs[2].text.strip() if len(specs) > 2 else np.nan,
                'battery': specs[3].text.strip() if len(specs) > 3 else np.nan,
                'display': specs[4].text.strip() if len(specs) > 4 else np.nan,
                'camera': specs[5].text.strip() if len(specs) > 5 else np.nan,
                'card': specs[6].text.strip() if len(specs) > 6 else np.nan,
                'os': specs[7].text.strip() if len(specs) > 7 else np.nan,
            }
            products.append(product_details)
        
        return products

    def save_to_json(self, products):
        df = pd.DataFrame(products)
        df.to_json('produkte.json', orient='records', lines=True, force_ascii=False)

    def run(self):
        self.scrape()
        products = self.parse_html()
        self.save_to_json(products)
        self.browser.quit()
        print("Scraping completed and data saved to produkte.json")

if __name__ == '__main__':
    spider = Smartphone()
    spider.run()
