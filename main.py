from snapchat import SnapChat
from time import perf_counter

login = 'lily30mur'
password = 'Murphy30L'
fa_code = 'ME4D H6FI TKDU E65Z ZDY3 VF7X 6SPR HAMH'
PROXY_HOST = '37.218.212.238'
PROXY_PORT = 44444
PROXY_USER = '14ada936fa640'
PROXY_PASS = 'e8748289a0'

fa_code = "".join([i for i in fa_code if not i.isspace()])


def main():
    start = perf_counter()
    s = SnapChat(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    s.login(login, password, fa_code)
    chats = s.find_id_chats()
    s.pars_chat(chats, 'Hi how are you?')  # 2 второй параметр сообщение
    finish = perf_counter()
    print('Time:', finish - start)


if __name__ == '__main__':
    main()
