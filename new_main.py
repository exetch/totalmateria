import asyncio
import os
import time
from datetime import datetime
import requests
from kopeechka import KopeechkaClient
from loguru import logger
from custom_browser import CustomBrowser, FingerprintManager
from material_data_processor import MaterialDataProcessor
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
PROXY_FOR_REQUSTS = 'http://' + PROXY_USER + ':' + PROXY_PASS + '@' + PROXY_SETTINGS
MAX_LOGIN_ATTEMPTS = 5


REGISTRATION_URL = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=RU'
SUCCESS_URL = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=RU'
LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=RU'
START_URL = 'https://portal.totalmateria.com/'
BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=RU'
CHANGE_IP_URL = 'https://changeip.mobileproxy.space/?proxy_key=c60aea12d2bd5902c95813a98273a37d&format=json'
api_token = os.getenv('KOPEECHKA_API')
kopeechka_client = KopeechkaClient(api_token)
site_to_register = 'https://www.totalmateria.com/'
filename = 'credentials.txt'
current_dir = os.getcwd()
project_root = os.path.join(current_dir, 'base_directory')

def write_credentials_to_file(filename, login, password):
    with open(filename, 'a') as file:
        file.write('-------------------------\n')
        file.write(f'{datetime.now()} - Получены учетные данные:\n')
        file.write(f'Логин: {login}\n')
        file.write(f'Пароль: {password}\n')
        file.write('-------------------------\n\n')

async def main():
    fingerprint_manager = FingerprintManager(browser='safari', os='ios')
    all_materials_processed = False
    while not all_materials_processed:

        fingerprint = fingerprint_manager.generate_fingerprint()
        custom_browser = CustomBrowser(PROXY_SETTINGS, PROXY_USER, PROXY_PASS, fingerprint, logger)
        kopeechka_client = KopeechkaClient(api_token)
        while True:
            response = requests.get(CHANGE_IP_URL)
            if response.json().get('status') == 'OK':
                break
        new_ip = response.json().get('new_ip')
        logger.info(f'IP успешно изменен: {new_ip}')
        while True:
            email_response = kopeechka_client.get_email(site_to_register)
            if email_response.get('status') == 'OK':
                break
        email_id = email_response.get('id')
        email = email_response.get('mail')
        if email:
            await custom_browser.load_cookies(email)
            registration_automation = RegistrationAutomationPyppeteer(custom_browser, email, logger)
            await registration_automation.registration(REGISTRATION_URL, SUCCESS_URL)
            logger.info("Ожидание письма...")
            time.sleep(10)
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

                login_attempts = 1
                while login_attempts < MAX_LOGIN_ATTEMPTS:
                    login_automation = LoginAutomationPyppeteer(custom_browser, login, password, logger)
                    cookies_dict, headers = await login_automation.login(LOGIN_URL, START_URL, BAD_URL)
                    if cookies_dict is not None and headers is not None:
                        login_attempts += 1
                        processor = MaterialDataProcessor(PROXY_FOR_REQUSTS, project_root, cookies_dict, headers, logger)
                        process_result = processor.process_response_files()
                        logger.info(process_result)

                        if process_result == 401:
                            continue
                        if process_result == 'All materials processed':
                            all_materials_processed = True
                            break  # Если все материалы обработаны, завершить основной цикл
                if not all_materials_processed:
                    logger.info("Все попытки логина исчерпаны. Регистрируем новый аккаунт.")


if __name__ == "__main__":
    asyncio.run(main())