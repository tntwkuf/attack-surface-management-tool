from .base_module import base_module_class
import socket

# Возращает список объектов и их IP в виде словарей
class resolve_host_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 7
        self.name = 'resolve_host_api'
        self.base = 'DNS Resolve'
        self.url = 'DNS Resolve'
        self.descr = "DNS Resolve."
        self.level = 10
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        name = target.object
        try:
            ip = list(socket.gethostbyname_ex(name))[2][0]
            return True, [{'object': name, 'ip': ip}]
        except socket.gaierror:
            return True, [{'object': name, 'ip': None}]
        except Exception as e:
            return False, e
