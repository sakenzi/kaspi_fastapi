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

    def parse_kaspi(self, products):
            self.open_url()
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, 'user_email_field')))
            email_input.send_keys()  

            confirm_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div/div/div/div[2]/section/section/form/button')))
            confirm_button.click()
            
            password_input = self.wait.until(EC.presence_of_element_located((By.ID, 'password_field')))
            password_input.send_keys()  
            confirm_button.click()

            button_to_list_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
            button_to_list_product_page.click()

            for product in products:
                vender_code = product['vender_code']
                min_price = product['min_price']
                max_price = product['max_price']
                step = product['step']
                market_link = product['market_link']

                print(f"Код во время парсинга: {vender_code}")

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
                            print(f"Продукт {index}: Неверный формат, пропуск")
                            continue
                        code = lines[1].strip()
                        print(f"Проверка продукта {index}: код = {code}")

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
                            competitor_price = start_for_prices(market_link)  

                            if competitor_price is True:
                                print(f"Код {vender_code}: Все хорошо, обновление цен не требуется.")
                            else:
                                competitor_price = int(competitor_price)
                                if current_price >= competitor_price:
                                    future_price = current_price - step
                                    if min_price <= future_price <= max_price:
                                        input_price.clear()
                                        input_price.send_keys(future_price)
                                        button_for_confirm_update = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/section/div/div/div[3]/button')))
                                        button_for_confirm_update.click()
                                        print(f"Код {vender_code}: Цена обновлена до {future_price}")
                                    else:
                                        print(f"Код {vender_code}: Цена {future_price} превышает установленные пределы (min: {min_price}, max: {max_price})")
                                else:
                                    print(f"Код {vender_code}: Текущая цена {current_price} цена уже ниже, чем у конкурентов {competitor_price}")

                            button_exit_product = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/div[2]/div/div[3]/div/div[2]/div/div/img')))
                            button_exit_product.click()

                            try:
                                button_to_list_product_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[2]/div/div/ul[2]/li[1]/a/div/div')))
                                button_to_list_product_page.click()
                            except Exception as nav_error:
                                continue
                            break  

                    except Exception as row_error:
                        continue

                if not product_found:
                    print(f"Код {vender_code}: В результатах поиска не найден подходящий товар")

                time.sleep(2)  

            return "Обработка завершена"

    def run(self):
        self.setup_driver()
        products = [
            {'vender_code': '593', 'min_price': 4280, 'max_price': 4290, 'step': 1, 'market_link': 'https://kaspi.kz/shop/p/netac-p500-standart-nt02p500stn-128g-r-128-gb-134445284/'},
            {'vender_code': '2168', 'min_price': 2500, 'max_price': 2800, 'step': 2, 'market_link': 'https://kaspi.kz/shop/p/europrint-npg-28-c-exv-14-chernyi-12901130/'},
            {'vender_code': '3151', 'min_price': 2712, 'max_price': 2713, 'step': 1, 'market_link': 'https://kaspi.kz/shop/p/setevoi-fil-tr-defender-es-99482-3-m-40600042/'},
            {'vender_code': '435', 'min_price': 1000, 'max_price': 2000, 'step': 1, 'market_link': 'https://kaspi.kz/shop/p/europrint-epc-pc211ev-chernyi-116910691/'},
        ]
        result = self.parse_kaspi(products)
        self.close_driver()
        return result


if __name__ == "__main__":
    def main():
        parser = KaspiParser()
        parser.run()
    main()