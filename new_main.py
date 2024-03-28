import asyncio
import os
import time
from datetime import datetime

from kopeechka import KopeechkaClient
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

fingerprint_manager = FingerprintManager(browser='safari', os='ios')
fingerprint = fingerprint_manager.generate_fingerprint()

# # Создаем экземпляр CustomBrowser
custom_browser = CustomBrowser(PROXY_SETTINGS, PROXY_USER, PROXY_PASS, fingerprint, logger)

REGISTRATION_URL = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=RU'
SUCCESS_URL = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=RU'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=RU'
START_URL = 'https://portal.totalmateria.com/'
BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=RU'
URL_KEYWORD = 'identity/connect/token'
api_token = os.getenv('KOPEECHKA_API')
kopeechka_client = KopeechkaClient(api_token)
site_to_register = 'https://www.totalmateria.com/'
filename = 'credentials.txt'

def write_credentials_to_file(filename, login, password):
    with open(filename, 'a') as file:
        file.write('-------------------------\n')
        file.write(f'{datetime.now()} - Получены учетные данные:\n')
        file.write(f'Логин: {login}\n')
        file.write(f'Пароль: {password}\n')
        file.write('-------------------------\n\n')

async def main():
    kopeechka_client = KopeechkaClient(api_token)
    email_response = kopeechka_client.get_email(site_to_register)
    email_id = email_response.get('id')
    email = email_response.get('mail')
    if email:
        await custom_browser.load_cookies(email)
        registration_automation = RegistrationAutomationPyppeteer(custom_browser, email, logger)
        await registration_automation.registration(REGISTRATION_URL, SUCCESS_URL)
        logger.info("Ожидание письма...")
        time.sleep(5)
        message_response = kopeechka_client.get_message(email_id)
        attempts = 0
        while "WAIT_LINK" in message_response.get('value', '') and attempts < 3:
            logger.info("Письмо не найдено, отправка повторного запроса...")
            time.sleep(10)
            message_response = kopeechka_client.get_message(email_id)
            attempts += 1

        if attempts == 3 and "WAIT_LINK" in message_response.get('value', ''):
            logger.error("Письмо так и не было получено после трех попыток.")
            kopeechka_client.cancel_email(email_id)
            logger.info(f"Почтовый адрес {email} отменен.")


        # Обработка письма, если оно было получено
        if message_response.get('status', '') == 'OK':
            html_content = message_response.get('fullmessage')
            login, password = kopeechka_client.extract_login_password(html_content)
            if login and password:
                write_credentials_to_file(filename, login, password)
                logger.success(f'Учетные данные сохранены: {login}, {password}')

                login_automation = LoginAutomationPyppeteer(custom_browser, login, password, logger)
                cookies_dict, auth_token = await login_automation.login(LOGIN_URL, START_URL, BAD_URL, URL_KEYWORD)

                # Сохраняем куки сразу после успешного логина, до закрытия браузера
                if cookies_dict:
                    await custom_browser.save_cookies(login)

                await custom_browser.close_browser()

if __name__ == "__main__":
    asyncio.run(main())