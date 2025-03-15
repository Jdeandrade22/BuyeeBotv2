import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from dataBase import save_rim_links_to_db

class SearchBot:
    def __init__(self, platform, keyword, criteria, price_min, price_max):
        self.keyword = keyword
        self.criteria = [c.strip().lower() for c in criteria.split(",")]
        self.price_min = price_min
        self.price_max = price_max

    def search_buyee_rims(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://buyee.jp")
        try:
            search_box = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "query")))
            search_box.send_keys(self.keyword)
            search_box.send_keys(Keys.RETURN)
            time.sleep(0.5)
            results = driver.find_elements(By.CSS_SELECTOR, "a[href*='/item/']")
            rim_links = [
                result.get_attribute("href") for result in results
                if any(criterion in result.text.lower() for criterion in self.criteria)
            ]
            return rim_links
        finally:
            driver.quit()

    def perform_search(self):
        rim_links = self.search_buyee_rims()
        if rim_links:
            save_rim_links_to_db(rim_links)
        return rim_links