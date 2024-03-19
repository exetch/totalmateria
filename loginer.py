import json
import os
import time
from loguru import logger
from fake_useragent import UserAgent
from selenium.common import TimeoutException
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv


logger.add("logs/process_log_{time}.log", rotation="1 week")
load_dotenv()


class LoginAutomation:
    def __init__(self, email, password, proxy):
        self.email = email
        self.password = password
        self.driver = None
        self.headers = None
        self.cookies = None
        # Константы для идентификаторов
        self.email_field_id = "orderForm_tb_email"
        self.password_field_id = "orderForm_tb_password"
        self.submit_button_id = "orderForm_btn_login_KTM"
        self.proxy_options = {
            "proxy": {
                "https": proxy
            }
        }

    def start_driver(self, headless=False):
        """Инициализирует драйвер."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=self.proxy_options)

    def login(self, login_url, start_url):
        """Процесс логина на сайт."""
        try:
            logger.info("Запуск драйвера...")
            self.start_driver()
            self.driver.get(login_url)
            logger.info("Ввод email и пароля...")
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.ID, self.email_field_id))
            # )
            time.sleep(5)
            email_field = self.driver.find_element(By.ID, self.email_field_id)
            email_field.send_keys(self.email)
            time.sleep(2)
            password_field = self.driver.find_element(By.ID, self.password_field_id)
            password_field.send_keys(self.password)
            time.sleep(1)
            # login_button = self.driver.find_element(By.ID, self.submit_button_id)
            # time.sleep(3)
            # login_button.click()
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 60).until(
                lambda driver: driver.current_url != login_url
            )

            logger.success("Успешный вход.")
            WebDriverWait(self.driver, 180).until(
                lambda driver: driver.current_url == start_url
            )
            time.sleep(20)
            cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
            logger.info("Cookies после входа: {}", cookies_dict)
            for request in self.driver.requests:
                if request.response and 'portal.totalmateria.com/identity/connect/token' in request.url:
                    response_body = request.response.body
                    if isinstance(response_body, bytes):
                        response_body = response_body.decode('utf-8')

                    token_data = json.loads(response_body)

                    token = token_data.get('access_token')
                    logger.info(f'Токен авторизации: {token}')
                    break
        except TimeoutException:
            logger.info("Превышено время ожидания входа на страницу")
        finally:
            self.driver.quit()



EMAIL = 'osipov2012vova82287o@rambler.ua'
PASSWORD = '1SG3V5DU'
CHECK_URL = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=EN'
START_URL = 'https://portal.totalmateria.com/en/search/quick'
PROXY = os.getenv('PROXY')

if __name__ == "__main__":
    driver = LoginAutomation(EMAIL, PASSWORD, PROXY)
    driver.login(LOGIN_URL, START_URL)


