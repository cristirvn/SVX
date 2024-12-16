from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from typing import List
from dataclasses import dataclass
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import os.path
import configparser
import os
import csv 
from Drive_backup import upload_to_google_drive, upload_to_gdrive_by_key

@dataclass
class Match:
    sport : str
    date: str
    ROUND: str
    home: str
    away: str
    home_score: int
    away_score: int
    home_score_by_period : List[int]
    away_score_by_period: List[int]
    url : str
    country : str
    division : str
    season : str

    def printing(self):
        return f"{self.ROUND}, {self.date}, {self.home}, {self.away}, {self.home_score}, {self.away_score}, {self.sport}, {self.url}"


def add_date(temp_data, year):
        temp_data[1] = temp_data[1] +' '+ year
        return ' '.join(temp_data)

def get_urls(driver):
    elems = driver.find_elements(By.CSS_SELECTOR, '.event__match')
    urls = []
    for elem in elems:
        try:
            temp_url = elem.find_element(By.CSS_SELECTOR, '.eventRowLink').get_attribute('href')
            urls.append(temp_url)
        except:
            pass
    return urls


def crawl_championship(championship_url: str, file_to_upload) -> List[Match]:
    Champ_list : List[Match] = []
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=chrome_options)
    path = r"C:\Users\User\Desktop\workspace2\chromedriver-win64\chromedriver.exe"
    service = Service(path)
    driver = webdriver.Chrome(service=service)
    driver.get(championship_url)
    wait = WebDriverWait(driver, 3)
    
    temp_years = season.split('-')
    while True:
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".event__more")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
        except:     
            break
    urls = get_urls(driver)
    url_index = 0

    table = driver.find_element(By.CSS_SELECTOR, '.sportName')
    table_text = table.text
    with open("matches.txt", "w") as file:
        file.write(table_text)

    with open("matches.txt", "r") as file:
        lines = file.readlines()

    current_date = ""
    home_team = ""
    away_team = ""
    home_score = ""
    away_score = ""
    ROUND = ""
    home_score_by_period =""
    away_score_by_period=""
    anterior_month = ""
    def is_integer(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    with open(file_to_upload, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sport', 'Date', 'Round', 'Home_team', 'Away_team', 'Home_score', 'Away_score','Home_score_by_period',
                                 'Away_score_by_period', 'Match_url', 'Country', 'Divison', 'Season'])
        for line in lines:
            line = line.strip()
        
            if 'ROUND' in line and ROUND != line:
                if current_date and home_team and away_team and home_score and away_score:
                    away_score = int(away_score)
                    home_score = int(home_score)
                    if anterior_month != '12':
                        temp_date = current_date.split('.')
                        #getting the anterior month for each match
                        anterior_month = temp_date[1]

                    try:
                        if current_date:
                            temp_date = current_date.split('.')
                            if anterior_month == '12':
                                current_date = add_date(temp_date, temp_years[0])
                            elif int(anterior_month) <= 12:
                                current_date = add_date(temp_date, temp_years[1])
                    except:
                        pass
                    match = [sport, current_date, ROUND, home_team, away_team, home_score,
                                     away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"]
                    writer.writerow(match)
                    Champ_list.append(Match(sport, current_date, ROUND, home_team, away_team, home_score,
                                away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"))
                    url_index += 1
                    
                
                home_team = ""
                away_team = ""
                home_score = ""
                away_score = ""
                current_date = ""
                home_score_by_period=[]
                away_score_by_period=[]

            if "ROUND" in line:
                ROUND = line
            elif "FINAL" in line:
                ROUND = line
            elif "SEMI-FINALS" in line or "QUARTER-FINALS" in line or "PLACE" in line or "Group" in line or "Relegation" in line:
                ROUND = line
            
            if "AOT" in line:
                continue
            if ":" in line:

                if current_date and home_team and away_team and home_score and away_score:
                    away_score = int(away_score)
                    home_score = int(home_score)
                    if anterior_month != '12':
                        temp_date = current_date.split('.')
                        #getting the anterior month for each match
                        anterior_month = temp_date[1]

                    try:
                            if current_date:
                                temp_date = current_date.split('.')
                            if anterior_month == '12':
                                current_date = add_date(temp_date, temp_years[0])
                            elif int(anterior_month) <= 12:
                                current_date = add_date(temp_date, temp_years[1])
                            

                    except:
                        pass
                    match = [sport, current_date, ROUND, home_team, away_team, home_score,
                                     away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"]
                    writer.writerow(match)
                    Champ_list.append(Match(sport, current_date, ROUND, home_team, away_team, home_score,
                                away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"))
                    url_index += 1
                
                current_date = ""
                home_team = ""
                away_team = ""
                home_score = ""
                away_score = ""
                home_score_by_period=[]
                away_score_by_period=[]
                current_date = line

            elif isinstance(line, str) and home_team == "":
                home_team = line
            elif isinstance(line, str) and away_team == "":
                away_team = line
            elif is_integer(line) and home_score == "":
                home_score = line
            elif home_score and away_score == "":
                away_score = line
            else:
                try:
                    if len(home_score_by_period) == len(away_score_by_period):
                        home_score_by_period.append(int(line))
                    else:
                        away_score_by_period.append(int(line))
                except:
                    pass
        temp_date = current_date.split('.')
        current_date = add_date(temp_date, temp_years[0])
        match = [sport, current_date, ROUND, home_team, away_team, home_score,
                                     away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"]
        writer.writerow(match)
        Champ_list.append(Match(sport, current_date, ROUND, home_team, away_team, home_score,
                                away_score,home_score_by_period, away_score_by_period, urls[url_index], country, division, f"{temp_years[0]}-{temp_years[1]}"))
        
        driver.quit()
        return Champ_list

def insert_match(cur, match: Match):
    insert_query = """
    INSERT INTO matches (
        sport, date, round, home, away, home_score, away_score, 
        home_score_by_period, away_score_by_period, url, country, division, season
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(insert_query, (
        match.sport,
        match.date,
        match.ROUND,
        match.home,
        match.away,
        match.home_score,
        match.away_score,
        match.home_score_by_period,
        match.away_score_by_period,
        match.url,
        match.country,
        match.division,
        match.season
    ))


sport = input("Enter sport: ")
country = input("Enter country: ")
division = input("Enter division: ")
season = input("enter the season with '-'(e.g: 2006-2007): ")

link = f"https://www.flashscore.com/{sport}/{country}/{division}-{season}/results/"
file_to_upload =f"{country}-{division}-{season}.csv"
matches : List[Match] = []

if not os.path.exists(file_to_upload):
    matches = crawl_championship(link, file_to_upload)

config = configparser.ConfigParser()
config.read("config.ini")
db_host = config["database"]["host"]
db_name = config["database"]["dbname"]
db_user = config["database"]["user"]
db_password = config["database"]["password"]
db_port = config["database"]["port"]
cur = None
conn = None
try:
    conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user,
                            password=db_password, port=db_port)
    cur = conn.cursor()
    # SQL statement to create the 'matches' table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS matches (
        id SERIAL PRIMARY KEY,
        sport VARCHAR(50),
        date DATE,
        round VARCHAR(50),
        home VARCHAR(100),
        away VARCHAR(100),
        home_score INT,
        away_score INT,
        home_score_by_period INT[],
        away_score_by_period INT[],
        url TEXT,
        country VARCHAR(50),
        division VARCHAR(50),
        season VARCHAR(20)
    );
    """

    # Execute the SQL query to create the table
    cur.execute(create_table_query)
    for match in matches:
        insert_match(cur, match)
    conn.commit()

except:
    raise Exception
finally:
    if cur is not None and conn is not None:
        cur.close()
        conn.close()
        
upload_to_gdrive_by_key(file_to_upload)


