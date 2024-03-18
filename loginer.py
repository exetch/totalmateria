import time
from loguru import logger
from fake_useragent import UserAgent
from selenium.common import TimeoutException
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logger.add("logs/process_log_{time}.log", rotation="1 week")



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
        # chrome_options.add_argument("--proxy-server=65.21.25.28:13529")
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
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.email_field_id))
            )

            email_field = self.driver.find_element(By.ID, self.email_field_id)
            email_field.send_keys(self.email)
            time.sleep(5)
            password_field = self.driver.find_element(By.ID, self.password_field_id)
            password_field.send_keys(self.password)
            time.sleep(1)
            login_button = self.driver.find_element(By.ID, self.submit_button_id)
            time.sleep(3)
            login_button.click()
            WebDriverWait(self.driver, 60).until(
                lambda driver: driver.current_url != login_url
            )

            logger.success("Успешный вход.")
            WebDriverWait(self.driver, 180).until(
                lambda driver: driver.current_url == start_url
            )
            cookies = self.driver.get_cookies()
            cookies_dict = {}
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie['value']
            logger.info("Cookies после входа: {}", cookies_dict)
        except TimeoutException:
            logger.info("Превышено время ожидания входа на страницу")
        finally:
            self.close_driver()

    def close_driver(self):
        """Закрывает драйвер."""
        if self.driver:
            self.driver.quit()


EMAIL = 'vdpcxsmtsw@rambler.ru'
PASSWORD = 'X0NQIBWA'
CHECK_URL = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=EN'
START_URL = 'https://portal.totalmateria.com/en/search/quick'
# PROXY = 'http://qCaIYyyXmyCv:OjAvEbk7jP@65.21.25.28:13529'
PROXY = 'http://0e45f25ff7:702ff64e5f@188.120.243.158:40710'

if __name__ == "__main__":
    driver = LoginAutomation(EMAIL, PASSWORD, PROXY)
    # driver.login(CHECK_URL, CHECK_URL)
    driver.login(LOGIN_URL, START_URL)


