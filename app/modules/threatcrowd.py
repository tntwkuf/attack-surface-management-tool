import json
from .base_module import base_module_class
from datetime import datetime

# Возращает список объектов в виде словарей и IP адрес объекта из запроса
class threatcrowd_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 12
        self.name = 'threatcrowd_api'
        self.base = 'ThreatcrowdAPI'
        self.url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain='
        self.descr = "Obtain information from ThreatCrowd about identified IP addresses, domains and e-mail addresses."
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        result = []
        domains = []
        try:
            res = json.loads(self.make_request_get(self.url + name).content)
            if res and res['response_code'] != '0':
                dates = {}
                for i in res['resolutions']:
                    try:
                        dates.update({datetime.strptime(i['last_resolved'], '%Y-%m-%d'): i['ip_address']})
                    except:
                        pass
                ip = dates.get(min([i for i in list(dates.keys())], key=lambda x: abs(x - datetime.now())))
                result.append({'object': name, 'ip': ip})
                for i in res['subdomains']:
                    if i not in domains:
                        result.append({'object': i})
                        domains.append(i)
                        if 'www.' in i:
                            result.append({'object': i.split('www.')[1]})
                            domains.append(i.split('www.')[1])
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
