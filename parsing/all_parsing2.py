from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KaspiMarketForPricesParser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('headless')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.service = Service(ChromeDriverManager().install())
        self.options = options
        self.driver = None
        self.wait = None
        self.first_seller_name = None
        self.price = None

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
            first_seller_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div/div/div[1]/div/div/div[1]/table/tbody/tr[1]/td[1]/a')))
            self.first_seller_name = first_seller_name.get_attribute('textContent').strip()
            logger.info(f"Первый продавец: {self.first_seller_name}")

            first_seller_price_elem = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr:first-child td:nth-child(4) div')))
            price_text = first_seller_price_elem.get_attribute('textContent')
            self.price = re.sub(r'\D', '', price_text)
            logger.info(f"Цена первого продавца {self.first_seller_name}: {self.price}")

            if self.first_seller_name == name_market:
                try:
                    second_seller_price_elem = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div/div/div[1]/div/div/div[1]/table/tbody/tr[2]/td[4]/div')))
                    price_text = second_seller_price_elem.get_attribute('textContent')
                    second_price = re.sub(r'\D', '', price_text)
                    logger.info(f"Цена второго продавца: {second_price}")
                    return {
                        'is_kmag_first': True,
                        'second_seller_price': int(second_price) if second_price else 0,
                        'first_seller_name': self.first_seller_name,
                        'first_seller_price': int(self.price) if self.price else 0
                    }
                except Exception as e:
                    logger.error(f"Ошибка при извлечении цены второго продавца: {e}")
                    return {
                        'is_kmag_first': True,
                        'second_seller_price': 0,
                        'first_seller_name': self.first_seller_name,
                        'first_seller_price': int(self.price) if self.price else 0
                    }
            else:
                return {
                    'is_kmag_first': False,
                    'competitor_price': int(self.price) if self.price else 0,
                    'first_seller_name': self.first_seller_name,
                    'first_seller_price': int(self.price) if self.price else 0
                }

        except Exception as e:
            logger.error(f"Ошибка при парсинге продавцов: {e}")
            return None

    @property
    def first_seller(self):
        logger.info(f"First seller: {self.first_seller_name}")
        return self.first_seller_name
    
    @property
    def price_first_market(self):
        logger.info(f"Price first market: {self.price}")
        return int(self.price) if self.price else 0
    
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