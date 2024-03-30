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


    async def login(self, login_url, start_url, bad_url):

        await self.custom_browser.start_browser()
        try:
            self.logger.info(f"Переход на страницу входа: {login_url}")

            await self.custom_browser.page.goto(login_url, {'waitUntil': 'networkidle2'})
            # await self.custom_browser.load_cookies(self.email)
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
                await self.custom_browser.close_browser()
                return None, None
            except Exception as e:
                self.logger.success(f"Почта не забанена! Успех")

            await asyncio.sleep(30)
            try:
                current_url = self.custom_browser.page.url
                if 'portal.totalmateria.com' in current_url:
                    self.logger.success(f"Успешно перешли на {start_url}")
                elif 'TrialConfirm' in current_url:
                    self.logger.error("Ошибка входа, логины кончились.")
                    await self.custom_browser.close_browser()
                    return None, None
            except Exception as e:
                self.logger.error(f"Произошла ошибка при ожидании завершения входа: {e}")

            # Ищем токен авторизации и куки
            access_token = await self.custom_browser.page.evaluate('''() => {
                return localStorage.getItem('access_token');
            }''')
            if access_token:
                self.auth_token = access_token
            else:
                self.logger.error("Access token не найден в LocalStorage.")

            cookies = await self.custom_browser.page.cookies()
            cookies_dict = {}
            for cookie in cookies:
                cookies_dict[cookie['name']] = cookie ['value']


            if self.auth_token:
                self.logger.success(f"Токен авторизации успешно получен!")
                headers_dict = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'ru-RU,ru;q=0.9',
                    'Authorization': f'Bearer {self.auth_token}',
                    'Connection': 'keep-alive',
                    'Referer': 'https://portal.totalmateria.com/ru/search/quick/materials/5048801/mechanical',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'UnitSystem': '0',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'ValueReturnMode': 'ActualAndFormattedValue',
                    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
            else:
                self.logger.error("Токен авторизации не был получен.")
            await self.custom_browser.close_browser()
            return cookies_dict, headers_dict
        except Exception as e:
            self.logger.error(f"Произошла ошибка во время процесса входа: {e}")

        await self.custom_browser.close_browser()

