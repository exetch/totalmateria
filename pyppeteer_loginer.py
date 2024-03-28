import asyncio
import json


class LoginAutomationPyppeteer:
    def __init__(self, custom_browser, email, password, logger):
        self.custom_browser = custom_browser
        self.email = email
        self.password = password
        self.logger = logger
        self.auth_token = None
        self.email_field_id = "orderForm_tb_email"
        self.password_field_id = "orderForm_tb_password"
        self.submit_button_id = "orderForm_btn_login_KTM"


    async def login(self, login_url, start_url, bad_url, url_keyword):

        await self.custom_browser.start_browser()
        try:
            self.logger.info(f"Переход на страницу входа: {login_url}")

            await self.custom_browser.page.goto(login_url, {'waitUntil': 'networkidle2'})
            await self.custom_browser.load_cookies(self.email)
            self.logger.info("Ввод email и пароля...")
            await self.custom_browser.page.type(f'#{self.email_field_id}', self.email)
            await self.custom_browser.page.type(f'#{self.password_field_id}', self.password)

            await asyncio.sleep(2)
            await self.custom_browser.page.click(f'#{self.submit_button_id}')

            # Проверка не появилось ли сообщение о блокировке почты, или еще какая хуйня
            try:
                await self.custom_browser.page.waitForSelector('#orderForm_Message',
                                                                             {'timeout': 2000, 'visible': True})
                error_message = await self.custom_browser.page.evaluate(
                    '''() => document.querySelector('#orderForm_Message').innerText'''
                )
                self.logger.error(f"Обнаружена ошибка при регистрации: {error_message}")
                return None, None
            except Exception as e:
                self.logger.error(f"Произошла ошибка при ожидании входа: {e}")

            # Пытаемся залогиниться
            try:
                await self.custom_browser.page.waitForNavigation({'timeout': 25000, 'waitUntil': 'networkidle0'})
                current_url = self.custom_browser.page.url
                if current_url == start_url or current_url == 'https://portal.totalmateria.com/ru/search/quick':
                    self.logger.success(f"Успешно перешли на {start_url}")
                elif current_url == bad_url:
                    self.logger.error("Ошибка входа, перенаправлено на bad_url.")
                    return None, None
                else:
                    self.logger.warning(f"Переход на неизвестный URL: {current_url}")
            except Exception as e:
                self.logger.error(f"Произошла ошибка при ожидании входа: {e}")
            await asyncio.sleep(20)

            # Ищем токен авторизации и куки
            access_token = await self.custom_browser.page.evaluate('''() => {
                return localStorage.getItem('access_token');
            }''')
            if access_token:
                self.auth_token = access_token
            else:
                self.logger.error("Access token не найден в LocalStorage.")

            cookies = await self.custom_browser.page.cookies()
            cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

            if self.auth_token:
                self.logger.info(f"Токен авторизации успешно получен: {self.auth_token}")
            else:
                self.logger.error("Токен авторизации не был получен.")
            return cookies_dict, self.auth_token
        except Exception as e:
            self.logger.error(f"Произошла ошибка во время процесса входа: {e}")



