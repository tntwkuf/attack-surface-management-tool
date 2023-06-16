from .base_module import base_module_class
from .cve_circl import cve_circl_api


# Возращает список объектов и уязвимостей в виде словарей
class shodan_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 13
        self.name = 'shodan_api'
        self.base = 'ShodanAPI'
        self.url = 'https://internetdb.shodan.io/'
        self.descr = 'Shodan is a search engine for Internet-connected devices.'
        self.level = 4
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.ip
        result = []
        if not name:
            return False, 'Invalid IP'
        for ip in name.split(', '):
            try:
                res = self.make_request_get(self.url + ip)
                if res:
                    for i in res.json()['vulns']:
                        r, q = cve_circl_api().search(i)
                        if r:
                            result.append({'object': target.object, 'vulns': (i, q[0], q[1])})
            except:
                pass
        if result:
            return True, result
        else:
            return False, 'Result is empty'
