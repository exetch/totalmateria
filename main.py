import os

from loguru import logger
from material_data_processor import MaterialDataProcessor
from dotenv import load_dotenv
from loginer import LoginAutomation

load_dotenv()
if __name__ == "__main__":
    MAX_LOGIN_ATTEMPTS = 5
    login_attempts = 0
    successful_login = False
    EMAIL = 'dentconwechsta1972@outlook.com'
    PASSWORD = 'TK6JBWHS'
    LOGIN_URL = 'https://www.totalmateria.com/page.aspx?ID=Login&LN=EN'
    START_URL = 'https://portal.totalmateria.com/en/search/quick'
    logger.add("logs/process_log_{time}.log", rotation="1 week")
    project_root = 'C:\\Users\\ASUS\\PycharmProjects\\totalmateria\\base_directory'
    PROXY = os.getenv('PROXY')
    auto_login = LoginAutomation(EMAIL, PASSWORD, PROXY)
    while login_attempts < MAX_LOGIN_ATTEMPTS and not successful_login:
        try:
            cookies, headers = auto_login.login(LOGIN_URL, START_URL)
            if cookies and headers:
                successful_login = True
                processor = MaterialDataProcessor(PROXY, project_root, cookies, headers, logger)
                success = processor.process_response_files()
                if success is None:
                    successful_login = False
                    login_attempts += 1
        except Exception as e:
            logger.error(f"Произошла ошибка при попытке логина: {e}")
            login_attempts += 1

    if not successful_login:
        logger.error("Не удалось залогиниться после нескольких попыток.")




    processor.process_response_files()