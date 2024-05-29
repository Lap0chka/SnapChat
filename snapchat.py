import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from connect import Connect

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'


class SnapChat:
    """Login SnapChat, Parsing Chats, Send message"""

    def __init__(self, host=None, port=None, user=None, password=None):
        connect = Connect(host, port, user, password)
        self.driver = connect.get_chromedriver(use_proxy=True, user_agent=user_agent)

    def click_button(self, by='', value=''):
        time.sleep(2)
        submit_button = self.driver.find_element(by, value)
        submit_button.click()

    def input_field(self, by=None, value=None, inputs=None):
        time.sleep(2)
        input_field = self.driver.find_element(by, value)
        input_field.send_keys(inputs)

    def login(self, login, password, fa_code):
        self.driver.get("https://accounts.snapchat.com/accounts/v2/login")
        self.input_field(By.CLASS_NAME, 'form-control', login)
        self.click_button(By.XPATH, "//button[@type='submit' and contains(text(), 'Далее')]")
        time.sleep(4)
        self.input_field(By.CLASS_NAME, "form-control", password)
        self.click_button(By.XPATH, "//button[@type='submit' and contains(text(), 'Далее')]")
        ready_fa = self.twofa_auth(fa_code)
        self.input_field(By.CLASS_NAME, "form-control", ready_fa)
        self.click_button(By.XPATH, "//button[@type='submit' and contains(text(), 'Далее')]")
        time.sleep(3)

    def twofa_auth(self, fa_code):
        response = requests.get(f'https://2fa.live/tok/{fa_code}')
        fa_code = response.text.split(':\"')[-1][:-2]
        return fa_code

    def find_id_chats(self):
        chats = {}
        self.driver.get('https://web.snapchat.com/')
        time.sleep(4)
        self.click_button(By.CLASS_NAME, 'NRgbw')
        time.sleep(2)
        self.click_button(By.CLASS_NAME, 'O4POs')
        self.driver.execute_script("document.body.style.zoom='25%'")
        time.sleep(4)
        while True:
            flag = True
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            divs = soup.find_all("div", {"role": "listitem"})
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(3)
            for div in divs:
                try:
                    chat_name = div.find("span", class_="nonIntl").text
                    chat_id = div.find("span", class_="mYSR9 nonIntl").get("id")[6:]
                    if chat_id not in chats:
                        flag = False
                    chats[chat_id] = chat_name
                    print(f'Користувач {chat_name} добавлений')
                except:
                    print(f'Такий користувача уже добавлений')
            if flag:
                if not os.path.exists('chats'):
                    os.makedirs('chats')
                with open('chats/chats_id.json', "w") as file:
                    json.dump(chats, file, indent=4)
                return chats

    def send_message_all(self, chats='', send_message=None):
        for id, (index, name) in enumerate(chats.items(), 1):
            url = f'https://web.snapchat.com/{index}'
            self.driver.get(url)
            time.sleep(2)
            try:
                self.send_message(send_message, url)
                print(f'{id}. Повiдомлення користувачу {name} вiдправлено')
            except:
                print(f'Повiдомлення користувачу {name} не вiдправлено')
                time.sleep(20)
                self.driver.get(url)
                time.sleep(2)
                self.send_message(send_message, url)
                print(f'{id}. Повiдомлення користувачу {name} вiдправлено')

    def send_message(self, message, url=None):
        time.sleep(1)
        try:
            text_field = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
        except:
            self.driver.get(url)
            time.sleep(3)
            text_field = self.driver.find_element(By.XPATH, "//div[@role='textbox']")
        text_field.send_keys(message)
        text_field.send_keys(Keys.ENTER)
