from .base_module import base_module_class


# Возращает список объектов в виде словарей
class tld_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 3
        self.name = 'tld_api'
        self.base = 'CrobatAPI'
        self.url = 'https://sonar.omnisint.io/tlds/'
        self.descr = 'The entire Rapid7 Sonar DNS dataset indexed, available at your fingertips.'
        self.level = 1
        self.input = 'keyword'

    def search(self, name: str) -> tuple[True, list[dict]] or tuple[False, str]:
        try:
            result = []
            for r in self.make_request_get(self.url + name).json():
                result.append({'object': r})
            if result:
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
