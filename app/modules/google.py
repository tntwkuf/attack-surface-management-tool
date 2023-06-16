from bs4 import BeautifulSoup
from .base_module import base_module_class
import re


# Возращает список объектов и баннеров в виде словарей
class google_search(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 6
        self.name = 'google_search'
        self.base = 'Google'
        self.url = 'https://www.google.com/search?q=site:*.{}+-www.{}&start={}&sourceid=chrome&ie=UTF-8'
        self.descr = 'Google Search Engine + dorks'
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        result = []
        domains = []
        name = target.object
        e = 'smth wrong'
        for page in range(10):
            try:
                req = self.make_request_get(self.url.format(name, name, page * 10))
                soup = BeautifulSoup(req.content, features="lxml").prettify()
                for i in re.findall('(?:<a href=".url).+(?:' + name + ')', soup):
                    link = i.split('//')[1]
                    if 'google' not in link and link not in domains:
                        try:
                            header = self.make_request_get(f'https://{link}', tmout=10).headers[
                                'Server']
                        except:
                            try:
                                header = \
                                    self.make_request_get(f'http://{link}', tmout=10).headers[
                                        'Server']
                            except:
                                header = None
                        domains.append(link)
                        result.append({'object': link, 'banner': header})
            except Exception as q:
                e = q
                pass
        if result:
            return True, result
        else:
            return False, e
