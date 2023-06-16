from .base_module import base_module_class
import re
from bs4 import BeautifulSoup


# Возращает список объектов в виде словарей
class rapiddns_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 16
        self.name = 'rapiddns_api'
        self.base = 'RapidDNS API'
        self.url = 'https://rapiddns.io/subdomain/{}?full=1'
        self.descr = 'RapidDNS is a dns query tool which make querying subdomains or sites of a same ip easy!'
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        try:
            res = self.make_request_get(self.url.format(name))
            if res:
                result = []
                temp = {}
                ch = {}
                soup = BeautifulSoup(res.text, 'html.parser')
                for table in soup.find_all('table'):
                    for tr in table.find_all('tr'):
                        values = tr.find_all('td')
                        if values and values[2].text in ['A', 'CNAME']:
                            name = values[0].text
                            if not bool(re.search('[a-zA-Z]', values[1].text)):
                                ip = values[1].text.strip('\n')
                                temp.update({name: ip})
                            else:
                                ch.update({name: values[1].text.strip('\n')})
                for i in ch.items():
                    ip = temp.get(i[1], None)
                    if ip and i[0] not in list(temp.keys()):
                        temp.update({i[0]: ip})

                for i in temp.items():
                    result.append({'object': i[0], 'ip': i[1]})
                if result:
                    return True, result
                else:
                    return False, 'Result is empty'
            else:
                return False, 'Error'
        except Exception as e:
            return False, e
