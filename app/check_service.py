from Wappalyzer import Wappalyzer, WebPage
import requests, urllib3
from .conf import PROXIES, HEADERS
from netaddr import IPAddress
from datetime import datetime
from django.http import HttpResponse
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebChecker():
    def __init__(self):
        self.headers = HEADERS.copy()
        self.proxies = PROXIES.copy()
        self.seleniumwire_proxy = PROXIES.copy()
        self.seleniumwire_proxy.update({'no_proxy': 'localhost,127.0.0.1'})
        self.verify = False
        self.redirects = True
        self.timeout = 5
        self.sync_time = datetime.now().strftime("%d.%m.%Y")
        self.log = ''
        self.temp_log = ''
        self.plug_words = ['(На домене .* пока нет сайта)', '(Сайт находится в разработке)', '(Welcome to nginx!)',
                           '(Burp Suite)']

    def transform_cyrillic(self, text):
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        if not alphabet.isdisjoint(text.lower()):
            return text.encode('idna').decode()
        else:
            return text

    def check_plug(self, text):
        for w in self.plug_words:
            if re.search(w, text):
                return True
        return False

    def check_dns_record(self, target):
        domain = self.transform_cyrillic(target)
        self.headers.update({'Host': 'networkcalc.com'})
        try:
            r = requests.get("https://networkcalc.com/api/dns/lookup/" + domain, verify=self.verify,
                             proxies=self.proxies, headers=self.headers, allow_redirects=self.redirects,
                             timeout=self.timeout)
            if r.ok:
                return {'A': [x['address'] for x in r.json()['records']['A'] if x and x.get('address')]} or None
            else:
                return None
        except:
            return None

    def check_available_by_dns_name(self, target):
        domain = self.transform_cyrillic(target)
        _ = self.headers.pop('Host') if self.headers.get('Host') else None
        try:
            print('@@@@@@')
            resp = requests.get(url='https://' + domain, verify=self.verify, proxies=self.proxies, headers=self.headers,
                                allow_redirects=self.redirects, timeout=self.timeout)
            if 'Burp Suite' in resp.text:
                raise Exception
            print('1 ', resp.status_code, resp.status_code, resp.content)
        except Exception as e:
            print('11 ', e)
            try:
                print('#######')
                time.sleep(2)
                resp = requests.get(url='http://' + domain, proxies=self.proxies,
                                    headers=self.headers, allow_redirects=self.redirects, timeout=self.timeout)
                print('2 ', resp.status_code, resp.status_code, resp.content)
            except Exception as q:
                print('22', q)
                return None
        try:
            if 'spb99-prx' not in resp.url and not self.check_plug(resp.text) and 'Burp Suite' not in resp.text:
                return resp.status_code
        except:
            pass
        return None

    def check_available_by_ip(self, target, ip):
        domain = self.transform_cyrillic(target)
        self.headers.update({'Host': domain})
        try:
            resp = requests.get(url=f'https://{ip}:443', verify=self.verify, proxies=self.proxies,
                                headers=self.headers, allow_redirects=self.redirects, timeout=self.timeout)
        except:
            try:
                resp = requests.get(url=f'http://{ip}:80', proxies=self.proxies,
                                    headers=self.headers, allow_redirects=self.redirects, timeout=self.timeout)
            except:
                return None
        try:
            if 'spb99-prx' not in resp.url and not self.check_plug(resp.text):
                return resp.status_code
        except:
            pass
        return None

    def check_name_is_not_private_ip(self, name):
        result = True
        try:
            if IPAddress(name).is_private() or name == '127.0.0.1':
                result = False
        except:
            pass
        return result

    def check_web_techs(self, target):
        domain = self.transform_cyrillic(target)
        if domain:
            _ = self.headers.pop('Host') if self.headers.get('Host') else None
            try:
                resp = requests.get(url=f'https://{domain}', verify=self.verify, proxies=self.proxies,
                                    headers=self.headers, allow_redirects=self.redirects, timeout=self.timeout)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ProxyError):
                try:
                    resp = requests.get(url=f'http://{domain}', proxies=self.proxies,
                                        headers=self.headers, allow_redirects=self.redirects, timeout=self.timeout)
                except (requests.exceptions.ReadTimeout, requests.exceptions.ProxyError):
                    return None
            if resp:
                wappalyzer = Wappalyzer.latest()
                webpage = WebPage.new_from_response(resp)
                analyze = wappalyzer.analyze_with_versions(webpage)
                tech = None
                if analyze:
                    tech = [{x: y['versions']} if y['versions'] else {x: '-'} for x, y in analyze.items()]

                return {'final_url': resp.url,
                        'tech': tech}
            return None

    # def driver_initial(self):
    #     options = EdgeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--disable-gpu")
    #     options.add_argument("--no-sandbox")
    #     options.add_argument("--disable-infobars")
    #     options.add_argument("--disable-dev-shm-usage")
    #     options.add_argument("--ignore-certificate-errors")
    #     options.add_argument("--window-size=1920,1080")
    #     seleniumwire_options = {'proxy': self.seleniumwire_proxy}
    #     path = os.path.join(os.getcwd(), 'SOC', 'apps', 'perimetr', 'tools', 'dnsrecords', 'msedgedriver.exe')
    #     driver = webdriver.Edge(executable_path=path, seleniumwire_options=seleniumwire_options, edge_options=options)
    #     return driver
    #
    # def get_screen(self, target):
    #     try:
    #         driver = self.driver_initial()
    #         driver.get(target)
    #         screenshot = driver.get_screenshot_as_png()
    #         driver.quit()
    #         return io.BytesIO(screenshot)
    #     except Exception as e:
    #         return e


def complex_check(records_list):
    if records_list:
        checker = WebChecker()
        for record in records_list:
            checker.temp_log = ''
            try:
                # Проверка DNS-записи
                try:
                    dns_records = checker.check_dns_record(record.object)
                    # Если DNS-запись существует
                    if dns_records:
                        # Если в ней есть А-запись
                        if dns_records.get('A'):
                            # Трансформируем А-запись в строку
                            format_records = ', '.join(sorted(dns_records['A']))
                            if record.ip:
                                for f in sorted(dns_records['A']):
                                    if f not in record.ip.split(', '):
                                        record.ip += ', ' + f
                                        checker.temp_log += f'{checker.sync_time} {record.object} - добавлен IP из А-записи {f}\n'
                            else:
                                record.ip = format_records
                            # Если старая и новая запись не совпадают, пишем это в лог и обновляем запись
                            if record.a_record != format_records:
                                checker.temp_log += f'{checker.sync_time} {record.object} - изменилась А-запись {record.a_record} -> {format_records}\n'
                            record.a_record = format_records
                        # Если в результате нет А-записи, пишем в лог и сбрасываем поле
                        else:
                            checker.temp_log += f'{checker.sync_time} {record.object} - удалена A-запись\n'
                            record.a_record = None
                    # Если DNS-записи нет
                    else:
                        checker.temp_log += f'{checker.sync_time} {record.object} - не обнаружена DNS-запись\n'
                        record.a_record = None
                except Exception as e:
                    checker.temp_log += f'{checker.sync_time} {record.object} - ошибка в получении DNS-записи: {e}\n'
                # Проверка доступности по доменному имени и IP
                try:
                    # Если А-запись существует, проверяем доступность по hostname
                    if record.a_record:
                        # Сохраняем старое значение и проверяем доступность
                        old_resp_code_hostname = record.response_code_hostname
                        record.response_code_hostname = checker.check_available_by_dns_name(
                            record.object) or record.response_code_hostname or None
                        # Если ответ получен
                        if record.response_code_hostname:
                            # Если код ответа между 200 и 299, то ресурс доступен
                            if 200 <= int(record.response_code_hostname) <= 299:
                                record.online_by_hostname = True
                                record.online_by_ip = True
                            else:
                                record.online_by_hostname = False
                                record.online_by_ip = False
                            record.response_code_ip = record.response_code_hostname
                        # Если ответа нет, сбрасываем флаг
                        else:
                            record.online_by_hostname = False
                        if str(old_resp_code_hostname) != str(record.response_code_hostname):
                            checker.temp_log += f'{checker.sync_time} {record.object} - изменился код ответа {old_resp_code_hostname} -> {record.response_code_hostname}\n'
                    # Если А-записи нет, проверяем доступность по IP
                    else:
                        record.online_by_hostname = False
                        record.response_code_hostname = None
                        resp_codes = []
                        # Сохраняем текущие коды ответа по IP
                        old_resp_code_ip = record.response_code_ip
                        # Проходим по всем связанным сервисам и проверяем их доступность
                        if record.ip:
                            for s in record.ip.split(', '):
                                q = checker.check_available_by_ip(record.object, s)
                                if q:
                                    resp_codes.append(str(q))
                        # Если есть коды ответа сервисов, формируем строку
                        if resp_codes:
                            record.response_code_ip = ', '.join(resp_codes)
                        else:
                            record.response_code_ip = None
                        record.online_by_ip = False
                        # Если среди кодов есть правильный, ставим флаг и прекращаем цикл
                        for s in resp_codes:
                            if 200 <= int(s) <= 299:
                                record.online_by_ip = True
                                break
                        if str(old_resp_code_ip) != str(record.response_code_ip):
                            checker.temp_log += f'{checker.sync_time} {record.object} - изменился код ответа по IP {old_resp_code_ip} -> {record.response_code_ip}\n'
                except Exception as e:
                    record.online_by_hostname = False
                    record.online_by_ip = False
                    record.response_code_hostname = None
                    record.response_code_ip = None
                    checker.temp_log += f'{checker.sync_time} {record.object} - ошибка в определении доступности: {e}\n'

                # Проверка технологий и редиректа
                try:
                    tech = checker.check_web_techs(record.object)
                    # Если ответ получен
                    if tech:
                        # Если есть технологии
                        if tech['tech']:
                            format_tech = ", ".join(sorted([str(i) for i in tech["tech"]])).replace("}", "").replace(
                                "{", "").replace("'", "")
                            # Если технологии изменились
                            if format_tech != record.techs:
                                checker.temp_log += f'{checker.sync_time} {record.object} - изменились технологии {record.techs} -> {format_tech}\n'
                                record.techs = format_tech
                        # Если раньше технологии были, но больше нет
                        elif record.techs:
                            checker.temp_log += f'{checker.sync_time} {record.object} - изменились технологии {record.techs} -> None\n'
                            record.techs = None
                        # Если есть финальный адрес
                        if tech['final_url']:
                            # Если адрес изменился
                            if tech['final_url'] != record.redirect:
                                checker.temp_log += f'{checker.sync_time} {record.object} - изменился редирект {record.redirect} -> {tech["final_url"]}\n'
                                record.redirect = tech['final_url']
                        # Если раньше адрес редиректа был, но сейчас нет
                        elif record.redirect:
                            checker.temp_log += f'{checker.sync_time} {record.object} - изменился редирект {record.redirect} -> None\n'
                            record.redirect = None
                except Exception as e:
                    record.techs = None
                    record.redirect = None
                    checker.temp_log += f'{checker.sync_time} {record.object} - ошибка в определении технологий: {e}\n'
                record.save()
            except Exception as e:
                checker.temp_log += f'{checker.sync_time} {record.object} - возникла ошибка: {e}\n'
            checker.log += checker.temp_log
        filename = f'dnsrecords_check_log_{checker.sync_time}.txt'
        response = HttpResponse(checker.log, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
    else:
        return HttpResponse('Список объектов пуст')
