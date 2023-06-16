from .base_module import base_module_class
import time


# Возращает список объектов в виде словарей
class urlscan_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 5
        self.name = 'urlscan_api'
        self.base = 'URLScan.io'
        self.url = 'https://urlscan.io/api/v1/scan/'
        self.descr = 'Urlscan.io - Website scanner for suspicious and malicious URLs.'
        self.level = 3
        self.get_api_key()
        self.headers.update({'API-Key': self.key, 'Content-Type': 'application/json'})
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        try:
            data = {'url': name, 'visibility': 'public'}
            post_response = self.make_request_post(self.url, data, None, True)
            if post_response:
                post_response = post_response.json()
                time.sleep(self.timeout)
                link = post_response['api']
                result = []
                temp = []
                res = self.make_request_get(link).json()
                try:
                    result.append({'object': name, 'ip': res['page']['ip']})
                    temp.append(name)
                except:
                    pass
                for d in res['lists']['domains']:
                    if d not in temp:
                        temp.append(d)
                        result.append({'object': d})
                        if 'www.' in d:
                            result.append({'object': d.split('www.')[1]})
                            temp.append(d.split('www.')[1])

                return True, result
            else:
                return False, post_response
        except Exception as e:
            return False, e
