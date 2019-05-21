from threading import *
import time
import atexit

class Threader(object):

    def __init__(self, threads, onSucess=None, onError=None, actions=[]):
        self.waitForWork = False
        self.threads = []
        self.threadCount = threads
        self.work = actions
        self.errors = None
        self.onSucess = onSucess
        self.onError = onError
        self.qlock = Lock()
        self.xlock = Lock()
        self.elock = Lock()
        self.isKilled = False

    def add(self,action):
        with self.qlock:
            self.work.append(action)

    def start(self, waitForWork=False):
        self.waitForWork = waitForWork

        for tc in range(self.threadCount):
            t = Thread(target=self._getWork)
            t.start()
            self.threads.append(t)

        if not waitForWork:
            self._join()

    def finish(self):
        self.waitForWork = False
        self._join()

    def kill(self):
        self.work = []
        self.isKilled = True

    def _join(self):
        for t in self.threads:
            t.join()

    def _nextWorkItem(self):
        with self.qlock:
            if len(self.work) > 0:
                return self.work.pop(0)
        if self.waitForWork:
            time.sleep(.2)
            return self._nextWorkItem()
        return False

    def _getWork(self):
        w = self._nextWorkItem()
        while w:
            self._doWork(w)
            w = self._nextWorkItem()

    def _doWork(self,w):
        try:
            r = None
            if isinstance(w,tuple):
                r = w[0](**w[1])
            else:
                r = w()
            if self.onSucess:
                with self.xlock:
                    if not self.isKilled:
                        self.onSucess(r)

        except Exception, e:
            if self.onError:
                with self.elock:
                    self.onError(e)
            if not self.errors:
                self.errors = []
            self.errors.append(str(e))
