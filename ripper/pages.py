import os
import re
from urlparse import urlparse, urljoin
from .helpers import Helpers



class Page(object):
    def __init__(self,href,url,name,exists):
        self.reference = href
        self.url = url
        self.name = name
        self.exists = exists
        self.replace_reference = True

class Pages(object):

    def __init__(self,url,source):
        self._pages = []
        self.url = urlparse(url)
        for href in self._find_hrefs(source):
            p = self._as_page(href)
            if p:
                self._pages.append(p)

    def __iter__(self):
        return self._pages.__iter__()

    def next(self):
        return self._pages.next()

    def _find_hrefs(self,source):
        patterns = [
            "\<a[^\>]+href\=\'(?P<url>[^\']+)\'",
            '\<a[^\>]+href\=\"(?P<url>[^\"]+)\"'
        ]
        return Helpers.find_with_regex(source,patterns)

    def _as_page(self,href):
        parsed = urlparse(href)
        if parsed.netloc in ["",self.url.netloc] and href[:1] != "#":
            if parsed.netloc:
                url = parsed.geturl()
            else:
                url = urljoin(self.url.geturl(),parsed.geturl())

            name = self._get_page_name(parsed)
            exists = True if name == "index" or name in map(lambda x: x.name,self._pages) else False

            return Page(href,url,name,exists)
        return False

    def _get_page_name(self,parsed):
        name = parsed.path.strip("./").replace("/","-")
        if re.findall("\.[^-]+$",name):
            return name.split(".")[0]
        else:
            return "index" if name == "" else name
