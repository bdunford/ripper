import os
import sys
import traceback
import time
from urlparse import urlparse
from .ripper import Ripper
from .options import Options
from .window import Window


class WindowManager(object):
    def __init__(self):
        self.window = None
        self.header = False

    def close(self):
        if self.window:
            self.window.close()

wm = WindowManager()

def _header_log(ripper):
    return [
        "-" * 100,
        (" " * 30) + ">>Ripper<<",
        (" " * 20) + "( Just borrowing some websites )",
        " ",
        "website:     %s" % ripper.url,
        "destination: %s" % ripper.base,
        " ",
    ]

def _window_log(ripper,entry):

    log = _header_log(ripper)
    log.append("-" * 100)
    for k,v in ripper.stats.iteritems():
        log.append("{0}: {1}".format(k,v))

    log.append(" ")

    if type(entry).__name__ == "Page":
        log.append("GET: %s" % entry.reference)
        log.append("AS: %s" % entry.name + ripper.extension if entry.replace_reference else entry.reference)
        log.append("TYPE: Page")
        log.append("STATUS: Already Exists" if entry.exists or not entry.replace_reference else "STATUS: Ripped")
    else:
        log.append("GET: %s" % entry.source.reference)
        log.append("AS: %s" % entry.path)
        log.append("TYPE: Asset")
        log.append("STATUS: %s" % "Downloaded" if entry.downloaded else "Failed")
    wm.window.write(log)

def _console_log(ripper, entry):
    if not wm.header:
        for h in _header_log(ripper):
            print h
        print "-" * 100
        wm.header = True
    if type(entry).__name__ == "Page":
        print "[+] Page: %s" % entry.reference
    else:
        if entry.downloaded:
            #print "[+] Asset: %s"  % urlparse(entry.source.reference).path[-100:]
            print "[+] Asset: %s"  % entry.source.reference
        else:
            print "[-] Failed: %s" % entry.source.url[:100]

def _init_logger(window=True):
    if window:
        wm.window = Window(100)
        return _window_log
    else:
        return _console_log

def rip():

    s = time.time()
    o = Options()

    try:
        destination = o.destination.rstrip(os.sep) if o.destination[0:1] == os.sep else os.getcwd() + os.sep + o.destination.rstrip(os.sep)
        x = Ripper(_init_logger(o.window),o.threads)
        x.rip(o.url,destination,o.top_level_pages)
        wm.close()
        if len(x.errors) > 0:
            print x.errors
        print "-" * 100
        print "Pages Ripped: %s" % x.totals["pages_down"]
        print "Assets Downloaded: %s" % str(len(set(map(lambda m: m.path ,filter(lambda f: f.downloaded == True, x.assets)))))
        print "Assets Failed: %s" % str(len(set(map(lambda m: m.source.reference ,filter(lambda f: f.downloaded == False, x.assets)))))
        print "Time Elapsed: %s" % str(time.time() - s)
        print "-" * 100
    except:
        wm.close()
        print "{0} Error {0}".format("-" * 45)
        print "Unable to Rip: %s" % o.url
        print "To Location: %s" % destination
        print "-" * 100
        print "Error: %s"  % traceback.format_exc()
        print "-" * 100
