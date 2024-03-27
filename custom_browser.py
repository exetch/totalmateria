import asyncio
import json
import os
from browserforge.fingerprints import FingerprintGenerator
from pyppeteer import launch
from browserforge.injectors.pyppeteer import NewPage

class FingerprintManager:
    def __init__(self, browser='safari', os='ios'):
        self.browser = browser
        self.os = os

    def generate_fingerprint(self):
        fingerprint_generator = FingerprintGenerator()
        return fingerprint_generator.generate(browser=self.browser, os=self.os)

    def save_fingerprint(self, email, fingerprint):
        directory = "browser_fingerprints"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, f"{email}.json")
        with open(filepath, 'w') as file:
            json.dump(fingerprint, file)
        print(f"Fingerprint сохранен в {filepath}.")

class CustomBrowser:
    def __init__(self, proxy_settings, proxy_username, proxy_password, fingerprint, logger):
        self.proxy_settings = proxy_settings
        self.fingerprint = fingerprint
        self.logger = logger
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.browser = None
        self.page = None

    async def start_browser(self):
        self.browser = await launch({
            'headless': False,
            'args': [f"--proxy-server={self.proxy_settings}"],
            'executablePath': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'ignoreDefaultArgs': ["--enable-automation"],
            'userDataDir': "./user_data",
        })
        self.page = await NewPage(self.browser, fingerprint=self.fingerprint)

        # Аутентификация на прокси-сервере
        await self.page.authenticate({'username': self.proxy_username, 'password': self.proxy_password})
        self.logger.info("Аутентификация пройдена")

    async def save_cookies(self, path="cookies.json"):
        try:
            cookies = await self.page.cookies()
            with open(path, "w") as file:
                json.dump(cookies, file)
            self.logger.info("Куки сохранены в файл.")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении куки: {str(e)}")

    async def load_cookies(self, path="cookies.json"):
        if os.path.exists(path):
            try:
                with open(path, "r") as file:
                    cookies = json.load(file)
                for cookie in cookies:
                    await self.page.setCookie(cookie)
                self.logger.info("Куки загружены из файла и установлены в браузер.")
            except Exception as e:
                self.logger.error(f"Ошибка при загрузке куки: {str(e)}")
        else:
            self.logger.info("Файл куки не найден.")

