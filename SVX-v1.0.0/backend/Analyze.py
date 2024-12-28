from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2

def analyze_per_quarter(url):
    pass    
def analyze_point_by_point(driver):
    #match history link

    button = driver.find_element(By.TAG_NAME, 'body')
    button = button.find_element(By.CSS_SELECTOR, 'div.container__detail div.container__detailInner div.filterOver div[role="tablist"]')
    link_array = button.find_elements(By.TAG_NAME, 'a')
    button = link_array[4]
    
    button.click()
    time.sleep(2)
    button = driver.find_element(By.TAG_NAME, 'body')

    quarters = button.find_elements(By.CSS_SELECTOR, 'div.container__detail div.container__detailInner div.subFilterOver div[role="tablist"] a')
    quarter_urls = []
    for link in quarters:
        quarter_urls.append(link.get_attribute('href'))

    #analyzing for each quarter
    for link in quarter_urls:
        analyze_per_quarter(link)
        

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#retrieving matches for a championship to make statistics
cur = None
conn = None
try:
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",
                            password="cuchiegras", port=5432)
    cur = conn.cursor()

    #retrieve name of all tables from database
    '''
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
    cur.execute(query)
    tables = cur.fetchall()
    for table in tables:
        print(table[0])
        '''
    #retrieving the matches urls from the database
    query = "SELECT url FROM matches;"
    cur.execute(query)
    matches_links = cur.fetchall()

except:
    raise Exception
finally:
    if cur is not None and conn is not None:
        cur.close()
        conn.close()


for url in matches_links:
    driver.get(url[0])
    analyze_point_by_point(driver)
    raise Exception

driver.quit()