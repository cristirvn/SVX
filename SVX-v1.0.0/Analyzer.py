from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
def pre_game_odds_analyze(driver):
    pass

def point_by_point_analyze(driver):
    sections_button = driver.find_element(By.TAG_NAME, 'body')
    sections_button = sections_button.find_element(By.CSS_SELECTOR, 'div.container__detail div.container__detailInner div.filterOver div[role="tablist"]')
    links_of_each_section = sections_button.find_elements(By.TAG_NAME, 'a')
    match_history_link = links_of_each_section[4]
    
    match_history_link.click()
    time.sleep(2)
    match_history_button = driver.find_element(By.TAG_NAME, 'body')

    quarters = match_history_button.find_elements(By.CSS_SELECTOR, 'div.container__detail div.container__detailInner div.subFilterOver div[role="tablist"] a')
    quarter_urls = []
    for link in quarters:
        quarter_urls.append(link.get_attribute('href'))
    
    maximum_differences = []
    quart = 1
    for q in quarter_urls:
        max_dif_quarter = 0
        end_score_dif = 0
        driver.get(q)
        match_details = driver.find_element(By.CSS_SELECTOR, ".container__detail .container__detailInner .duelParticipant")
       
        overall_score = match_details.find_element(By.CSS_SELECTOR, ".duelParticipant__score .detailScore__matchInfo .detailScore__wrapper").find_elements(By.TAG_NAME, "span")
        home_score = int(overall_score[0].text)
        away_score = int(overall_score[2].text)

        home_team = match_details.find_element(By.CSS_SELECTOR, ".duelParticipant__home .participant__participantNameWrapper .participant__participantName").text
        away_team = match_details.find_element(By.CSS_SELECTOR, ".duelParticipant__away  .participant__participantNameWrapper .participant__participantName").text
        if home_score > away_score:
            points = driver.find_element(By.TAG_NAME, 'body').find_element(By.CLASS_NAME, 'matchHistoryRowWrapper').find_elements(By.CLASS_NAME, 'matchHistoryRow')
            #store the last element to get the ending score of the quarter
            end_score = points[-1]

            #store the maximum ahead difference for the winner team
            maxx_dif = 0
            for point in points:
                difference = point.find_element(By.CSS_SELECTOR, ".matchHistoryRow__home").text
                if difference:
                    maxx_dif = max(maxx_dif, int(difference))
            
            #getting the difference between winner team score and loser team score at the end of each quarter
            end_score = end_score.find_elements(By.CSS_SELECTOR, '.matchHistoryRow__scoreBox .matchHistoryRow__score')
            end_maximum_dif = int(end_score[0].text) - int(end_score[1].text)

        else:
            points = driver.find_element(By.TAG_NAME, 'body').find_element(By.CLASS_NAME, 'matchHistoryRowWrapper').find_elements(By.CLASS_NAME, 'matchHistoryRow')
            #store the last element to get the ending score of the quarter
            end_score = points[-1]
            #store the maximum ahead difference for the winner team
            maxx_dif = 0
            for point in points:
                difference = point.find_element(By.CSS_SELECTOR, ".matchHistoryRow__away").text
                if difference:
                    maxx_dif = max(maxx_dif, int(difference))

            #getting the difference between winner team score and loser team score at the end of each quarter
            end_score = end_score.find_elements(By.CSS_SELECTOR, '.matchHistoryRow__scoreBox .matchHistoryRow__score')
            end_maximum_dif = int(end_score[1].text) - int(end_score[0].text)

        maximum_differences.append([maxx_dif, end_maximum_dif])

    for el in maximum_differences:
        print(el)
    #analising the data differences to check where the match is lost
    negative_difference = 0 # represent quarter where winner team conducted in points, but in the end was conducted
    array_index = 0
    for data in maximum_differences:
        if data[1] < 0:
            negative_difference = array_index
        array_index += 1
    
    #itterate from negative_difference index, to check where the match is lost
    if negative_difference + 1 == 4: print("We can tell that the ending result is predictable only in the 4th quarter")
    else:
        #calculate what quarter has had the bigges difference points at its end

        end_difference = 0 #difference at the end of the match
        quarter_var = 0 #variable to memorate the quarter where match is lost
        ahead_points = 0 #difference of points that the winner team had in specified qurter

        for quarter in range(negative_difference + 1, 4):
            data = maximum_differences[quarter]
            if(data[1] > end_difference):
                end_difference = data[1]
                quarter_var = quarter + 1
                ahead_points = data[0]
            elif data[1] == end_difference:
                if data[0] > ahead_points:
                    ahead_points = data[0]
                    quarter_var = quarter + 1

        print(f"Match is lost in quarter {quarter_var}.")
            


    '''
    https://www.flashscore.com/match/UwgPkSbe/#/match-summary
    https://www.flashscore.com/match/G8tb11YB/#/match-summary
    https://www.flashscore.com/match/4Gc0hc2t/#/match-summary -- probleme
    https://www.flashscore.com/match/pYewaWy9/#/match-summary
    https://www.flashscore.com/match/8Mymz4VN/#/match-summary
    https://www.flashscore.com/match/E9VrHHOb/#/match-summary
        q maximum_dif end_score
        1  7           22-20 = 2
        2  4           37-45 = -8 dif negativa => loserii conduc
        3  5           68-65 = 3
        4  9           95-92 = 3
        {7,2}, {4,-8}, {5,3}, {9,3}
        runda 4

    https://www.flashscore.com/match/SICIIzaA/#/match-summary
        1  8           22-25 = 3
        2  5           49-45 = -4
        3  0           69-67 = -2
        4  0           93-94 = 1

    '''


match_link = input("Enter link of the match: ")
chrome_options = Options().add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(match_link)

point_by_point_analyze(driver)

driver.quit()