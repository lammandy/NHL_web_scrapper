#TODO create CSV with player name + Dec pts + Jan pts
#TODO navigate to next 100 players 8x

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
NHL_STATS_URL = 'https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100'


class WebScrapping:
    def __init__(self):
        # install DriverManager
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.original_window = self.driver.current_window_handle
        self.driver.get(NHL_STATS_URL)

        time.sleep(2) # Let the user actually see something!
        self.num_players = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/main/div[5]/div[2]/div[2]/span[1]').get_attribute('innerHTML').split()[0]
        # 8
        # self.count = int(self.num_players) // 100
        self.count = 3
        #while loop bitches
        dict_pts = create_player_dict(self)

        create_csv(self, dict_pts)
        time.sleep(2) # Let the user actually see something!

        self.driver.quit()

def create_player_dict(self):
    #for loop of the 2nd last num changes till...
    self.field_names = ['player_name', 'dec_pts', 'jan_pts']
    all_pts = []
    page_num = 1
    while self.count > 0:
        for i in range(1, 2):
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1)
            player = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[2]/main/div[5]/div[1]/div[2]/div[{i}]/div/div[2]/div/a')))
            url = player.get_attribute('href')

            # opens player url with stats
            self.driver.switch_to.new_window('tab')
            self.driver.get(url)
            split_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section[2]/section[2]/div/section/ul/li[3]/a')))
            split_button.click()

            dec_pts = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/section[2]/section[2]/div/section/div/div[3]/div[1]/div/div/div[1]/div/table/tbody/tr[8]/td[5]/span'))).get_attribute('innerHTML')
            player_name = self.driver.find_element(By.XPATH, f'/html/body/div[3]/section[2]/section[1]/section[1]/div/div[2]/ul/li[1]/span').get_attribute('innerHTML')
            jan_pts = self.driver.find_element(By.XPATH, f'/html/body/div[3]/section[2]/section[2]/div/section/div/div[3]/div[1]/div/div/div[1]/div/table/tbody/tr[9]/td[5]/span').get_attribute('innerHTML')

            # add player and pts to dict
            player_pts = {}
            player_pts[self.field_names[0]] = player_name
            player_pts[self.field_names[1]] = dec_pts
            player_pts[self.field_names[2]] = jan_pts
            all_pts.append(player_pts)

            self.driver.close()
            self.driver.switch_to.window(self.original_window)

        self.driver.get(f"https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points&page={page_num}&pageSize=100")
        page_num += 1
        self.count -= 1
    return all_pts

def create_csv(self, all_pts):
    with open('NHL_Player_Monthly_Pts.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = self.field_names, lineterminator='\n')
        writer.writeheader()
        writer.writerows(all_pts)

WebScrapping()

