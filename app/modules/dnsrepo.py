from .base_module import base_module_class
from bs4 import BeautifulSoup
import re

# Возращает список объектов в виде словарей
class dnsrepo_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 14
        self.name = 'dnsrepo_api'
        self.base = 'DNSRepo'
        self.url = 'https://dnsrepo.noc.org/?search={}'
        self.descr = 'DNS Database Repository Search'
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        pattern = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
        name = target.object
        try:
            res = self.make_request_get(self.url.format(name))
            if res:
                soup = BeautifulSoup(res.text, 'html.parser')
                result = []
                temp = []
                for table in soup.find_all('table'):
                    for tr in table.find_all('tr'):
                        values = tr.find_all('td')
                        if values:
                            name = values[0].text[:-1]
                            for ip in values[1].text.split('\n'):
                                if re.findall(pattern, ip) and name not in temp:
                                    result.append({'object': name, 'ip': ip})
                                    temp.append(name)
                                    break
                if result:
                    return True, result
                else:
                    return False, 'Results is empty'
            else:
                return False, 'Error'
        except Exception as e:
            return False, e
