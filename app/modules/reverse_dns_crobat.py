from .base_module import base_module_class


# Возращает список объектов и их IP в виде словарей
class reverse_dns_crobat_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 18
        self.name = 'reverse_dns_crobat_api'
        self.base = 'CrobatAPI'
        self.url = 'https://sonar.omnisint.io/reverse/'
        self.descr = "Rapid7's DNS Database easily searchable via a lightening fast API, with domains available in milliseconds."
        self.level = 2
        self.input = 'ip'

    def search(self, name: object) -> tuple[True, list[dict]] or tuple[False, str]:
        target = name.ip
        result = []
        try:
            res = self.make_request_get(self.url + target)
            if res:
                for i in res.json():
                    result.append({'object': i, 'ip': target})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
