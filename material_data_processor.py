import json
import os
import sys
import time
from random import randint
import requests
from loguru import logger

class MaterialDataProcessor:
    def __init__(self, proxy_url, project_root, cookies, headers, logger):
        self.proxy_url = proxy_url
        self.project_root = project_root
        self.cookies = cookies
        self.headers = headers
        self.logger = logger

    @staticmethod
    def get_material_ids(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [material['materialId'] for material in data.get('materials', [])]
        except UnicodeDecodeError as e:
            logger.error(f"Ошибка декодирования Unicode в файле {file_path}: {e}")
            raise

    @staticmethod
    def read_or_create_processed_groups(path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []


    def fetch_and_save_material_properties(self, material_id, properties_dir):
        os.makedirs(properties_dir, exist_ok=True)
        proxies = {"http": self.proxy_url, "https": self.proxy_url}
        urls = {
            'physical': f'https://portal.totalmateria.com/referencedata/ru/materials/{material_id}/physical/syntheticRangeAll',
            'mechanical': f'https://portal.totalmateria.com/referencedata/ru/materials/{material_id}/mechanical/syntheticRangeAll'
        }

        for prop_type, url in urls.items():
            attempt = 0  # Счетчик попыток
            while attempt < 5:
                try:
                    response = requests.get(url, cookies=self.cookies, headers=self.headers, proxies=proxies)
                    response.raise_for_status()

                    if response.status_code == 401:
                        logger.info("Unauthorized access detected. Please re-login with new session cookies and headers.")
                        return False

                    file_path = os.path.join(properties_dir, f'{material_id}_{prop_type}.json')
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(response.json(), file, indent=4, ensure_ascii=False)

                    logger.info(f"Properties for material ID {material_id} ({prop_type}) fetched and saved at: {file_path}")
                    # Случайная задержка между запросами
                    sleep_time = randint(1, 2)
                    logger.debug(f"Waiting for {sleep_time} seconds before the next request...")
                    time.sleep(sleep_time)
                    break

                except requests.exceptions.ProxyError as proxy_err:
                    logger.warning(
                        f"Proxy Error encountered while fetching properties for material ID {material_id}: {proxy_err}. Retrying in 4 seconds...")
                    time.sleep(4)

                except requests.exceptions.SSLError as ssl_err:
                    if attempt == 0:
                        logger.warning(
                            f"SSL Error encountered while fetching properties for material ID {material_id}: {ssl_err}. Retrying in 4 seconds...")
                    time.sleep(4)
                    attempt += 1

                except requests.exceptions.HTTPError as e:
                    logger.error(f"HTTP Error fetching properties for material ID {material_id}: {e}")
                    return False

                if attempt == 5:  # прекращаем выполнение скрипта после 5 попыток
                    logger.error(
                        f"Failed to fetch properties for material ID {material_id} after retrying. Execution stopped.")
                    sys.exit(1)

        return True

    @staticmethod
    def update_processed_materials(path, material_id):
        processed_materials = MaterialDataProcessor.read_or_create_processed_groups(path)
        if material_id not in processed_materials:
            processed_materials.append(material_id)
            with open(path, 'w') as file:
                json.dump(processed_materials, file, indent=4)


    def process_response_files(self):
        for dirpath, dirs, filenames in os.walk(self.project_root):
            for filename in filenames:
                if filename.endswith('_response.json'):
                    file_path = os.path.join(dirpath, filename)
                    material_ids = self.get_material_ids(file_path)
                    processed_materials_path = os.path.join(self.project_root, 'processed_materials.json')
                    processed_materials = self.read_or_create_processed_groups(processed_materials_path)

                    properties_dir = os.path.join(dirpath, 'material_properties')

                    for material_id in material_ids[:10]:  # Ограничиваем количество материалов для обработки до 10
                        if material_id not in processed_materials:
                            success = self.fetch_and_save_material_properties(material_id, properties_dir)
                            if not success:
                                return
                            self.update_processed_materials(processed_materials_path, material_id)

