import asyncio
import json
import os
from datetime import time

from dotenv import load_dotenv
from pyppeteer import launch, errors
from pyppeteer.errors import TimeoutError
from loguru import logger
from pyppeteer_registration import FingerprintManager
from browserforge.injectors.pyppeteer import NewPage

load_dotenv()
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PROXY = PROXY_HOST + ':' + PROXY_PORT
EMAIL = 'peirohmyre1976@yahoo.com'
PASSWORD = 'A5R2PL70'
CHECK_URL = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=RU'
START_URL = 'https://portal.totalmateria.com/ru/search/quick'
BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=RU'
URL_KEYWORD = 'identity/connect/token'

class LoginAutomationPyppeteer:
    def __init__(self, custom_browser, email, password, logger):
        self.custom_browser = custom_browser
        self.email = email
        self.password = password
        self.logger = logger
        self.auth_token = None
        self.email_field_id = "orderForm_tb_email"
        self.password_field_id = "orderForm_tb_password"
        self.submit_button_id = "orderForm_btn_login_KTM"

    async def extract_token_from_response(self, url_keyword):
        async def check_response(response):
            url = response.url
            if url_keyword in url:
                self.logger.info(f"Обнаружен URL, содержащий ключевое слово '{url_keyword}'.")
                try:
                    response_body = await response.text()
                    token_data = json.loads(response_body)
                    if "access_token" in token_data:
                        self.auth_token = token_data["access_token"]
                        self.logger.success(f"Токен авторизации: {self.auth_token}")
                except Exception as e:
                    self.logger.error(f"Ошибка при извлечении токена: {e}")

        self.custom_browser.page.on('response', lambda response: asyncio.create_task(check_response(response)))

    async def login(self, login_url, start_url, bad_url, url_keyword):
        await self.custom_browser.start_browser()
        await self.extract_token_from_response(url_keyword)

        try:
            self.logger.info(f"Переход на страницу входа: {login_url}")
            await self.custom_browser.page.goto(login_url, {'waitUntil': 'networkidle2'})

            self.logger.info("Ввод email и пароля...")
            await self.custom_browser.page.type(f'#{self.email_field_id}', self.email)
            await self.custom_browser.page.type(f'#{self.password_field_id}', self.password)

            await asyncio.sleep(2)  # Небольшая задержка перед отправкой формы
            await self.custom_browser.page.click(f'#{self.submit_button_id}')
            await self.custom_browser.page.waitForNavigation()

            current_url = self.custom_browser.page.url
            if current_url == bad_url:
                self.logger.error("Ошибка входа.")
                return None, None

            self.logger.info(f"Ожидание перехода на {start_url}...")
            await self.custom_browser.page.waitForFunction(f'window.location.href === "{start_url}"', {'timeout': 10000})
            self.logger.success(f"Успешно перешли на {start_url}")
            cookies = await self.custom_browser.page.cookies()
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            if self.auth_token:
                self.logger.info(f"Токен авторизации успешно получен: {self.auth_token}")
            else:
                self.logger.error("Токен авторизации не был получен.")
            return cookies_dict, self.auth_token
        except Exception as e:
            self.logger.error("Произошла ошибка во время процесса входа:", e)
        finally:
            await self.custom_browser.close_browser()



if __name__ == "__main__":
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
    fingerprint_manager = FingerprintManager(browser='safari', os='ios')
    fingerprint = fingerprint_manager.generate_fingerprint()
    print(PROXY)
    print(PROXY_USER)
    print(PROXY_PASS)

    async def main():
        driver = LoginAutomationPyppeteer(email=EMAIL, password=PASSWORD, proxy=PROXY, proxy_username=PROXY_USER, proxy_password=PROXY_PASS, logger=logger, fingerprint=fingerprint)
        cookies, token = await driver.login(login_url=LOGIN_URL, start_url=START_URL, bad_url=BAD_URL, url_keyword=URL_KEYWORD)
        print(cookies, token)

    asyncio.run(main())