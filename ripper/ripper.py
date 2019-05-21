import os
import sys
import traceback
import uuid
import time
import copy
from .requester import Requester
from .resources import Resources, Resource
from .writer import Writer
from .window import Window
from .asset import Asset
from .threads import Threader
from .pages import Pages, Page
from .stripper import Stripper
from urlparse import urlparse, urljoin
from threading import *


class Generic(object):
    pass

#TODO NEED TO TREAT DATA LIKE SCRIPTS and replace references

class Ripper(object):

    def __init__(self, logger=None, threads=4):
        self.logger = logger
        self.threads = threads
        self.stats = {}
        self.assets = []
        self.errors = []
        self.pages = []
        self.is_threading = False
        self.extension = ".html"
        self.totals = {"pages":1,"assets":0, "pages_down":0, "assets_down":0}
        self.lock = Lock()

    def rip(self,url,base, top_level_pages=True):
        self.url = url
        self.base = base
        self.index_file = os.path.join(base,"index" + self.extension)
        self.stats = {}
        self.assets = []
        self.pages = []

        index = self._get_page(self.url);
        self._update_totals("pages_down",1)

        if not index:
            raise ValueError('Could not access website. Is the URL correct?')

        self.pages = self._get_page_links(self.url,index)

        if top_level_pages:

            self._update_totals("pages",len(self.pages))

            for p in self.pages:
                if not p.exists:
                    if p.replace_reference:
                        content = self._get_page(p.url);
                        if not content:
                            content = "<html></html>"
                        else:
                            content = self._update_page_links(content,self.extension)
                            pages = self._get_page_links(self.url,content)
                            content = self._update_page_links(content,self.extension)
                            content = self._remove_page_links(content,pages)
                            content = self._remove_trackers(content)
                            p.downloaded = True

                        Writer.write(content,os.path.join(self.base,p.name + self.extension))
                    self.logger(self,p)
                    self._update_totals("pages_down",1)

            index = self._update_page_links(index,self.extension)
        else:
            index = self._remove_page_links(index,self.pages,False)

        index = self._remove_trackers(index)
        Writer.write(index,self.index_file)
        self.logger(self,Page(urlparse(self.url).path,self.url,"index",False))

    def _get_page(self,url,relative_assets=False):

        requester = Requester()
        page = requester.get_source(url)

        if page:

            content = page.text
            marker = str(uuid.uuid4())

            threader = False
            if not self.is_threading:
                threader = Threader(self.threads,self._log_asset)
                threader.start(True)
                self.is_threading = True


            resources = Resources(page)
            self._update_totals("assets",self._get_total_assets_to_download(resources))

            for r in resources:

                if threader:
                    threader.add((self._get_asset,{"resource" : r, "marker" : marker}))
                else:
                    asset = self._get_asset(r,marker)
                    self._log_asset(asset)

            if threader:
                threader.finish()
                if threader.errors:
                    self.errors += threader.errors

            return self._update_page_assets(content,marker,relative_assets)
        else:
            return False

    def _get_page_links(self,url,content):
        pages = []
        for p in Pages(url,content):
            if p.reference in map(lambda x: x.url, self.assets):
                p.replace_reference = False
            pages.append(p)
        return pages

    def _get_asset(self,resource,marker):
        requester = Requester()
        asset_exists = self._find_asset_by_reference(resource,marker)
        if asset_exists:
            return asset_exists
        else:
            asset = Asset(self.base,resource,marker)
            if asset.mime:
                x = requester.get_stream(asset.source.url) if asset.mime.stream else self._get_page(asset.source.url,False if asset.mime.category == "scripts" else True)
                if x:
                    Writer.write(x,asset.path)
                    asset.downloaded = True
            return asset

    def _find_asset_by_reference(self,resource,marker):
        find = self._check_asset_exists(resource)
        if find:
            asset = copy.deepcopy(find)
            asset.resource = resource
            asset.marker = marker
            asset.existing = True
            return asset
        else:
            return False

    def _check_asset_exists(self,resource):
        find = filter(lambda a: a.source.reference == resource.reference or a.source.url == resource.url,list(self.assets))
        if len(find) > 0:
            return find[0]
        else:
            return False


    def _log_asset(self,asset):
        if asset.downloaded:
            self._update_stats(asset.mime)
            if not asset.existing:
                self._update_totals("assets_down",1)
        self.assets.append(asset)
        self.logger(self,asset)

    def _update_page_assets(self,content,marker,relative_assets):
        for asset in self.assets:
            if asset.downloaded == True and asset.marker == marker:
                content = self._find_and_replace(content,asset.source.reference,asset.relative_url if relative_assets else asset.url)
        return content

    def _update_page_links(self,content,extension):
        for page in self.pages:
            if page.replace_reference:
                wrap = "{0}{1}{0}"
                content = self._find_and_replace(content,wrap.format('"',page.reference),wrap.format('"',page.name + extension))
                content = self._find_and_replace(content,wrap.format("'",page.reference),wrap.format("'",page.name + extension))
        return content

    def _remove_page_links(self,content,pages,check_pages=True):

        for page in pages:
            if len(filter(lambda p: p.name == page.name,self.pages)) == 0 or not check_pages:
                if page.replace_reference:
                    wrap = "{0}{1}{0}"
                    content = self._find_and_replace(content,wrap.format('"',page.reference),wrap.format('"#',page.name))
                    content = self._find_and_replace(content,wrap.format("'",page.reference),wrap.format("'#",page.name))
        return content

    def _remove_trackers(self, content):
        return Stripper.Strip(content)

    def _find_and_replace(self,text,find,replace):
        text = text.replace(find,replace)
        return text

    def _update_stats(self,mime):
        if mime.category in self.stats:
            self.stats[mime.category] += 1
        else:
            self.stats[mime.category] = 1

    def _update_totals(self,key,value):
        with self.lock:
            self.totals[key] += value

    def _get_total_assets_to_download(self,resources):
        #TODO this needs to compare both the reference and the url just like the _find_asset_by_reference
        return len(list(filter(lambda r: self._check_asset_exists(r),list(resources))))
        #return len(list(filter(lambda r: r.reference not in map(lambda a: a.source.reference,list(self.assets)),list(resources._resources))))
