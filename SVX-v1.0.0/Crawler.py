from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChampionshipLinks:
    def __init__(self, sport_name, country, division):
        self.sport_name = sport_name
        self.country = country
        self.division = division

    def get_link_prefix(self) -> str:
        return f"https://www.flashscore.com/{self.sport_name}/{self.country}/{self.division}"

def retrieve_country_links(driver, list_of_links, sport):
    temp = driver.find_element(By.CLASS_NAME, 'lmc__menu')
    button = temp.find_element(By.CLASS_NAME, 'lmc__itemMore')
    # Attempt a standard click
    try:
        button.click()
    except:
        # Use JavaScript if normal click fails
        driver.execute_script("arguments[0].click();", button)

    links_of_the_countries = temp.find_elements(By.CLASS_NAME, 'lmc__block')
    for link in links_of_the_countries:
    
            # button = WebDriverWait(link, 1).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, '.lmc__block .lmc__item'))
            # )
            button = link.find_element(By.CSS_SELECTOR, '.lmc__block .lmc__item')
            try:
                button.click()
            except:
                driver.execute_script("arguments[0].click();", button)
            

    leagues = driver.find_elements(By.CLASS_NAME, 'lmc__template')
    for league in leagues:
        name = league.find_element(By.TAG_NAME, 'a')
        name = name.get_attribute('href')
        name = name.split('/')
        country = name[4]
        division = name[5]
        list_of_links.append(ChampionshipLinks(sport, country, division))


sport = input("Enter the sport: ")
sport_url = f"https://www.flashscore.com/{sport}/"
list_of_links : List[ChampionshipLinks] = []
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(sport_url)

#start = time.time()
retrieve_country_links(driver, list_of_links, sport)

#end = time.time()
# print(end-start)
# raise type
for ch in list_of_links:
    official_link = ch.get_link_prefix()
    print(official_link)
driver.quit()


