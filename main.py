import os

from loguru import logger
from material_data_processor import MaterialDataProcessor
from utils import cookies, headers
from loginer import LoginAutomation
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":

    logger.add("logs/process_log_{time}.log", rotation="1 week")
    project_root = 'C:\\Users\\ASUS\\PycharmProjects\\totalmateria\\base_directory'
    proxy_url = os.getenv('PROXY')

    processor = MaterialDataProcessor(proxy_url, project_root, cookies, headers, logger)

    processor.process_response_files()