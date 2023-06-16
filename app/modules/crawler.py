from .base_module import base_module_class
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import time


# Возращает список объектов и их IP в виде словарей
class crawler_api(base_module_class):
    def __init__(self):
        base_module_class.__init__(self)
        self.id = 17
        self.name = 'crawler_api'
        self.base = 'Requests'
        self.url = '-'
        self.descr = "Recursive crawl of all url from the site"
        self.level = 3
        self.input = 'object'

    def search(self, target: object) -> tuple[True, list[dict]] or tuple[False, str]:
        target = 'https://' + target.object
        pool = [target]
        visited = []
        ext = []
        count = 0
        while pool and count <= self.crawl_count:
            time.sleep(self.timeout / 15)
            url = pool.pop(0)
            print(f'[#] {url}')
            try:
                req = self.make_request_get(target=url, tmout=10)
                if req and req.ok:
                    soup = BeautifulSoup(req.content, "html.parser")
                    for a_tag in soup.findAll("a"):
                        href = a_tag.attrs.get("href")
                        if href == "" or href is None or 'tel:' in href or 'void(0)' in href:
                            continue
                        href = urljoin(url, href)
                        parsed_href = urlparse(href)
                        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                        if href.lower().endswith(
                                ('.pdf', '.rar', '.zip', '.doc', '.docx', '.xls', '.xlsx', '.jpg', '.img', '.png',
                                 '.exe', '.jpeg', '.mp4', '.mpeg', '.mp3', '.tif', '.gif')):
                            continue
                        if urlparse(url).netloc != urlparse(href).netloc:
                            if urlparse(href).netloc and urlparse(href).netloc not in ext and '@' not in urlparse(
                                    href).netloc and '(' not in urlparse(
                                href).netloc and ';' not in urlparse(
                                href).netloc:
                                ext.append(urlparse(href).netloc)
                        else:
                            if href not in visited:
                                visited.append(href)
                                pool.append(href)
                                count += 1
            except:
                pass

        if ext:
            return True, [{'object': i} for i in ext]
        else:
            return False, 'Result is empty'
