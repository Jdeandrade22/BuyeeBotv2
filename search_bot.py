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
        self.platform = platform
        self.keyword = keyword
        self.criteria = [c.strip().lower() for c in criteria.split(",")]
        self.price_min = price_min
        self.price_max = price_max
    def search_buyee_rims(self):
        options = webdriver.ChromeOptions()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Adjust as needed
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
    def search_ebay_rims(self):
        ebay_api_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        headers = {'Authorization': 'Bearer YOUR_EBAY_API_KEY'}
        params = {
            'q': self.keyword,
            'filter': f'price:[{self.price_min}..{self.price_max}]',
            'limit': 10
        }
        response = requests.get(ebay_api_url, headers=headers, params=params)
        if response.status_code == 200:
            items = response.json().get('itemSummaries', [])
            rim_links = [item['itemWebUrl'] for item in items if
                         any(criterion in item['title'].lower() for criterion in self.criteria)]
            return rim_links
        else:
            print(f"Error fetching eBay data: {response.status_code}")
            return []
    def perform_search(self):
        if self.platform == 'Buyee':
            rim_links = self.search_buyee_rims()
        elif self.platform == 'eBay':
            rim_links = self.search_ebay_rims()
        else:
            rim_links = []
        if rim_links:
            save_rim_links_to_db(rim_links)
        return rim_links