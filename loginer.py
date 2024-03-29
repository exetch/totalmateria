import json
import os
import time
from loguru import logger
from fake_useragent import UserAgent
from selenium.common import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

from get_plugin import get_plugin

logger.add("logs/process_log_{time}.log", rotation="1 week")
load_dotenv()
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
current_dir = os.getcwd()
PLUGIN_NAME = os.path.join(current_dir, 'proxy_auth_plugin.zip')

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
        # self.proxy_options = {
        #     "proxy": {
        #         "https": proxy
        #     }
        # }

    def start_driver(self):
        """Инициализирует драйвер."""
        if not os.path.isfile(PLUGIN_NAME):
            get_plugin(PLUGIN_NAME, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension(PLUGIN_NAME)
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=self.proxy_options)
    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
            logger.info("Драйвер успешно закрыт.")

    def login(self, login_url, start_url, bad_url):
        """Процесс логина на сайт."""
        try:
            logger.info("Запуск драйвера...")
            self.start_driver()
            self.driver.get(login_url)
            logger.info("Ввод email и пароля...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, self.email_field_id))
            )
            email_field = self.driver.find_element(By.ID, self.email_field_id)
            email_field.send_keys(self.email)
            time.sleep(2)
            password_field = self.driver.find_element(By.ID, self.password_field_id)
            password_field.send_keys(self.password)
            time.sleep(3)
            # login_button = self.driver.find_element(By.ID, self.submit_button_id)
            # time.sleep(3)
            # login_button.click()
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 60).until(
                lambda driver: driver.current_url != login_url
            )
            if self.driver.current_url == bad_url:
                return 1, 2
            logger.success("Успешный вход.")
            WebDriverWait(self.driver, 180).until(
                lambda driver: driver.current_url == start_url
            )
            time.sleep(20)
            cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
            logger.success("Cookies после входа: {}", cookies_dict)
            for request in self.driver.requests:
                if request.response and 'portal.totalmateria.com/identity/connect/token' in request.url:
                    response_body = request.response.body
                    if isinstance(response_body, bytes):
                        response_body = response_body.decode('utf-8')

                    token_data = json.loads(response_body)

                    token = token_data.get('access_token')
                    logger.success(f'Токен авторизации: {token}')
                    headers_dict = {
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Language': 'ru-RU,ru;q=0.9',
                        'Authorization': f'Bearer {token}',
                        'Connection': 'keep-alive',
                        'Referer': 'https://portal.totalmateria.com/ru/search/quick/materials/5048801/mechanical',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        'UnitSystem': '0',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'ValueReturnMode': 'ActualAndFormattedValue',
                        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
                    break
            return cookies_dict, headers_dict
        except TimeoutException:
            logger.info("Превышено время ожидания входа на страницу")
        finally:
            self.close_driver()



EMAIL = 'osipov2012vova82287o@rambler.ua'
PASSWORD = '1SG3V5DU'
CHECK_URL = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=RU'
START_URL = 'https://portal.totalmateria.com/en/search/quick'
BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=RU'

PROXY = os.getenv('PROXY')

if __name__ == "__main__":
    driver = LoginAutomation(EMAIL, PASSWORD, PROXY)
    driver.login(LOGIN_URL, START_URL, BAD_URL, TOKEN_URL)


