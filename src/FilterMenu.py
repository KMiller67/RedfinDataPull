import time

from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait


class HomeTypes(Enum):
    HOUSE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[1]/div'
    TOWNHOUSE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[2]/div'
    CONDO = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[3]/div'
    LAND = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[4]/div'
    MULTIFAMILY = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[5]/div'
    MOBILE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[6]/div'
    COOP = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[7]/div'
    OTHER = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[8]/div'


def home_type_select(home_types: list, driver: webdriver):
    """
    Helper function to select the home type(s) the user desires to pull data for; this function is intended to be used
    AFTER the 'All Filters' dropdown has been clicked
    :param home_types: List of all home types the user desires to pull data for; Options include: house, townhouse,
    condo, land, multi-family, mobile, co-op, and other
    :param driver: Webdriver used for webscraping
    :return: N/A; used only to select desired home types on Redfin website
    """
    # Ensure home types are uppercase and dashes are removed
    home_types = map(lambda x: x.upper().replace('-', ''), home_types)

    # Select desired home types within the Redfin 'All Filters' dropdown
    for home_type in home_types:
        try:
            driver.find_element(By.XPATH, HomeTypes[home_type].value).click()
        except KeyError:
            print(f'Home type {home_type} is not an available filter option. {home_type} not selected.')
            continue


class FilterMenu:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def openMenu(self):
        # Click 'All Filters'; Set to show 'For Sale' listings only by default
        self.driver.find_element(By.XPATH, '//*[@id="sidepane-header"]/div/div[1]/form/div[5]/div').click()
        # time.sleep(1.5)

    def selectSoldData(self):
        self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[1]/div/div/div/div/div/div/div[3]').click()
        # time.sleep(1.5)

    def selectHomeTypes(self, home_types: list):
        home_type_header = self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[5]/div[1]/div/span')
        self.driver.execute_script("return arguments[0].scrollIntoView();", home_type_header)   # Find Home Type header
        # time.sleep(1.5)

        if type(home_types) == str:  # If user selects single home type (string), convert it to a list
            home_types = [home_types]
        home_type_select(home_types=home_types, driver=self.driver)
        # time.sleep(1.5)

    def selectComingSoonCheckbox(self):
        # Listing status set to both 'Coming Soon' and 'Active' by default; First click unchecks 'Coming Soon'
        self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[1]/div/div[2]/span[1]/label/span[1]').click()
        # time.sleep(1.5)

    def selectTimeOnRedfin(self, time_on_redfin: str):
        # Set to only include listings from the last 7 days (reduces # of homes to download; need to keep < 350)
        select = Select(self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[6]/div[2]/div[2]/span/span/select'))
        select.select_by_visible_text(time_on_redfin)   # Enter time_on_redfin as in dropdown; ex. 'Less than 7 days'
        # time.sleep(1.5)

    def selectForeclosuresCheckbox(self):
        # Turn off 'Foreclosures' listing type; checked by default
        listing_type_header = self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[1]/div/span')
        self.driver.execute_script('return arguments[0].scrollIntoView()', listing_type_header)     # Find Listing Type header
        self.driver.find_element(By.XPATH, '//*[@id="filterContent"]/div/div[10]/div[2]/div/div[1]/div[2]/span/label/span[1]').click()
        # time.sleep(1.5)

    def closeMenu(self):
        self.driver.find_element(By.XPATH, '//*[@id="right-container"]/div[6]/div/aside/header/button').click()
        time.sleep(1.5)
