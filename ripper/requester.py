import requests
requests.packages.urllib3.disable_warnings()

class Requester(object):

    def __init__(self):
        self.headers = {
            "user-agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "accept" : "*/*",
            "accept-encoding" : "gzip, deflate",
            "accept-language" :"en-US,en;q=0.8"
        }

    def get_source(self,url):
        return self._request(url)


    def get_stream(self,url):
        return self._request(url,True)

    def get_type(self,url):
        try:
            r = requests.get(url, headers=self.headers,verify=False, timeout=2)
            c = r.headers["content-type"]
            return c.split(";")[0] if c else ""
        except:
            return ""


    def _request(self,url,stream=False):
        try:
            r = requests.get(url, headers=self.headers,verify=False,stream=stream,timeout=2)
            if r.status_code == 200:
                return r
            else:
                return False
        except:
            return False
