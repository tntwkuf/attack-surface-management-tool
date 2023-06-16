from .base_module import base_module_class


# Возращает список объектов в виде словарей
class crobat_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 9
        self.name = 'crobat_api'
        self.base = 'CrobatAPI'
        self.url = 'https://sonar.omnisint.io/subdomains/'
        self.descr = "Rapid7's DNS Database easily searchable via a lightening fast API, with domains available in milliseconds."
        self.level = 3
        self.input = 'object'

    def search(self, target:object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        result = []
        try:
            for i in self.make_request_get(self.url + name).json():
                result.append({'object': i})
            if result:
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
