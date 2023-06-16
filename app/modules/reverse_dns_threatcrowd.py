import json
from .base_module import base_module_class


# Возращает список объектов и их IP в виде словарей
class reverse_dns_threatcrowd_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 19
        self.name = 'reverse_dns_threatcrowd_api'
        self.base = 'ThreatcrowdAPI'
        self.url = 'https://www.threatcrowd.org/searchApi/v2/ip/report/?ip='
        self.descr = "Obtain information from ThreatCrowd about identified IP addresses, domains and e-mail addresses."
        self.level = 2
        self.input = 'ip'

    def search(self, name: object) -> tuple[True, list[dict]] or tuple[False, str]:
        target = name.ip
        result = []
        ready = []
        try:
            res = json.loads(self.make_request_get(self.url + target).content)
            if res and res['response_code'] != '0':
                for i in res['resolutions']:
                    try:
                        ready.append(i['domain'])
                        if 'www.' in i['domain']:
                            ready.append(i['domain'].split('www.')[1])
                    except:
                        pass
                for i in set(ready):
                    result.append({'object': i, 'ip': target})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
