from bs4 import BeautifulSoup
from .base_module import base_module_class


# Возращает список объектов в виде словарей
class reverse_ip_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 20
        self.name = 'reverse_ip_api'
        self.base = 'RapidDNS'
        self.url = 'https://rapiddns.io/sameip/{}?full=1'
        self.descr = 'RapidDNS is a dns query tool which make querying subdomains or sites of a same ip easy!'
        self.level = 2
        self.input = 'ip'

    def search(self, name: object) -> tuple[True, list[dict]] or tuple[False, str]:
        target = name.ip
        result = []
        try:
            res = self.make_request_get(self.url.format(target))
            if res:
                soup = BeautifulSoup(res.text, 'html.parser')
                for table in soup.find_all('table'):
                    for tr in table.find_all('tr'):
                        if tr.find_all('td'):
                            target = tr.find_all('td')[0].text
                            ip = tr.find_all('td')[1].text.strip('\n')
                            result.append({'object': target, 'ip': ip})
                            if 'www.' in target:
                                result.append({'object': target.split('www.')[1], 'ip': ip})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
