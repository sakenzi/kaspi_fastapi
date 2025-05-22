from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


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
        first_seller_name = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div/div/div[1]/div/div/div[1]/table/tbody/tr[1]/td[1]/a')))
        first_seller_name = first_seller_name.get_attribute('textContent')
        if first_seller_name == name_market:
            return True
        else:
            competitor_price = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div[3]/div/div/div[1]/div/div/div[1]/table/tbody/tr[1]/td[4]/div')
            massiv = competitor_price.get_attribute('textContent').split()
            # need to input in Postgres about competitor_price
            print(first_seller_name, "у него цена", massiv[0]+massiv[1])
            price = massiv[0] + massiv[1]
            return int(price)

    def run(self):
        result =  self.parse_kaspi()
        return result
    

# if __name__ == "__main__":
def start_for_prices(url):
    parser = KaspiMarketForPricesParser()
    parser.setup_driver()
    parser.open_url(url)
    result = parser.parse_kaspi('k-MAG')
    parser.close_driver()
    return result
    # main()