import asyncio
import os

from loguru import logger
from custom_browser import CustomBrowser, FingerprintManager
from pyppeteer_loginer import LoginAutomationPyppeteer
from pyppeteer_registration import RegistrationAutomationPyppeteer
from dotenv import load_dotenv

load_dotenv()
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PROXY_SETTINGS = PROXY_HOST + ':' + PROXY_PORT
CHROME_EXECUTABLE_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
EMAIL = "ViCassiday@post.com"
USERNAME = "testuser"
PASSWORD = "testpassword"

fingerprint_manager = FingerprintManager(browser='safari', os='ios')
fingerprint = fingerprint_manager.generate_fingerprint()

# Создаем экземпляр CustomBrowser
custom_browser = CustomBrowser(PROXY_SETTINGS, PROXY_USER, PROXY_PASS, fingerprint, logger)

# URL для регистрации и URL успеха (для проверки успешной регистрации)
REGISTRATION_URL = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=RU'
SUCCESS_URL = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=RU'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=RU'
START_URL = 'https://portal.totalmateria.com/ru/search/quick'
BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=RU'
URL_KEYWORD = 'identity/connect/token'


async def main():
    # Попытка загрузить существующие куки
    await custom_browser.load_cookies("cookies.json")

    # Регистрация (если требуется)
    # registration_automation = RegistrationAutomationPyppeteer(custom_browser, EMAIL, logger)
    # await registration_automation.registration(REGISTRATION_URL, SUCCESS_URL)

    # Логин
    login_automation = LoginAutomationPyppeteer(custom_browser, EMAIL, PASSWORD, logger)
    await login_automation.login(LOGIN_URL, START_URL, BAD_URL, 'identity/connect/token')

    # Сохраняем куки после успешного входа
    await custom_browser.save_cookies("cookies.json")

    await custom_browser.close_browser()

if __name__ == "__main__":
    asyncio.run(main())