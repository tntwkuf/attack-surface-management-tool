from bs4 import BeautifulSoup
from .base_module import base_module_class


# Возращает список объектов в виде словарей
class reverse_whois_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 2
        self.name = 'reverse_whois_api'
        self.base = 'ViewDNS'
        self.url = 'https://viewdns.info/reversewhois/?q='
        self.descr = 'This free tool will allow you to find domain names owned by an individual person or company. Simply enter the email address or name of the person or company to find other domains registered using those same details. FAQ.'
        self.level = 1
        self.input = 'keyword'

    def search(self, name: str) -> tuple[True, list[dict]] or tuple[False, str]:
        result = []
        try:
            res = self.make_request_get(self.url + name)
            if res:
                soup = BeautifulSoup(res.text, 'html.parser')
                tables = [
                    [
                        [td.get_text(strip=True) for td in tr.find_all('td')]
                        for tr in table.find_all('tr')
                    ]
                    for table in soup.find_all('table')
                ]
                for i in range(1, (len(tables[3]))):
                    result.append({'object': tables[3][i][0]})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
