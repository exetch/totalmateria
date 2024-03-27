import asyncio
import os
from dotenv import load_dotenv
from pyppeteer import errors
from faker import Faker
import random
from loguru import logger


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
    def __init__(self, custom_browser, email, logger):
        self.custom_browser = custom_browser
        self.email = email
        self.logger = logger
        self.user_data = self.generate_user_data()

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
        self.logger.info("Заполняем форму регистрации...")
        page = self.custom_browser.page

        fields = {
            '#ctl10_tb_fname': user_data['Name'],
            '#ctl10_tb_lname': user_data['Surname'],
            '#ctl10_tb_email': self.email,
            '#ctl10_tb_confirm_email': self.email,
            '#ctl10_tb_company': user_data['Company'],
            '#ctl10_tb_city': user_data['City'],
            '#ctl10_tb_zip': user_data['Postcode'],
            '#ctl10_tb_phone': user_data['Phone Number']
        }

        for selector, value in fields.items():
            await page.waitForSelector(selector)
            await page.type(selector, value)
            await asyncio.sleep(1)

        dropdowns = {
            '#ctl10_ddl_profession': str(random.randint(1, 10)),
            '#ctl10_ddl_industry': str(random.randint(1, 10)),
            '#ctl10_ddl_country': str(random.randint(1, 180))
        }
        for selector, value in dropdowns.items():
            await page.waitForSelector(selector)
            await page.select(selector, value)
            await asyncio.sleep(1)

        try:
            await page.waitForSelector(".cookie-popup-accept-cookies", {'timeout': 5000})
            await page.click(".cookie-popup-accept-cookies")
            self.logger.info("Кнопка сохранения cookie нажата")
        except Exception as e:
            self.logger.error(f"Не удалось найти или нажать кнопку согласия на использование куки: {e}")

        checkboxes_selectors = [
            '#ctl10_cblSurveyAnswers_0',
            '#ctl10_cblSurveyAnswers_3',
            '#ctl10_cblSurveyAnswers_1',
            '#ctl10_cblSurveyAnswers_4',
            '#ctl10_cblSurveyAnswers_2'
        ]
        for selector in checkboxes_selectors:
            try:
                await page.waitForSelector(selector, {'timeout': 5000})
                await page.click(selector)
                self.logger.info(f"Чекбокс {selector} выбран.")
                await asyncio.sleep(1)
            except Exception as e:
                self.logger.error(f"Не удалось найти или выбрать чекбокс {selector}. Ошибка: {e}")

    async def check_registration_errors(self):
        page = self.custom_browser.page
        error_selectors = [
            "ctl10_lbl_ErrorTitle",
            "ctl10_lbl_error"
        ]
        errors_found = False
        error_messages = []

        for selector in error_selectors:
            try:
                await page.waitForSelector(f"#{selector}", {'visible': True, 'timeout': 5000})
                actual_error_message = await page.evaluate(f'document.querySelector("#{selector}").innerText')
                error_messages.append(actual_error_message)
                errors_found = True
            except errors.TimeoutError:
                continue

        if errors_found:
            for message in error_messages:
                self.logger.error(f"Ошибка регистрации: {message}")
            return False

        return True

    async def registration(self, registration_url, success_url):
        await self.custom_browser.start_browser()

        try:
            await self.custom_browser.page.goto('https://2ip.ru', timeout=60000)

        except errors.TimeoutError:
            print("Превышено время ожидания загрузки")
        try:
            await self.custom_browser.page.goto(registration_url, timeout=30000)
        except errors.TimeoutError:
            self.logger.error("Превышено время ожидания загрузки страницы.")
        await self.fill_out_form(self.user_data)

        await self.custom_browser.page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
        await asyncio.sleep(2)

        submit_button_selector = '#ctl10_btn_submit'
        await self.custom_browser.page.waitForSelector(submit_button_selector, {'timeout': 5000})
        await self.custom_browser.page.click(submit_button_selector)
        await asyncio.sleep(2)
        self.logger.info(f"Кнопка 'Запросить' нажата.")

        if not await self.check_registration_errors():
            self.logger.eror("Обнаружены ошибки в форме.")
            await self.custom_browser.close_browser()
            return

        try:
            await self.custom_browser.waitForNavigation({
                'timeout': 5000,
                'waitUntil': 'networkidle0'
            })
            current_url = self.custom_browser.url
            if current_url == success_url:
                self.logger.info(f"Регистрация успешно завершена.")
            else:
                self.logger.error("URL после регистрации не соответствует ожидаемому.")
        except Exception as e:
            self.logger.error(f"Произошла ошибка при ожидании завершения регистрации: {e}")

        await self.custom_browser.close_browser()

if __name__ == "__main__":
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")
    success_reg_url = 'https://www.totalmateria.com/page.aspx?id=RegisterConfirmation&LN=RU'
    registration_url = 'https://www.totalmateria.com/page.aspx?ID=Register&LN=RU'
    email = 'example@google.com'
    fingerprint_manager = FingerprintManager(browser='safari', os='ios')
    fingerprint = fingerprint_manager.generate_fingerprint()
    reger = RegistrationAutomationPyppeteer(email, PROXY, PROXY_USER, PROXY_PASS, logger, fingerprint)
    asyncio.get_event_loop().run_until_complete(reger.registration(registration_url, success_reg_url))