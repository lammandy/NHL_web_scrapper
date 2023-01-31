#TODO create list or dictionary of links to player stats
#TODO create CSV with player name + Dec pts + Jan pts
#TODO navigate to next 100 players 8x

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

NHL_STATS_URL = 'https://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20222023&seasonTo=20222023&gameType=2&filter=gamesPlayed,gte,1&sort=points&page=0&pageSize=100'


class WebScrapping:
    def __init__(self):
        # install DriverManager
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.original_window = self.driver.current_window_handle
        self.driver.get(NHL_STATS_URL);

        time.sleep(2) # Let the user actually see something!

        dict_pts = create_player_dict(self)
        print(dict_pts)
        time.sleep(2) # Let the user actually see something!

        self.driver.quit()

def create_player_dict(self):
        #for loop of the 2nd last num changes till...
        field_names = ['player_name', 'dec_pts', 'jan_pts']
        pts = []
        for i in range(1, 3):
            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=1 )
            player = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[1]/div[2]/main/div[5]/div[1]/div[2]/div[{i}]/div/div[2]/div/a')))
            url = player.get_attribute('href')
            # opens player url with stats
            self.driver.switch_to.new_window('tab')
            self.driver.get(url)
            split_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/section[2]/section[2]/div/section/ul/li[3]/a')))
            split_button.click()

            wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/section[2]/section[1]/section[1]/div/div[2]/ul/li[1]/span')))
            player_name = self.driver.find_element(By.XPATH, f'/html/body/div[3]/section[2]/section[1]/section[1]/div/div[2]/ul/li[1]/span').get_attribute('innerHTML')
            print(player_name)
            dec_pts = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/section[2]/section[2]/div/section/div/div[3]/div[1]/div/div/div[1]/div/table/tbody/tr[8]/td[5]/span'))).get_attribute('innerHTML')
            jan_pts = wait.until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[3]/section[2]/section[2]/div/section/div/div[3]/div[1]/div/div/div[1]/div/table/tbody/tr[9]/td[5]/span'))).get_attribute('innerHTML')
            print(player_name, dec_pts, jan_pts)
            # find xpath of Jan and Dec

            # get/write dict of Player name, Jan and Dec into pts

            self.driver.close()
            self.driver.switch_to.window(self.original_window)

            pts.append(url)
            time.sleep(2)
        return pts

WebScrapping()

