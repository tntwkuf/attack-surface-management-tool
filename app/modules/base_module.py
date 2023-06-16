import urllib3
from .. import conf
import requests
from netaddr import IPNetwork, IPAddress
import json
import random
from colorama import Fore, Style
import datetime, time


# Базовый класс для поисковых модулей
class base_module_class():
    '''
    id - уникальный номер модуля
    name - наименование модуля
    url - основная поисковая ссылка
    descr - описание модуля
    crawl_count - количество ссылок, которые проверяет crawler в пределах одного домена/поддомена
    level - уровень, на котором работает модуль
    timeout - таймаут для http-запросов в модуле
    base - на какой системе/API базируется модуль
    input - какие параметры принимает на вход
    headers - заголовки для http-запросов
    need_proxy - флаг о необходимости использования прокси для запросов
    proxies - список используемых прокси
    '''

    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.id = 0
        self.name = ''
        self.url = ''
        self.descr = ''
        self.crawl_count = 1000
        self.level = 0
        self.timeout = 30
        self.base = ''
        self.input = ''
        self.headers = conf.HEADERS
        self.need_proxy = conf.PROXY_NEEDED
        if self.need_proxy:
            self.proxies = conf.PROXIES
        else:
            self.proxies = None

    # Метод для получения ключа API из настроек
    def get_api_key(self) -> None:
        if self.name in list(conf.API_KEYS.keys()):
            self.key = conf.API_KEYS[self.name]
        else:
            self.key = None

    # Метод для отправки запроса GET
    def make_request_get(self, target: str, tmout=None) -> requests.models.Response:
        res = requests.get(target, verify=False, proxies=self.proxies, timeout=tmout or self.timeout,
                           headers=self.headers)
        if res.ok:
            return res
        else:
            return None

    # Метод для отправки запроса POST
    def make_request_post(self, url, data, cookies=None, data_need_dumps=False) -> requests.models.Response or None:
        if data_need_dumps:
            data = json.dumps(data)
        try:
            response = requests.post(url, verify=False, proxies=self.proxies, cookies=cookies, timeout=self.timeout,
                                     headers=self.headers,
                                     data=data)
            return response
        except:
            return \
                None

    # Метод для разбиения подсети на отдельные IP адреса
    def separate_subnet(self, target: str) -> list[str]:
        result = []
        for ip in IPNetwork(target):
            result.append(str(ip))
        return result

    # Метод для проверки, входит ли объект в исключения
    def is_exception(self, target: str, exceptions: list[str]) -> bool:
        if target in exceptions:
            return True
        else:
            return False

    # Метод, возвращающий объект без http/https и его домен
    def get_domain_from_record(self, target: str) -> tuple[str, str]:
        rec = target.replace('http://', '').replace('https://', '')
        rec = rec.split('/')[0]
        dom = rec.split('.')[-2] + '.' + rec.split('.')[-1]
        return rec, dom

    # Метод для проверки, проверялся ли данный объект модулем
    def is_checked(self, name, progress) -> bool:
        if self.input == 'keyword':
            if name in [i.object for i in progress]:
                return True
            else:
                return False
        elif self.input == 'object':
            if name.object in [i.object for i in progress]:
                return True
            else:
                return False
        elif self.input == 'ip':
            if name.ip in [i.object for i in progress]:
                return True
            else:
                return False
        elif self.input == 'domain':
            rec, dom = self.get_domain_from_record(name.object)
            for i in [i.object for i in progress]:
                if dom == self.get_domain_from_record(i)[1]:
                    return True
            return False

    def randomize_user_agent(self) -> str:
        random.seed()
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',            
        ]
        return random.choice(user_agents)

    # Выводит сообщение о начале обработки объекта модулем
    def print_start(self, name: str) -> None:
        print(
            f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}][START] {self.name} - {name}' + '\033[39m' + Style.RESET_ALL)

    # Выводит сообщение о успешной обработке объекта модулем
    def print_succes(self, name: str) -> None:
        print(Fore.GREEN + Style.BRIGHT +
              f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}][SUCCESS] {self.name} - {name}' + '\033[39m' + Style.RESET_ALL)

    # Выводит сообщение о ошибке обработки объекта модулем
    def print_fail(self, name: str, error: str) -> None:
        print(Fore.RED + Style.BRIGHT +
              f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}][FAIL] {self.name} - {name} - {error}' + '\033[39m' + Style.RESET_ALL)

    # Выводит сообщение о том, что объект уже обработан модулем
    def print_exists(self, name: str) -> None:
        print(Fore.YELLOW + Style.BRIGHT +
              f'[{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}][ALREADY EXISTS] {self.name} - {name}' + '\033[39m' + Style.RESET_ALL)
