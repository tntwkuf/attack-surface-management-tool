from bs4 import BeautifulSoup
from .base_module import base_module_class

# Возращает список объектов и открытых портов в виде словарей
class port_scan_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 8
        self.name = 'port_scan_api'
        self.base = 'ViewDNS'
        self.url = 'https://viewdns.info/portscan/?host='
        self.descr = 'The ViewDNS.info API allows webmasters to integrate the tools provided by ViewDNS.info into their own sites in a simple and effective manner.'
        self.level = 4
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        result = []
        try:
            res = self.make_request_get(self.url + name)
            if res:
                soup = BeautifulSoup(res.text, 'html.parser')
                for table in soup.find_all('table'):
                    for tr in table.find_all('tr'):
                        for td in tr.find_all('td'):
                            for row in td.find_all('table'):
                                maintable = row
                for tr in maintable.find_all('tr'):
                    for td in tr.find_all('td'):
                        if 'width' not in str(td):
                            value = td.get_text()
                            if value.isdigit():
                                port = value
                            if 'open' in str(td):
                                result.append(port)
                if not result:
                    return True, [{'object': name, 'ports': None}]
                else:
                    return True, [{'object': name, 'ports': ', '.join(result)}]
            else:
                return False, 'error'
        except Exception as e:
            return False, e
