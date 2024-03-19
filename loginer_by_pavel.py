import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from get_plugin import get_plugin
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PLUGIN_NAME = BASE_DIR / 'proxy_auth_plugin.zip'


class TMLogger:
    def __init__(self, login, password, plugin_name, user_agent=None):
        self.login = login
        self.password = password
        self.plugin_name = plugin_name
        self.user_agent = user_agent
        self.proxy_options = {
            "proxy": {
                "https": 'http://qCaIYyyXmyCv:OjAvEbk7jP@65.21.25.28:13529'
            }
        }

    def get_driver(self):
        if not os.path.isfile(self.plugin_name):
            get_plugin(PLUGIN_NAME, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options, seleniumwire_options=self.proxy_options)
        if self.user_agent:
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": self.user_agent})
        return driver

    def tm_login(self):
        driver = self.get_driver()
        driver.get('https://bot.sannysoft.com/')
        # time.sleep(900)
        driver.get('https://www.totalmateria.com/RU/page.aspx?ID=Login&LN=RU')
        time.sleep(5)
        email_input = driver.find_element(By.ID, 'orderForm_tb_email')
        email_input.clear()
        email_input.send_keys(self.login)
        time.sleep(2)
        password_input = driver.find_element(By.ID, value='orderForm_tb_password')
        password_input.clear()
        password_input.send_keys(self.password)
        time.sleep(2)
        password_input.send_keys(Keys.ENTER)
        time.sleep(10)
        cookies = driver.get_cookies()
        print(cookies)
        for request in driver.requests:
            if request.response and 'portal.totalmateria.com/identity/connect/token' in request.url:
                response_body = request.response.body
                if isinstance(response_body, bytes):
                    response_body = response_body.decode('utf-8')

                token_data = json.loads(response_body)

                token = token_data.get('access_token')
                print()
                print()
                print(token)
                break
        time.sleep(1000)
        driver.quit()

if __name__ == "__main__":
    my_login = 'osipov2012vova82287o@rambler.ua'
    my_password = '1SG3V5DU'
    my_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    logger = TMLogger(login=my_login, password=my_password, plugin_name=PLUGIN_NAME)
    logger.tm_login()