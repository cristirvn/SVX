from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from typing import List
import configparser

from sqlalchemy import create_engine, Column, String, Integer, CHAR, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

path = r"C:\Users\User\Desktop\workspace2\chromedriver-win64\chromedriver.exe"
service = Service(path)
driver = webdriver.Chrome(service=service)

driver.get(sport_url)

retrieve_country_links(driver, list_of_links, sport)
driver.quit()

#created a table in database using sqlalchemy to store the championship links
Base = declarative_base()

config = configparser.ConfigParser()
config.read("config.ini")

db_user = config["database"]["user"]
db_password = config["database"]["password"]
db_host = config["database"]["host"]
db_port = config["database"]["port"]
db_name = config["database"]["dbname"]

# Create the database URL dynamically
database_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Link(Base):
    __tablename__ = "championship_links"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    url = Column("url", String)
    sport = Column("sport", String)  
    country = Column("country", String)
    league = Column("league", String)
    Created_at = Column(TIMESTAMP, server_default=func.now())  # Automatically set timestamp

    def __init__(self, url, sport, country, league):
        self.url = url
        self.sport = sport
        self.country = country
        self.league = league


engine = create_engine(database_url, echo = True)
Base.metadata.create_all(bind = engine)

Session = sessionmaker(bind = engine)
session = Session()

#adding the championships links in the data base
# session.query(Link).filter(Link.id >= 407, Link.id <= 808).delete(synchronize_session=False)

for ch in list_of_links:
    official_link = ch.get_link_prefix()
    element = Link(official_link, sport, ch.country, ch.division)
    session.add(element)

session.commit()
session.close()