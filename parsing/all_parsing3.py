from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KaspiMarketForPricesParser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.service = Service(ChromeDriverManager().install())
        self.options = options
        self.driver = None
        self.wait = None
        self.first_seller_name = None

    def setup_driver(self):
        self.driver = webdriver.Chrome(options=self.options, service=self.service)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)

    def open_url(self, url):
        self.driver.get(url)
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def parse_kaspi(self, name_market):
        try:
            first_seller_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr:first-child td a')))
            self.first_seller_name = first_seller_name.get_attribute('textContent').strip()
            logger.info(f"First seller: {self.first_seller_name}")

            if self.first_seller_name == name_market:
                return True
            else:
                competitor_price = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr:first-child td:nth-child(4) div')))
                price_text = competitor_price.get_attribute('textContent')
                self.price = re.sub(r'\D', '', price_text)
                logger.info(f"Competitor {self.first_seller_name} price: {self.price}")
                return int(self.price) if self.price else 0
        except Exception as e:
            logger.error(f"Ошибка при парсинге продавца: {e}")
            return None

    @property
    def first_seller(self):
        logger.info(f"First_seller_name: {self.first_seller_name}")
        return self.first_seller_name
    
    @property
    def price_first_market(self):
        return int(self.price)
    
    def run(self, name_market):
        self.setup_driver()
        try:
            result = self.parse_kaspi(name_market)
        finally:
            self.close_driver()
        return result

def start_for_prices(url):
    parser = KaspiMarketForPricesParser()
    parser.setup_driver()
    try:
        parser.open_url(url)
        result = parser.parse_kaspi('k-MAG')
    finally:
        parser.close_driver()
    return result