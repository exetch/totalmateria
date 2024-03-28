import asyncio
import json
import os
from browserforge.fingerprints import FingerprintGenerator
from browserforge.fingerprints import Fingerprint
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
            fingerprint_dict = {
            'headers': fingerprint.headers,
            'slim': fingerprint.slim,
            'fonts': fingerprint.fonts,
            'screen': str(fingerprint.screen),
            'battery': fingerprint.battery,
            'audioCodecs': fingerprint.audioCodecs,
            'mockWebRTC': fingerprint.mockWebRTC,
            'multimediaDevices': fingerprint.multimediaDevices,
            'navigator': str(fingerprint.navigator),
            'pluginsData': fingerprint.pluginsData,
            'videoCard': str(fingerprint.videoCard),
            'videoCodecs': fingerprint.videoCodecs,
        }
            json.dump(fingerprint_dict, file)
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

    async def close_browser(self):
        await self.page.close()
        await self.browser.close()
        self.logger.info("Браузер закрыт")

    async def save_cookies(self, email):
        directory = "cookies"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{email}.json"
        filepath = os.path.join(directory, filename)

        try:
            cookies = await self.page.cookies()
            with open(filepath, "w") as file:
                json.dump(cookies, file)
            self.logger.info(f"Куки сохранены в файл {filepath}.")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении куки для {email}: {str(e)}")

    async def load_cookies(self, email):
        directory = "cookies"
        filename = f"{email}.json"
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as file:
                    cookies = json.load(file)
                    # Преобразуем каждый куки в формат, принимаемый Pyppeteer
                    for cookie in cookies:
                        await self.page.setCookie(**cookie)
                self.logger.info(f"Куки загружены из файла {filepath} и установлены в браузер.")
            except Exception as e:
                self.logger.error(f"Ошибка при загрузке куки для {email}: {str(e)}")
        else:
            self.logger.info(f"Файл куки для {email} не найден.")

