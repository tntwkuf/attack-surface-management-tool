import json
from .base_module import base_module_class

# Возращает список объектов в виде словарей
class sublister_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 11
        self.name = 'sublister_api'
        self.base = 'SublisterAPI'
        self.url = 'https://api.sublist3r.com/search.php?domain='
        self.descr = "Passive subdomain enumeration using Sublist3r's API"
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        result = []
        try:
            res = self.make_request_get(self.url + name)
            if res and res.text != 'null':
                for i in json.loads(res.content):
                    result.append({'object': i})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
