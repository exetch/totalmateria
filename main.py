import os
import time
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from kopeechka import KopeechkaClient
from registration_automat import RegistrationAutomation
from loginer import LoginAutomation
from material_data_processor import MaterialDataProcessor

def write_credentials_to_file(filename, login, password):
    with open(filename, 'a') as file:
        file.write('-------------------------\n')
        file.write(f'{datetime.now()} - Получены учетные данные:\n')
        file.write(f'Логин: {login}\n')
        file.write(f'Пароль: {password}\n')
        file.write('-------------------------\n\n')

if __name__ == "__main__":
    logger.add("logs/process_log_{time}.log", rotation="1 week")
    load_dotenv()

    LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=PL'
    START_URL = 'https://portal.totalmateria.com/pl/search/quick'
    BAD_URL = 'https://www.totalmateria.com/page.aspx?ID=TrialConfirm&LN=PL'
    current_dir = os.getcwd()
    project_root = os.path.join(current_dir, 'base_directory')
    PROXY = os.getenv('PROXY')
    api_token = os.getenv('KOPEECHKA_API')
    site_to_register = 'https://www.totalmateria.com/'
    filename = 'credentials.txt'
    attempts = 0

    while True:
        kopeechka_client = KopeechkaClient(api_token)
        email_response = kopeechka_client.get_email(site_to_register)
        email_id = email_response.get('id')
        email = email_response.get('mail')
        logger.debug(email)
        if email:
            reger = RegistrationAutomation(email, PROXY, logger)
            reger.start_driver()
            success_reg_url = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=PL'
            registration_url = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=PL'
            reger.registration(registration_url, success_reg_url)

            logger.info("Ожидание письма...")
            time.sleep(10)
            message_response = kopeechka_client.get_message(email_id)
            logger.debug(message_response)
            while "WAIT_LINK" in message_response.get('status', '') and attempts < 3:
                logger.info("Письмо не найдено, отправка повторного запроса...")
                time.sleep(10)
                message_response = kopeechka_client.get_message(email_id)
                attempts += 1

            if attempts == 3 and "WAIT_LINK" in message_response.get('status', ''):
                logger.error("Письмо так и не было получено после трех попыток.")
                kopeechka_client.cancel_email(email_id)
                logger.info(f"Почтовый адрес {email} отменен.")
                reger.close_driver()
                break

            # Обработка письма, если оно было получено
            if email in message_response.get('mail_body', ''):
                html_content = message_response.get('mail_body')
                login, password = kopeechka_client.extract_login_password(html_content)
                if login and password:
                    write_credentials_to_file(filename, login, password)
                    logger.success(f'Учетные данные сохранены: {login}')

                    # Запуск процесса логина и получения данных
                    auto_login = LoginAutomation(login, password, PROXY)
                    cookies, headers = auto_login.login(LOGIN_URL, START_URL, BAD_URL)

                    if cookies == 1 and headers == 2:
                        logger.error("Пробный доступ к сайту закончился, нужно регистрировать новый аккаунт.")
                        continue
                    elif cookies is not None and headers is not None:
                        processor = MaterialDataProcessor(PROXY, project_root, cookies, headers, logger)
                        success = processor.process_response_files()
                        if success:
                            logger.info("Обработка данных успешно завершена.")
                        else:
                            logger.error("Ошибка при обработке данных.")
                            break
                else:
                    logger.warning('Логин или пароль не найдены в письме.')
            else:
                logger.error('Письмо с учетными данными не было получено.')

            reger.close_driver()
        else:
            logger.error('Не удалось получить почтовый адрес.')
            break


