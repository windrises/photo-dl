import sys
import requests
import threading
import traceback
from lxml import etree
from photo_dl.log import log
from requests.adapters import HTTPAdapter
from photo_dl.config import headers
from photo_dl.config import timeout
from photo_dl.config import max_retries
from photo_dl.config import threads as _thread_size


signal_flag = True


def set_signal():
    global signal_flag
    signal_flag = False
    print(signal_flag)


def request(url, html_flag=True):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=max_retries))
    session.mount('https://', HTTPAdapter(max_retries=max_retries))
    response = session.get(url=url, headers=headers, timeout=timeout)
    if html_flag:
        response.encoding = 'utf-8'
        return etree.HTML(response.text)
    return response


class RequestThread(threading.Thread):
    def __init__(self, url, info=None, html_flag=True):
        threading.Thread.__init__(self)
        self.url = url
        self.info = info
        self.html_flag = html_flag
        self.response = None

    def run(self):
        try:
            self.response = request(self.url, self.html_flag)
        except:
            log('%s\n%s' % (self.url, traceback.format_exc()))


class MultiRequest:
    def __init__(self, urls, name='', progress=True, html_flag=True, thread_size=_thread_size):
        self.urls = urls
        self.name = name
        self.progress = progress
        self.html_flag = html_flag
        self.thread_size = thread_size
        self.threads = []
        self.count = 1

    def get_generator(self):
        for url in self.urls:
            yield url

    def put_request(self):
        global signal_flag
        generator = self.get_generator()
        while signal_flag:
            if threading.activeCount() < self.thread_size:
                url = next(generator, None)
                if url is None:
                    break
                thread = RequestThread(url['url'], url.get('info'), self.html_flag)
                thread.start()
                self.threads.append(thread)
                if self.progress:
                    print('\r[%d / %d] %s' % (self.count, len(self.urls), self.name), end='')
                self.count += 1

    def run(self):
        if len(self.urls) == 0:
            return []
        _threads = []
        try:
            put_thread = threading.Thread(target=self.put_request)
            put_thread.start()
            put_thread.join()
            for thread in self.threads:
                thread.join()
                _threads.append(thread)
        except SystemExit:
            sys.exit()
        except:
            log('%s\n%s' % (self.name, traceback.format_exc()))
        return _threads
