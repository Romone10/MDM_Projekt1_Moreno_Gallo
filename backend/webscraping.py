from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time

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
    
