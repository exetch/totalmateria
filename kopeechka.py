import os
import re
import random
import requests
from  dotenv import load_dotenv



class KopeechkaClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = 'https://api.kopeechka.store'
        self.email_domains = [
            "hotmail.com", "outlook.com", "outlook.fr", "outlook.es", "outlook.de",
            "outlook.it", "outlook.be", "outlook.pt", "outlook.ie", "outlook.jp",
            "outlook.co.id", "outlook.dk", "outlook.cl", "outlook.at", "outlook.com.au",
            "outlook.in", "outlook.com.br", "outlook.cz", "outlook.sg", "outlook.com.ar",
            "outlook.co.th", "outlook.sk", "outlook.com.gr", "outlook.kr", "outlook.co.il",
            "outlook.lv", "outlook.hu", "outlook.ph", "outlook.com.tr", "outlook.com.vn",
            "outlook.my", "mail.com", "email.com", "usa.com", "gmx.com",
            "caramail.com", "gmx.fr", "caramail.fr", "mail.ru", "bk.ru",
            "inbox.ru", "list.ru"
        ]

    def get_balance(self):
        url = f'{self.base_url}/user-balance?token={self.api_token}&type=json&api=2.0'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_email(self, site):
        email_type = random.choice(self.email_domains)
        url = f"{self.base_url}/mailbox-get-email?site={site}&mail_type={email_type}&token={self.api_token}&type=json&api=2.0"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_message(self, ID):
        full_param = '1'
        url = f"{self.base_url}/mailbox-get-message?id={ID}&token={self.api_token}&type=json&full={full_param}&api=2.0"

        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def cancel_email(self, ID):
        url = f'{self.base_url}/mailbox-cancel?id={ID}&token={self.api_token}&type=json&api=2.0'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def reorder_email(self, site, email, regex, subject, password=None):
        url = f"{self.base_url}/mailbox-reorder?site={site}&email={email}&token={self.api_token}&regex={regex}&subject={subject}&type=json&api=2.0"
        if password:
            url += f"&password={password}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_login_password(self, html_content):
        login_pattern = r'Twój login to: <b>([^<]+)</b>'
        password_pattern = r'Hasło: <b>([^<]+)</b>'

        login_match = re.search(login_pattern, html_content)
        password_match = re.search(password_pattern, html_content)

        if login_match and password_match:
            return login_match.group(1), password_match.group(1)
        else:
            return None, None

if __name__ == '__main__':
    load_dotenv()
    api_token = os.getenv('KOPEECHKA_API')
    client = KopeechkaClient(api_token)
    balance = client.get_balance()
    print(f'Balance: {balance}')

