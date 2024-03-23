import time
from fake_useragent import UserAgent
from selenium.common import TimeoutException
from seleniumwire import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

class RegistrationAutomation:
    def __init__(self, email, proxy, logger):
        self.email = email
        self.driver = None
        self.user_data = self.generate_user_data()
        self.name_field_id = 'ctl10_tb_fname'
        self.surname_field_id = 'ctl10_tb_lname'
        self.email_field_id = 'ctl10_tb_email'
        self.confirm_email_field_id = 'ctl10_tb_confirm_email'
        self.company_field_id = 'ctl10_tb_company'
        self.city_field_id = 'ctl10_tb_city'
        self.zip_field_id = 'ctl10_tb_zip'
        self.phone_filed_if = 'ctl10_tb_phone'
        self.profession_field_id = 'ctl10_ddl_profession'
        self.industry_field_id = 'ctl10_ddl_industry'
        self.country_field_id = 'ctl10_ddl_country'
        self.submit_field_id = 'ctl10_btn_submit'
        self.logger = logger
        self.proxy_options = {
            "proxy": {
                "https": proxy
            }
        }
    def generate_user_data(self):
        fake = Faker('ru_RU')
        gender = random.choice(["male", "female"])
        if gender == "male":
            name = random.choice(russian_names["male"])
            surname = fake.last_name_male()
        else:
            name = random.choice(russian_names["female"])
            surname = fake.last_name_female()
        city, base_postcode = random.choice(list(cities_base_postcodes.items()))
        full_postcode = f"{base_postcode}{random.randint(100, 999)}"
        user = {
            "Name": name,
            "Surname": surname,
            "Company": fake.company(),
            "City": city,
            "Postcode": full_postcode,
            "Phone Number": fake.bothify(text='+7 (9##) ###-####'),
        }
        return user

    def set_profession(self, profession_value=None):
        try:
            profession_select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.profession_field_id))
            )

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, self.profession_field_id))
            )
            profession_dropdown = Select(profession_select_element)
            if profession_value is not None:
                profession_dropdown.select_by_value(profession_value)
            else:
                options = [option.get_attribute("value") for option in profession_dropdown.options if
                           option.get_attribute("value").strip()]
                if not options:
                    self.logger.error("Список профессий пуст.")
                    return
                random_value = random.choice(options[1:])
                profession_dropdown.select_by_value(random_value)
        except Exception as e:
            self.logger.error(f"Ошибка при установке профессии: {e}")

    def set_random_industry(self):
        try:
            self.logger.info("Ожидание элемента селектора индустрии...")
            industry_select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.industry_field_id))
            )
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, self.industry_field_id)))
            industry_select = Select(industry_select_element)
            options = [option for option in industry_select.options if option.get_attribute("value") != "0"]
            if not options:
                self.logger.error("Список индустрий пуст.")
                return
            random_choice = random.choice(options)
            industry_select.select_by_value(random_choice.get_attribute("value"))
            self.logger.success("Успешно установлена индустрия.")
        except Exception as e:
            self.logger.error(f"Ошибка при установке индустрии: {e}")

    def set_random_country(self):
        try:
            self.logger.info("Ожидание элемента селектора страны...")
            country_select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.country_field_id))
            )
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, self.country_field_id)))
            country_select = Select(country_select_element)
            country_options = [option.get_attribute("value") for option in country_select.options if
                               option.get_attribute("value").strip()]
            if not country_options:
                self.logger.error("Список стран пуст.")
                return
            random_value = random.choice(country_options[1:])
            country_select.select_by_value(random_value)
            self.logger.success("Успешно установлена страна.")
        except Exception as e:
            self.logger.error(f"Ошибка при установке страны: {e}")

    def select_checkboxes_except_other(self):
        try:
            accept_cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cookie-popup-accept-cookies"))
            )
            accept_cookies_button.click()
            self.logger.info("Кнопка согласия куки нажата.")
        except Exception as e:
            self.logger.warning(f"Не удалось найти или нажать кнопку согласия на использование куки: {e}")
        try:
            checkboxes_ids = [
                'ctl10_cblSurveyAnswers_0',
                'ctl10_cblSurveyAnswers_3',
                'ctl10_cblSurveyAnswers_1',
                'ctl10_cblSurveyAnswers_4',
                'ctl10_cblSurveyAnswers_2'
            ]
            for checkbox_id in checkboxes_ids:
                try:
                    checkbox_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, checkbox_id))
                    )
                    if not checkbox_element.is_selected():
                        checkbox_element.click()
                except Exception as e:
                    self.logger.error(f"Не удалось найти или выбрать чекбокс с ID: {checkbox_id}. Ошибка: {e}")
            self.logger.success("Все необходимые чекбоксы выбраны.")
        except Exception as e:
            self.logger.error(f"Ошибка при выборе чекбоксов: {e}")

    def fill_out_form(self, user_data):
        # Заполнение текстовых полей
        self.driver.find_element(By.ID, self.name_field_id).send_keys(user_data['Name'])
        self.driver.find_element(By.ID, self.surname_field_id).send_keys(user_data['Surname'])
        self.driver.find_element(By.ID, self.email_field_id).send_keys(self.email)
        self.driver.find_element(By.ID, self.confirm_email_field_id).send_keys(self.email)
        self.driver.find_element(By.ID, self.company_field_id).send_keys(user_data['Company'])
        self.driver.find_element(By.ID, self.city_field_id).send_keys(user_data['City'])
        self.driver.find_element(By.ID, self.zip_field_id).send_keys(user_data['Postcode'])
        self.driver.find_element(By.ID, self.phone_filed_if).send_keys(user_data['Phone Number'])
        self.set_profession()
        self.set_random_industry()
        self.set_random_country()
        self.select_checkboxes_except_other()


    def start_driver(self):
        """Инициализирует драйвер."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=self.proxy_options)

    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.logger.info("Драйвер успешно закрыт.")

    def registration(self, login_url, success_url):
        """Процесс регистрации."""
        try:
            self.logger.info("Запуск драйвера...")
            self.start_driver()
            self.driver.get(login_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, self.email_field_id))
            )
            self.logger.info("Заполнение полей формы регистрации...")
            self.fill_out_form(self.user_data)
            time.sleep(0.5)
            self.driver.find_element(By.ID, self.submit_field_id).click()
            WebDriverWait(self.driver, 20).until(
                lambda driver: driver.current_url == success_url
            )
            self.logger.success("Регистрация успешно завершилась!")
        except TimeoutException:
            self.logger.info("Превышено время ожидания входа на страницу")
        finally:
            self.close_driver()