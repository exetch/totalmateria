import os
import json
from loguru import logger


# Функция убирающая недопустимые символы
def sanitize_filename(filename):

    for char in r'\<>:"/|?*':
        filename = filename.replace(char, '')

    if len(filename) > 255:
        filename = filename[:255]

    return filename


# Функция для создания и записи в файл свойств
def write_properties_to_file(group_name, property_names, root):
    # Создаем имя файла, очищая его от недопустимых символов

    clean_group_name = sanitize_filename(group_name)

    properties_file_name = f"свойства в группе {clean_group_name}.txt"

    properties_file_path = os.path.join(root, properties_file_name)

    try:

        with open(properties_file_path, 'w', encoding='utf-8') as file:

            for property_name in property_names:
                file.write(f"{property_name}\n")

        logger.info(f"Properties for the group '{group_name}' have been written to {properties_file_path}")

    except Exception as e:

        logger.exception(f"Failed to write properties to file: {e}")


# Функция для сбора свойств из JSON файлов
def collect_properties_from_json(files):
    property_names = set()

    for file_name in files:

        try:

            with open(file_name, 'r', encoding='utf-8') as file:

                data = json.load(file)

                synthetic_data = data.get('syntheticData', [])

                for item in synthetic_data:

                    property_name = item.get('propertyName')

                    if property_name:
                        property_names.add(property_name)

            logger.info(f"Collected properties from {file_name}")

        except Exception as e:

            logger.exception(f"Failed to collect properties from {file_name}: {e}")

    return property_names


def process_directories(root):
    for subdir, dirs, files in os.walk(root):


        if 'material_properties' in dirs:
            material_properties_path = os.path.join(subdir, 'material_properties')

            json_files = [f for f in os.listdir(material_properties_path) if f.endswith('.json')]

            json_files = [os.path.join(material_properties_path, f) for f in json_files]

            properties = collect_properties_from_json(json_files)

            write_properties_to_file(os.path.basename(subdir), properties, subdir)




def delete_txt_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                os.remove(os.path.join(root, file))
                print(f"Deleted: {os.path.join(root, file)}")

def combine_properties(root):
    combined_properties = {}
    for subdir, dirs, files in os.walk(root, topdown=False):
        properties_set = set()

        for file in files:
            if file.endswith('.txt') and file != 'properties_combined.txt':
                with open(os.path.join(subdir, file), 'r', encoding='utf-8') as f:
                    properties_set.update(line.strip() for line in f if line.strip())

        if dirs:
            for d in dirs:
                dirpath = os.path.join(subdir, d)
                if dirpath in combined_properties:
                    properties_set.update(combined_properties[dirpath])

            combined_properties[subdir] = properties_set

    for path, props in combined_properties.items():
        properties_file = os.path.join(path, 'properties_combined.txt')
        with open(properties_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(props)))
        logger.info(f"Combined properties written to: {properties_file}")

if __name__ == "__main__":
    project_root = 'C:\\Users\\ASUS\\PycharmProjects\\totalmateria\\base_directory'  # Замени на свой путь к проекту

    logger.add("process_log_{time}.log", rotation="1 week")
    delete_txt_files(project_root)
    process_directories(project_root)
    combine_properties(project_root)


