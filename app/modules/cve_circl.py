from .base_module import base_module_class


# Возращает список объектов и их IP в виде словарей
class cve_circl_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 21
        self.name = 'cve_circl_api'
        self.base = 'CVE Search'
        self.url = 'https://cve.circl.lu/api/cve/'
        self.descr = "CVE Search is accessible via a web interface and an HTTP API. cve-search is an interface to search publicly known information from security vulnerabilities in software and hardware along with their corresponding exposures."
        self.level = 10

    def search(self, name: str) -> tuple[True, tuple[str, str]] or tuple[False, str]:
        try:
            res = self.make_request_get(self.url + name)
            if res:
                if res.json()['cvss']:
                    cvss = str(res.json()['cvss'])
                else:
                    cvss = None
                if res.json()['summary']:
                    summary = res.json()['summary']
                else:
                    summary = None
                return True, (cvss, summary)
            else:
                return False, 'error'
        except Exception as e:
            return False, e
