from urlparse import urlparse, urljoin
from .helpers import Helpers


#TODO make sure the list is unique
class Resource(object):
    def __init__(self,path,page_url):
        base = urlparse(page_url)
        ref =  urlparse(path)

        self.reference = path
        self.filename = ref.path[ref.path.rfind('/'):][1:] if ref.path.rfind('/') > -1 else False
        self.extension = ref.path[ref.path.rfind('.'):] if ref.path.rfind('.') > -1 else False

        if ref.netloc:
            self.url = ref.geturl() if ref.scheme else "{0}:{1}".format(base.scheme,ref.geturl())
        else:
            self.url = urljoin(base.geturl(),ref.geturl())

class Resources(object):

    def __init__(self,request):
        page_parser = self._get_page_parser(request);
        if page_parser:
            self._resources = map(lambda x: Resource(x,request.url),self._clean(page_parser(request.text)))
        else:
            self._resources = []

    def __iter__(self):
       return self._resources.__iter__()

    def next(self):
        return self._resources.next()

    def _get_page_parser(self,request):
        if request.headers["content-type"].find("/css") > -1:
            return self._find_in_styles
        if request.headers["content-type"].find("/javascript") > -1:
            return self._find_in_scripts
        if request.headers["content-type"].find("/x-javascript") > -1:
            return self._find_in_scripts
        if request.headers["content-type"].find("/html") > -1:
            return self._find_in_html

        if request.headers["content-type"].find("/xhtml") > -1:
            return self._find_in_html

        return False


    def _find_in_html(self,source):

        patterns = [
            "src\s*\=\s*\'(?P<url>[^\')]+)\'",
            'src\s*\=\s*\"(?P<url>[^\")]+)\"',
            'link[^\>]+href\s*\=\s*\"(?P<url>[^\")]+)\"',
            "link[^\>]+href\s*\=\s*\'(?P<url>[^\')]+)\'",
        ]
        references = Helpers.find_with_regex(source,patterns)
        references += self._find_in_styles(source)

        return references


    def _find_in_scripts(self,source):
        patterns = [
            '\"src\"[\,\s]+\"(?P<url>[^\")]+)\"\)',
            "\'src\'[\,\s]+\'(?P<url>[^\')]+)\'\)"
        ]
        return Helpers.find_with_regex(source,patterns)

    def _find_in_styles(self,source):
        patterns = [
            "url\(\'(?P<url>[^\')]+)\'\)",
            'url\(\"(?P<url>[^\")]+)\"\)',
            'url\((?P<url>[^\"\'\)]+)\)',
        ]
        return Helpers.find_with_regex(source,patterns)

    def _as_string_array(self,a):
        return map(lambda x: str(x),a)

    def _clean(self, references):
        return list(set(filter(lambda x: x.lower().find("data:") != 0,references)))


    #import statments
    #https://developer.mozilla.org/en-US/docs/Web/CSS/@import
    #images as url
    #url('somthing.png')
