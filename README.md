# Предварительные условия

На Google Диске должен быть загружен файл base_directory.rar, содержащий необходимые данные для работы проекта.
В корневой директории totalmateria должен находиться файл .env, содержащий api_key и прокси.
1. Клонируйте репозиторий проекта:
```bash
!git clone https://github.com/exetch/totalmateria.git
```
2. Перейдите в директорию проекта:
```bash
%cd totalmateria
```
3. Установите зависимости из requirements.txt:
```bash
!pip install -r requirements.txt
pip install loguru selenium selenium-wire python-dotenv faker fake-useragent
```
4. Установи unrar для распаковки архивов:
```bash
!apt-get install unrar
```
5. Подключи Google Диск для доступа к файлам проекта:
```bash
from google.colab import drive
drive.mount('/content/drive')
```
6. Распакуй файл base_directory.rar в директорию проекта:
```bash
!unrar x "/content/drive/My Drive/base_directory.rar" "/content/totalmateria/"
```
7. Запускай главный скрипт проекта:
```bash
!python /content/totalmateria/main.py
```
8. Лови баги и исправляй=))