import os
import uuid
from .mimes import Mimes, Mime
from .requester import Requester

class Asset(object):

    def __init__(self, base, resource, marker):
        self.assets_dir = "assets"
        self.source = resource
        self.mime = self._get_mime()
        self.marker = marker
        self.existing = False

        if self.mime:
            self._set_asset_info(base)
        else:
            self.path = None
            self.url = None
            self.relative_url = None

        self.downloaded = False


    def _get_mime(self):
        requester = Requester()
        m = Mimes.by_extension(self.source.extension)
        m = m if m else Mimes.by_content_type(requester.get_type(self.source.url))
        return m if m else None

    def _set_asset_info(self, base):
        name = self.source.filename if self.mime.use_file_name and self.source.filename and len(self.source.filename) > 0 else str(uuid.uuid4())[:8] + self.mime.extension
        assets_url = self.assets_dir

        self.path = os.sep.join([base,self.assets_dir,self.mime.category,name])
        self.url = "/".join([assets_url,self.mime.category,name])
        self.relative_url = "/".join(["..",self.mime.category,name])
