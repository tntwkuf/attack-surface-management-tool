import re
from .base_module import base_module_class


# Возращает список объектов в виде словарей
class virustotal_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 15
        self.name = 'virustotal_api'
        self.base = 'VirusTotal'
        self.url = "https://www.virustotal.com/api/v3/domains/"
        self.descr = 'Analyze suspicious files, domains, IPs and URLs to detect malware and other breaches, automatically share them with the security community'
        self.level = 3
        self.get_api_key()
        self.headers.update({"Accept": "application/json", "x-apikey": self.key})
        self.input = 'domain'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = self.get_domain_from_record(target.object)[1]
        cursor = None
        err = 'Result is empty'
        result = []
        while True:
            try:
                if cursor:
                    url = self.url + name + "/subdomains?limit=40" + '&cursor=' + cursor
                else:
                    url = self.url + name + "/subdomains?limit=40"
                response = self.make_request_get(url).json()
                for rec in response['data']:
                    d = rec['id']
                    for attr in rec['attributes']['last_dns_records']:
                        if attr.get('value', None) and not bool(re.search('[a-zA-Z]', attr['value'])):
                            ip = attr['value']
                    result.append({'object': d, 'ip': ip})
                    if 'www.' in d:
                        result.append({'object': d.split('www.')[1], 'ip': ip})
                    d = None
                    ip = None
                if response['meta'].get('cursor', None):
                    cursor = response['meta']['cursor']
                else:
                    break
            except Exception as e:
                err = e
                break
        if result:
            return True, result
        else:
            return False, err
