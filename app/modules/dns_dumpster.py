from .base_module import base_module_class
from bs4 import BeautifulSoup
import re

# def retrieve_results(table):
#     res = []
#     trs = table.findAll('tr')
#     for tr in trs:
#         tds = tr.findAll('td')
#         pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
#         ip = re.findall(pattern_ip, tds[1].text)[0]
#         domain = str(tds[0]).split('<br/>')[0].split('>')[1].split('<')[0]
#         header = ' '.join(tds[0].text.replace('\n', '').split(' ')[1:])
#         reverse_dns = tds[1].find('span', attrs={}).text
#
#         additional_info = tds[2].text
#         country = tds[2].find('span', attrs={}).text
#         autonomous_system = additional_info.split(' ')[0]
#         provider = ' '.join(additional_info.split(' ')[1:])
#         provider = provider.replace(country, '')
#         data = {'domain': domain,
#                 'ip': ip,
#                 'reverse_dns': reverse_dns,
#                 'as': autonomous_system,
#                 'provider': provider,
#                 'country': country,
#                 'header': header}
#         res.append(data)
#
#     return res

# Возращает список объектов, IP и баннеров в виде словарей
class dns_dumpster_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 10
        self.name = 'dns_dumpster_api'
        self.base = 'DNSDumpsterAPI'
        self.url = 'https://dnsdumpster.com/'
        self.descr = "DNSdumpster.com is a FREE domain research tool that can discover hosts related to a domain."
        self.level = 3
        self.headers.update({'User-Agent': self.randomize_user_agent()})
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        result = []
        self.__init__()
        try:
            req = self.make_request_get(self.url)
            soup = BeautifulSoup(req.content, 'html.parser')
            csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']
        except Exception as e:
            return False, e
        cookies = {'csrftoken': csrf_middleware}
        data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': name, 'user': 'free'}
        self.headers.update({'referer': self.url, 'Content-type': 'application/x-www-form-urlencoded'})
        try:
            req = self.make_request_post(self.url, data=data, cookies=cookies)
        except Exception as e:
            return False, e
        if req:
            if req.status_code != 200:
                return False, "Unexpected status code: {code}".format(code=req.status_code)

            if 'There was an error getting results' in req.content.decode('utf-8'):
                return False, "There was an error getting results"

            if 'The requested resource was not found on this server' in req.content.decode('utf-8'):
                return False, "The requested resource was not found on this server"
        else:
            return False, f"There was an error: {req}"

        soup = BeautifulSoup(req.content, 'html.parser')
        tbl = soup.findAll('table')
        try:
            trs = tbl[3].findAll('tr')
            for tr in trs:
                tds = tr.findAll('td')
                pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
                result.append({'object': str(tds[0]).split('<br/>')[0].split('>')[1].split('<')[0],
                               'ip': re.findall(pattern_ip, str(tds[1]))[0],
                               'banner': ' '.join(tds[0].text.replace('\n', '').split(' ')[1:])})
            return True, result
        except Exception as e:
            return False, e
