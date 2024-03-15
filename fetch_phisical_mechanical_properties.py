import json
import os
import requests
from loguru import logger
from utils import cookies, headers

logger.add("process_log_{time}.log", rotation="1 week")


def get_material_ids(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [material['materialId'] for material in data.get('materials', [])]

# Функция для чтения или создания processed_groups.json
def read_or_create_processed_groups(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def fetch_and_save_material_properties(material_id, properties_dir, cookies, headers):
    os.makedirs(properties_dir, exist_ok=True)

    urls = {
        'physical': f'https://portal.totalmateria.com/referencedata/ru/materials/{material_id}/physical/syntheticRangeAll',
        'mechanical': f'https://portal.totalmateria.com/referencedata/ru/materials/{material_id}/mechanical/syntheticRangeAll'
    }

    for prop_type, url in urls.items():
        try:
            response = requests.get(url, cookies=cookies, headers=headers)
            response.raise_for_status()

            if response.status_code == 401:
                logger.info("Unauthorized access detected. Please re-login with new session cookies and headers.")
                return False

            file_path = os.path.join(properties_dir, f'{material_id}_{prop_type}.json')
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)

            logger.info(f"Properties for material ID {material_id} ({prop_type}) fetched and saved at: {file_path}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error fetching properties for material ID {material_id}: {e}")
            return False
    return True



def update_processed_materials(path, material_id):
    processed_materials = read_or_create_processed_groups(path)
    if material_id not in processed_materials:
        processed_materials.append(material_id)
        with open(path, 'w') as file:
            json.dump(processed_materials, file, indent=4)


def process_response_files(root, cookies, headers):
    for dirpath, dirs, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('_response.json'):
                file_path = os.path.join(dirpath, filename)
                material_ids = get_material_ids(file_path)
                processed_materials_path = os.path.join(root, 'processed_materials.json')
                processed_materials = read_or_create_processed_groups(processed_materials_path)

                # Создаем директорию внутри текущей папки для свойств материалов
                properties_dir = os.path.join(dirpath, 'material_properties')

                for material_id in material_ids[:10]:  # Ограничиваем количество материалов для обработки до 10
                    if material_id not in processed_materials:
                        success = fetch_and_save_material_properties(material_id, properties_dir, cookies, headers)
                        if not success:
                            return
                        update_processed_materials(processed_materials_path, material_id)


if __name__ == "__main__":
    project_root = 'C:\\Users\\ASUS\\PycharmProjects\\totalmateria\\base_directory'
    process_response_files(project_root, cookies, headers)
