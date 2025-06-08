from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from parsing.all_parsing2 import start_for_prices
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KaspiParser:
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
        self.wait = WebDriverWait(self.driver, 20)

    def open_url(self):
        self.driver.get('https://idmc.shop.kaspi.kz/login')
    
    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def parse_kaspi(self, products, kaspi_email: str, kaspi_password: str):
            self.open_url()
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, 'user_email_field')))
            email_input.send_keys(kaspi_email)

            confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div/div[2]/section/section/form/button')))
            confirm_button.click()
            
            password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'password_field')))
            password_input.send_keys(kaspi_password)
            confirm_button.click()

            button_to_list_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
            button_to_list_product_page.click()

            for product in products:
                vender_code = product['vender_code']
                min_price = product['min_price']
                max_price = product['max_price']
                step = product['step']
                market_link = product['market_link']

                if not all([vender_code, min_price, max_price, step, market_link]):
                    logger.warning(f"Пропуск продукта {vender_code}: отсутствуют необходимые данные")
                    continue

                try:
                    input_for_search_product = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div/div/input')))
                    input_for_search_product.clear()
                    input_for_search_product.send_keys(vender_code)
                    
                    button_for_search = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[2]/div/div[4]/div[1]/div[1]/div/div/div/div/p/button')))
                    button_for_search.click()

                    product_rows = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.subtitle.is-6')))
                    product_found = False

                    for index, row in enumerate(product_rows, start=1):
                        try:
                            row_text = row.text
                            lines = row_text.split('\n')
                            if len(lines) < 2:
                                logger.warning(f"Продукт {index}: Неверный формат, пропуск")
                                continue
                            code = lines[1].strip()
                            logger.info(f"Проверка продукта {index}: код = {code}")

                            if vender_code == code:
                                product_found = True
                                row_xpath = f'/html/body/div[1]/section/div[2]/div/section/div/div[1]/table/tbody/tr[{index}]/td[2]/div/div/div[2]/p[1]/a'
                                link_to_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, row_xpath)))
                                link_to_product_page.click()

                                button_to_open_update_window = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section/div[2]/div/div[1]/div[2]/div[2]/div/button')))
                                button_to_open_update_window.click()

                                input_price = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/section/div/div/div[1]/div[2]/div/input')))
                                massiv = input_price.get_attribute('value').split()
                                current_price = int(''.join(massiv))
                                
                                try:
                                    competitor_price = start_for_prices(market_link)
                                    if competitor_price is True:
                                        logger.info(f"Код {vender_code}: Все хорошо, обновление цен не требуется.")
                                    else:
                                        competitor_price = int(competitor_price)    
                                        if current_price >= competitor_price:
                                            future_price = current_price - step
                                            if min_price <= future_price <= max_price:
                                                input_price.clear()
                                                input_price.send_keys(future_price)
                                                button_for_confirm_update = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/section/div/div/div[3]/button')))
                                                # button_for_confirm_update.click()  
                                                logger.info(f"Код {vender_code}: Цена обновлена до {future_price}")
                                            else:
                                                logger.warning(f"Код {vender_code}: Цена {future_price} превышает пределы (min: {min_price}, max: {max_price})")
                                        else:
                                            logger.info(f"Код {vender_code}: Текущая цена {current_price} уже ниже, чем у конкурентов {competitor_price}")
                                except ValueError as ve:
                                    continue
                                except Exception as e:
                                    continue

                                button_exit_product = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/div/img')))
                                button_exit_product.click()

                                try:
                                    button_to_list_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
                                    button_to_list_product_page.click()
                                except Exception as nav_error:
                                    logger.error(f"Код {vender_code}: Ошибка возврата к списку продуктов: {str(nav_error)}")
                                    continue

                                break

                        except Exception as row_error:
                            logger.error(f"Код {vender_code}, продукт {index}: Ошибка обработки строки: {str(row_error)}")
                            continue

                    time.sleep(2)

                except Exception as product_error:
                    button_to_list_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
                    button_to_list_product_page.click()
                    continue

            logger.info("Обработка завершена")
            return "Обработка завершена"

    def run(self, products=None, kaspi_email=None, kaspi_password=None):
        self.setup_driver()
        result = self.parse_kaspi(products, kaspi_email, kaspi_password)
        self.close_driver()
        return result

if __name__ == "__main__":
    def main():
        parser = KaspiParser()
        parser.run()
    main()