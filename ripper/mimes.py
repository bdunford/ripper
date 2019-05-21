
class Mime(object):
    def __init__(self,content_type, category, extension, stream=False, use_file_name=False):
        self.content_type = content_type
        self.category = category
        self.extension = extension
        self.stream = stream
        self.use_file_name = use_file_name

class Mimes(object):

    @staticmethod
    def all():
        return [
            Mime("application/javascript","scripts",".js"),
            Mime("text/javascript","scripts",".js"),
            Mime("application/x-javascript","scripts",".js"),
            Mime("text/css","styles",".css"),
            Mime("application/json","data",".json"),
            Mime("text/json","data",".json"),
            Mime("text/x-json","data",".xml"),
            Mime("application/xml","data",".xml"),
            Mime("text/xml","data",".xml"),
            Mime("application/rss+xml","data",".xml"),
            Mime("text/plain","data",".txt"),
            Mime("image/jpg","images",".jpg", True),
            Mime("image/jpeg","images",".jpg", True),
            Mime("image/png","images",".png", True),
            Mime("image/gif","images",".gif", True),
            Mime("image/bmp","images",".bmp", True),
            Mime("image/tiff","images",".tiff", True),
            Mime("image/x-icon","images",".ico", True),
            Mime("image/vnd.microsoft.icon","images",".ico",True),
            Mime("font/woff","fonts",".woff",True,True),
            Mime("font/woff2","fonts",".woff2",True,True),
            Mime("application/font-woff","fonts",".woff",True,True),
            Mime("application/font-woff2","fonts",".woff2",True,True),
            Mime("image/svg+xml","fonts",".svg", True,True),
            Mime("application/octet-stream","fonts","ttf",True,True),
            Mime("application/octet-stream","fonts","eot",True,True),
            Mime("application/vnd.ms-fontobject","fonts","eot",True,True)

        ]

    @staticmethod
    def by_content_type(content_type):
        if content_type:
            m = filter(lambda x: x.content_type.lower() == content_type.lower(), Mimes.all())
            if len(m) > 0:
                return m[0]
        return False


    @staticmethod
    def by_extension(extension):
        if extension:
            m = filter(lambda x: x.extension.lower() == extension.lower(),Mimes.all())
            if len(m) > 0:
                return m[0]
        return False
