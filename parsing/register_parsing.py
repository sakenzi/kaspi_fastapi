import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException


class KaspiParser:
    def __init__(self):
        options = Options()
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
        SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")
        self.driver =  webdriver.Remote(
            command_executor=SELENIUM_REMOTE_URL,
            options=self.options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 20)

    def open_url(self):
        print('open url')
        self.driver.get('https://idmc.shop.kaspi.kz/login')
    
    def close_driver(self):
        print('close url')

        if self.driver:
            self.driver.quit()

    def parse_kaspi(self, kaspi_email: str, kaspi_password: str):
        print('start url')

        self.open_url()
        email_input = self.driver.find_element(by=By.ID, value='user_email_field')
        print('email_input url')

        email_input.send_keys(kaspi_email)

        confirm_button = self.driver.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/section/section/form/button')
        confirm_button.click()
        print('confirm_button', )

        password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'password_field')))
        password_input.send_keys(kaspi_password)
        confirm_button.click()
        
        time.sleep(2)
        try:
            self.driver.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/section/section/form/div/a')
            print("Пароль или email неверный")
            return False, None
        except NoSuchElementException:
           print("Авторизация успешна")

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[3]/li[3]/a'))).click()

        name_market = self.wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div/section/div[2]/div/section/div/section/div[1]/section/div[1]/div/div[3]/div[2]/strong')))
        
        print(name_market.text)
        return True, name_market.text
        
    def run(self):
        self.setup_driver()
        result = self.parse_kaspi()
        return result
    

if __name__ == "__main__":
    def main():
        parser = KaspiParser()
        parser.run()
    main()