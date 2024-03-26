import asyncio
import os
import time

from dotenv import load_dotenv
from pyppeteer import launch, errors
from browserforge.fingerprints import FingerprintGenerator
from browserforge.injectors.pyppeteer import NewPage
from faker import Faker
import random


russian_names = {
    "male": [
        "Александр", "Дмитрий", "Максим", "Сергей", "Андрей",
        "Алексей", "Артем", "Илья", "Кирилл", "Михаил",
        "Никита", "Матвей", "Роман", "Егор", "Арсений",
        "Иван", "Денис", "Евгений", "Даниил", "Тимофей"
    ],
    "female": [
        "Анна", "Мария", "Елена", "Дарья", "Алина",
        "Ирина", "Екатерина", "Наталья", "Марина", "Виктория",
        "Светлана", "Ольга", "Юлия", "Татьяна", "Анастасия",
        "Ксения", "Елизавета", "Александра", "Валерия", "Полина"
    ]
}

cities_base_postcodes = {
    "Москва": "101",
    "Санкт-Петербург": "190",
    "Новосибирск": "630",
    "Екатеринбург": "620",
    "Казань": "420",
    "Нижний Новгород": "603",
    "Челябинск": "454",
    "Самара": "443",
    "Омск": "644",
    "Ростов-на-Дону": "344",
    "Уфа": "450",
    "Красноярск": "660",
    "Воронеж": "394",
    "Пермь": "614",
    "Волгоград": "400",
    "Краснодар": "350",
    "Саратов": "410",
    "Тюмень": "625",
    "Тольятти": "445",
    "Ижевск": "426",
}

load_dotenv()
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')
PROXY = PROXY_HOST + ':' + PROXY_PORT

class RegistrationAutomationPyppeteer:
    def __init__(self, email, proxy, username, password):
        self.email = email
        self.proxy = proxy
        self.username = username
        self.password = password
        self.browser = None
        self.page = None
        self.user_data = self.generate_user_data()

    async def start_browser(self):
        executable_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        args = [
            f'--proxy-server={self.proxy}',
        ]

        self.browser = await launch({
            'headless': False,
            'args': args,
            'executablePath': executable_path,
            'ignoreDefaultArgs': ["--enable-automation"],
            'userDataDir': "./user_data",
            # 'defaultViewport': None,
            # 'devtools': True,
            # 'ignoreHTTPSErrors': True,

        })

        fingerprint_generator = FingerprintGenerator()
        fingerprint = fingerprint_generator.generate()

        self.page = await NewPage(self.browser, fingerprint=fingerprint)

        # Аутентификация на прокси-сервере
        await self.page.authenticate({'username': self.username, 'password': self.password})

    async def close_browser(self):
        await self.page.close()
        await self.browser.close()

    def generate_user_data(self):
        fake = Faker('ru_RU')
        gender = random.choice(["male", "female"])
        name = random.choice(russian_names[gender])
        surname = fake.last_name_male() if gender == "male" else fake.last_name_female()
        city, base_postcode = random.choice(list(cities_base_postcodes.items()))
        full_postcode = f"{base_postcode}{random.randint(100, 999)}"
        return {
            "Name": name,
            "Surname": surname,
            "Company": fake.company(),
            "City": city,
            "Postcode": full_postcode,
            "Phone Number": fake.bothify(text='+7 (9##) ###-####'),
        }

    async def fill_out_form(self, user_data):
        await self.page.waitForSelector('#ctl10_tb_fname')
        await self.page.type('#ctl10_tb_fname', user_data['Name'])
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_lname')
        await self.page.type('#ctl10_tb_lname', user_data['Surname'])
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_email')
        await self.page.type('#ctl10_tb_email', self.email)
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_confirm_email')
        await self.page.type('#ctl10_tb_confirm_email', self.email)
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_company')
        await self.page.type('#ctl10_tb_company', user_data['Company'])
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_city')
        await self.page.type('#ctl10_tb_city', user_data['City'])
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_zip')
        await self.page.type('#ctl10_tb_zip', user_data['Postcode'])
        time.sleep(2)
        await self.page.waitForSelector('#ctl10_tb_phone')
        await self.page.type('#ctl10_tb_phone', user_data['Phone Number'])
        time.sleep(2)
        random_profession_value = str(random.randint(1, 10))
        await self.page.waitForSelector('#ctl10_ddl_profession')
        await self.page.select('#ctl10_ddl_profession', random_profession_value)
        time.sleep(2)
        random_industry_value = str(random.randint(1, 10))
        await self.page.waitForSelector('#ctl10_ddl_industry')
        await self.page.select('#ctl10_ddl_industry', random_industry_value)
        time.sleep(2)
        random_country_value = str(random.randint(1, 180))
        await self.page.waitForSelector('#ctl10_ddl_country')
        await self.page.select('#ctl10_ddl_country', random_country_value)
        time.sleep(2)
        try:
            await self.page.waitForSelector(".cookie-popup-accept-cookies", {'timeout': 5000})
            await self.page.click(".cookie-popup-accept-cookies")
            print("Кнопка согласия куки нажата.")
        except Exception as e:
            print(f"Не удалось найти или нажать кнопку согласия на использование куки: {e}")

            # Выбор чекбоксов
        checkboxes_selectors = [
            '#ctl10_cblSurveyAnswers_0',
            '#ctl10_cblSurveyAnswers_3',
            '#ctl10_cblSurveyAnswers_1',
            '#ctl10_cblSurveyAnswers_4',
            '#ctl10_cblSurveyAnswers_2'
        ]
        for selector in checkboxes_selectors:
            try:
                await self.page.waitForSelector(selector, {'timeout': 5000})
                await self.page.click(selector)
                print(f"Чекбокс {selector} выбран.")
                time.sleep(1)
            except Exception as e:
                print(f"Не удалось найти или выбрать чекбокс {selector}. Ошибка: {e}")

    async def registration(self, login_url, success_url):
        await self.start_browser()

        try:
            await self.page.goto('https://whoer.net/ru', timeout=30000)
            # Ожидаем, когда IP-адрес будет виден на странице, или любой другой уникальный элемент страницы
            await self.page.waitForSelector('.ip', {'timeout': 5000})
            ip_address = await self.page.evaluate('() => document.querySelector(".ip").innerText')
            print(f"Текущий IP-адрес: {ip_address}")
        except errors.TimeoutError:
            print("Превышено время ожидания загрузки страницы 2ip.ru.")
            # Здесь можно решить, стоит ли продолжать выполнение скрипта
        except Exception as e:
            print(f"Произошла ошибка при попытке получить IP-адрес: {e}")
        try:
            await self.page.goto(login_url, timeout=30000)
        except errors.TimeoutError:
            print("Превышено время ожидания загрузки страницы.")
        await self.fill_out_form(self.user_data)

        # Прокрутка страницы вниз до конца перед нажатием на кнопку
        await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        await asyncio.sleep(2)

        submit_button_selector = '#ctl10_btn_submit'
        await self.page.click(submit_button_selector)

        try:
            await self.page.waitForNavigation({
                'timeout': 20,
                'waitUntil': 'networkidle0'
            })
            current_url = self.page.url
            if current_url == success_url:
                print("Регистрация успешно завершилась!")
            else:
                print("URL после регистрации не соответствует ожидаемому.")
        except Exception as e:
            print(f"Произошла ошибка при ожидании завершения регистрации: {e}")

        await asyncio.sleep(60)  # Время для демонстрации перед закрытием
        await self.close_browser()

if __name__ == "__main__":


    success_reg_url = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=PL'
    registration_url = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=PL'
    email = 'baronebmfd4@gmail.com'
    print(PROXY)
    print()
    registration = RegistrationAutomationPyppeteer(email, PROXY, PROXY_USER, PROXY_PASS)
    asyncio.get_event_loop().run_until_complete(registration.registration(registration_url, success_reg_url))