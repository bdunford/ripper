import io
import sys
import re

class Stripper(object):
    #TODO ADD a GLOBAL STRIP OF ANY REFERENCE to base domain this may need to be called before any writes to disk for all assets in to everything
    #TODO ADD STRIPS FOR
    @staticmethod
    def Patterns():
        return [
            ("(?P<crap>\(function\(i[,\s]+s[,\s]+o[,\s]+g[,\s]+r[,\s]+a[,\s]+m\)[^<]*(ga\([^\)]\)\;)*)","/* Stripped Google Anylitics Yeah! */"),
            ("(?P<crap>integrity\=\"[^\"]+\")",""),
        ]

    @staticmethod
    def Strip(content):
        for p in Stripper.Patterns():
            x = re.compile(p[0],re.MULTILINE)
            matches = x.findall(content)
            if matches and len(matches):
                for m in matches:
                    r = m[0] if isinstance(m,tuple) else m
                    content = content.replace(r,p[1])

        return content
