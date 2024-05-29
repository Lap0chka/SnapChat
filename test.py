import time

from snapchat import SnapChat
import json
import requests
from lxml import html
from selenium import webdriver
import pickle

login = 'lily30mur'
password = 'Murphy30L'
fa_code = 'ME4D H6FI TKDU E65Z ZDY3 VF7X 6SPR HAMH'
PROXY_HOST = '37.218.212.238'
PROXY_PORT = 44444
PROXY_USER = '14ada936fa640'
PROXY_PASS = 'e8748289a0'
headers = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
}

fa_code = "".join([i for i in fa_code if not i.isspace()])

proxy = {
    'https': f'http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}'
}


class SnapChatt:
    def __init__(self, login=None, password=None, fa_code=None):
        self.login = login
        self.password = password
        self.fa_code = fa_code
        self.auth_token = '31778d1e5d10d6c14a31'
        self.session = requests.Session()
        if all([login, password, fa_code]):
            self.login_entrance()

    @property
    def fa_code(self):
        return self.__fa_code

    @fa_code.setter
    def fa_code(self, value):
        response = requests.get(f'https://2fa.live/tok/{value}')
        fa_code = response.text.split(':\"')[-1][:-2]
        self.__fa_code = fa_code

    def login_entrance(self):
        params = {
            'ai': 'Zm9sZW1sb3JkQGdtYWlsLmNvbQ==',
            'continue': '/accounts/sso?client_id=web-calling-corp--prod&referrer=https%3A%2F%2Fweb.snapchat.com%2F1bf09d33-9a82-58da-9283-9388e95d647e',
        }
        data = {
            'password': self.password,
            'xsrf_token': self.fa_code,
            'ai_token': self.login,
            'continue': '/accounts/sso?client_id=web-calling-corp--prod&referrer=https%3A%2F%2Fweb.snapchat.com%2F1bf09d33-9a82-58da-9283-9388e95d647e',
        }

        response = self.session.post(
            'https://accounts.snapchat.com/accounts/v2/password',
            params=params,
            headers=headers,
            data=data,
            proxies=proxy
        )

        print(response)

    def _timestamp(self):
        return int(time.time() + 60)

    def post(self, endpoint, data):
        """Submit a post request to the Snapchat API.

        :param endpoint: The service to submit the request to, i.e. '/upload'.
        :param data: The data to upload.
        :param params: Request specific authentication, typically a tuple of form (KEY, TIME).
        :param file: Optional field for submitting file content in multipart messages.
        """



        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
        }

        url = 'https://web.snapchat.com/' + endpoint

        r = self.session.post(url, data, headers=headers)

        print(r)
    def send_message(self, media_id='Test', recipients="3249b4f5-4927-5c44-b7ee-84b582360df4",):
        if not isinstance(recipients, list):
            recipients = [recipients]

        timestamp = self._timestamp()
        time = 10
        data = {
            "send_message_attempt_id": "3249b4f5-4927-5c44-b7ee-84b582360df4",
            "message": media_id,
            "snapchat_user_id": "9706e3e0-0aee-4f18-8bb4-1007c232ce1e",
            "timestamp": timestamp,

        }


        self.post('/messagingcoreservice.MessagingCoreService/CreateContentMessage', data)



s = SnapChatt(login, password, fa_code)
s.send_message()
