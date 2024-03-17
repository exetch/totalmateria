import string
from datetime import datetime
import requests
import random
import logging
import logging.config
import time
import re
import register_config

proxy_url = "http://cc5e904f65:61489d52c5@88.87.84.141:40778"
def generate_username(length=10):
    """ Генерирует случайное имя пользователя заданной длины. """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def extract_login_password(html_content):
    """
        Извлекает логин и пароль из предоставленного HTML-контента.

        Функция ищет в HTML-контенте логин и пароль, используя регулярные выражения.
        Логин и пароль должны быть заключены в теги <b> и следовать после определённых фраз.

        Args:
            html_content (str): Строка HTML-контента, из которой необходимо извлечь логин и пароль.

        Returns:
            tuple: Возвращает кортеж из двух элементов (логин, пароль). Если логин или пароль не найдены, возвращает (None, None).
    """
    login_pattern = r'Twój login to: <b>([^<]+)</b>'
    password_pattern = r'Hasło: <b>([^<]+)</b>'

    login_match = re.search(login_pattern, html_content)
    password_match = re.search(password_pattern, html_content)

    if login_match and password_match:
        return login_match.group(1), password_match.group(1)
    else:
        return None, None

def check_mail(mail=''):
    """
    Проверяет почтовый ящик на наличие новых сообщений.

    Аргументы:
        mail (str): Электронный адрес для проверки. Формат: 'login@domain.com'.

    Возвращает:
        bool: Возвращает True, если найдены новые сообщения, иначе False.

    Исключения:
        ValueError: Если указанный адрес электронной почты не соответствует формату 'login@domain'.
        ConnectionError: Если возникли проблемы с подключением к сети или серверу.
    """
    try:
        login, domain = mail.split('@')
    except ValueError:
        logging.warning("Invalid email format. It should be 'login@domain'.")
        raise ValueError("Invalid email format. It should be 'login@domain'.")

    check_url = f'{register_config.API}?action=getMessages&login={login}&domain={domain}'

    try:
        response = requests.get(check_url).json()
    except requests.ConnectionError:
        logging.warning("Connection error occurred.")
        raise ConnectionError("Connection error occurred.")

    if not response:
        logging.info("No new messages. Automatic check in 5 seconds.")
        return False
    else:
        for message in response:
            if 'id' in message:
                read_message_url = f'{register_config.API}?action=readMessage&login={login}&domain={domain}&id={message["id"]}'
                message_response = requests.get(read_message_url).json()
                html_content = message_response.get('htmlBody')

                login, password = extract_login_password(html_content)
                if login and password:
                    logging.info(f'Found login: {login}, password: {password}')
                    with open('credentials.txt', 'a') as file:
                        file.write('-------------------------\n')
                        file.write(f'{datetime.now()} - Найдены учетные данные:\n')
                        file.write(f'Логин: {login}\n')
                        file.write(f'Пароль: {password}\n')
                        file.write('-------------------------\n\n')
                    return True
    return False

def register_and_access_platform(email):
    """
        Регистрирует пользователя на платформе Total Materia, используя предоставленный электронный адрес..

        Аргументы:
            email (str): Электронный адрес для регистрации на платформе.

        Возвращает:
            None: Функция не возвращает значения, но логирует процесс регистрации.

        Исключения:
            HTTPError: Ошибка HTTP-запроса.
            ConnectionError: Ошибка подключения.
            Timeout: Ошибка тайм-аута.
            RequestException: Другие ошибки, связанные с HTTP-запросом.
    """
    try:
        session = requests.Session()
        headers = register_config.headers
        params = register_config.params
        data = register_config.data
        data['ctl10$tb_email'] = email
        data['ctl10$tb_confirm_email'] = email
        proxies = {"http": proxy_url}

        response = session.post('https://www.totalmateria.com/page.aspx', params=params, headers=headers, data=data, proxies=proxies)
        response.raise_for_status()

        if response.status_code == 200 and register_config.succesfull_registration_response in response.text:
            logging.info(f"Successful registration for email {email}")
        else:
            logging.warning(f"Unexpected response status: {response.status_code}, Body: {response.text}")

    except requests.exceptions.HTTPError as errh:
        logging.error(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"OOps: Something Else: {err}")



def registriation():
    """
    Осуществляет регистрацию пользователя на платформе, используя сгенерированный почтовый адрес.
    После регистрации осуществляет проверку почты на наличие новых сообщений.

    При успешной регистрации и обнаружении нового сообщения в почтовом ящике, функция завершает свою работу.
    Время выполнения регистрации логируется.

    Возвращает:
        None: Функция не возвращает значения, но логирует процесс регистрации и время выполнения.
    """
    start_time = time.time()

    domain = random.choice(register_config.domain_list)
    username = generate_username()
    email = f'{username}@{domain}'
    logging.info(f'Ваш почтовый адрес: {email}')

    register_and_access_platform(email)
    time.sleep(2)

    while True:
        found = check_mail(mail=email)
        if found:
            break
        time.sleep(5)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Время выполнения регистрации: {elapsed_time} секунд")

if __name__ == "__main__":
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger(__name__)
    registriation()