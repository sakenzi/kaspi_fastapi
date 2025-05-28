from datetime import datetime
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from all_parsing2 import start_for_prices


class KaspiParser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')
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
        self.wait = WebDriverWait(self.driver, 20)

    def open_url(self):
        self.driver.get('https://idmc.shop.kaspi.kz/login')
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()


    def parse_kaspi(self, vender_code, min_price, max_price, step):
        competitor_price = start_for_prices('https://kaspi.kz/shop/p/europrint-npg-28-c-exv-14-chernyi-12901130/')
        if competitor_price == True:
            return "Все круто"
        print(competitor_price)
        self.open_url()
        email_input = self.driver.find_element(by=By.ID, value='user_email_field')
        email_input.send_keys()

        confirm_button = self.driver.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/section/section/form/button')
        confirm_button.click()
        
        password_input = self.driver.find_element(by=By.ID, value='password_field')
        password_input.send_keys()
        confirm_button.click()

        button_to_list_product_page = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
        button_to_list_product_page.click()

        input_for_search_product = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div/div/input')))
        input_for_search_product.send_keys(vender_code)
        
        button_for_search = self.driver.find_element(By.XPATH, '/html/body/div/section/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div/p/button')
        button_for_search.click()

        link_to_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div[2]/div/section/div/div[1]/table/tbody/tr[1]/td[2]/div/div/div[2]/p[1]/a')))
        link_to_product_page.click() 

        button_to_open_update_window=self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div[2]/div/div[1]/div[2]/div[2]/div/button')))
        button_to_open_update_window.click()

        input_price = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/section/div/div/div[1]/div[2]/div/input')))
        massiv = input_price.get_attribute('value').split()
        current_price = int(massiv[0] + massiv[1])
        if current_price >= int(competitor_price):
            future_price = current_price - step
            if current_price >= min_price and current_price <= max_price:
                input_price.clear()
                input_price.send_keys(future_price)
                button_for_confirm_update = self.driver.find_element(By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/section/div/div/div[3]/button')
                button_for_confirm_update.click()
                print('Цена на товар изменен на', future_price)
            else:
                print('превышен лимит')

        time.sleep(5)

    def run(self):
        self.setup_driver()
        result = self.parse_kaspi(2168, 2620, 2700, 1)
        return result
    

if __name__ == "__main__":
    def main():
        parser = KaspiParser()
        parser.run()
    main()