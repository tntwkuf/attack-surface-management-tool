from .base_module import base_module_class
import json


# Возращает список объектов в виде словарей
class crt_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 4
        self.name = 'crt_api'
        self.base = 'CRT.SH'
        self.url = 'https://crt.sh/?q={}&output=json&exclude=expired'
        self.descr = 'Crt.sh is a web interface to a distributed database called the certificate transparency logs.'
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        try:
            res = self.make_request_get(self.url.format(name))
            if res:
                result = []
                temp = []
                content = res.content.decode('utf-8')
                data = json.loads(content)
                for i in data:
                    val = i['name_value']
                    if '*' not in val and val != name:
                        if '\n' in val:
                            temp.extend(val.split('\n'))
                        else:
                            temp.append(val)
                if temp:
                    for i in list(set(temp)):
                        result.append({'object': i})
                    return True, result
                else:
                    return False, 'Results is empty'
            else:
                return False, 'error'
        except Exception as e:
            return False, e
