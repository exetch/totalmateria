import os
import time
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from kopeechka import KopeechkaClient
from registration_automat import RegistrationAutomation

if __name__ == "__main__":
    logger.add("logs/process_log_{time}.log", rotation="1 week")
    load_dotenv()

    def write_credentials_to_file(filename, login, password):
        with open(filename, 'a') as file:
            file.write('-------------------------\n')
            file.write(f'{datetime.now()} - Получены учетные данные:\n')
            file.write(f'Логин: {login}\n')
            file.write(f'Пароль: {password}\n')
            file.write('-------------------------\n\n')


    api_token = os.getenv('KOPEECHKA_API')
    site_to_register = 'totalmateria.com'
    filename = 'credentials.txt'

    kopeechka_client = KopeechkaClient(api_token)
    try:
        email_response = kopeechka_client.get_email(site_to_register)
        email = email_response.get('mail')
        PROXY = os.getenv('PROXY')

        if email:
            reger = RegistrationAutomation(email, PROXY, logger)
            reger.start_driver()
            success_reg_url = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=PL'
            registration_url = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=PL'
            reger.registration(registration_url, success_reg_url)

            logger.info("Ожидание письма...")
            time.sleep(10)
            message_response = kopeechka_client.get_message(email_response.get('id'))

            if email not in message_response.get('mail_body', ''):
                logger.info("Письмо не найдено, отправка повторного запроса...")
                time.sleep(10)
                message_response = kopeechka_client.get_message(email_response.get('id'))

            if email in message_response.get('mail_body', ''):
                html_content = message_response.get('mail_body')
                login, password = kopeechka_client.extract_login_password(html_content)
                if login and password:
                    write_credentials_to_file(filename, login, password)
                    kopeechka_client.cancel_email(email_response.get('id'))
                    logger.success(f'Учетные данные сохранены: {login}')
                else:
                    logger.warning('Логин или пароль не найдены в письме.')
            else:
                logger.error('Письмо с учетными данными не было получено.')

            reger.close_driver()
        else:
            logger.error('Не удалось получить почтовый адрес.')
    except Exception as e:
        logger.error(f'Произошла ошибка в процессе регистрации: {e}')
    finally:
        if email_response and email_response.get('id'):
            try:
                cancel_response = kopeechka_client.cancel_email(email_response.get('id'))
                logger.info(f'Почта {email} отменена: {cancel_response}')
            except Exception as e:
                logger.error(f'Произошла ошибка при отмене почты: {e}')

        if 'reger' in locals():
            reger.close_driver()