from .base_module import base_module_class


# Возращает список объектов и IP в виде словарей
class bgp_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 1
        self.name = 'bgp_api'
        self.base = 'BGPVIew'
        self.url = 'https://api.bgpview.io/search?query_term='
        self.descr = 'BGPView is a simple API allowing consumers to view all sort of analytics data about the current state and structure of the internet.'
        self.level = 0
        self.input = 'keyword'

    def search(self, name: str) -> tuple[True, list[dict]] or tuple[False, str]:
        prefixes = []
        result = []
        try:
            res = self.make_request_get(self.url + name).json()
            if res:
                for i in res['data']['ipv4_prefixes']:
                    if i['prefix'] not in prefixes:
                        prefixes.append(i['prefix'])
                        for ip in self.separate_subnet(i['prefix']):
                            result.append({'ip': ip})
                return True, result
            else:
                return False, 'error'
        except Exception as e:
            return False, e
