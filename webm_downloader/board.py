# -*- coding: utf8 -*-

try:
    import urllib.request as request
    import urllib.error.HTTPError as HTTPError
except ImportError:
    import urllib2 as request
    from urllib2 import HTTPError

import re
import json
import pprint
import pickle
import time
import multiprocessing

import scraper_threads as scraper

import sys

reload(sys)
sys.setdefaultencoding('utf8')

BOARD_URL = 'https://2ch.pm/'
CATALOG_URL = BOARD_URL + '{}/catalog.json'
THREAD_URL = BOARD_URL + '{}/res/{}.json'
QUERY = r'(webm | цуиь | шebm)'
WEBM = 6


class AbstractDownloader(object):

    def _download(self):
        raw_data = request.urlopen(self._get_download_url())
        json_data = raw_data.read().decode()
        self.data = json.loads(json_data)
        self.pickle()

    def _unpickle(self):
        try:
            with open(self._get_filename(), 'rb') as f:
                self.data = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError) as e:
            print(e)

    def pickle(self):
        with open(self._get_filename(), 'wb') as f:
            pickle.dump(self.data, f)


class Catalog(AbstractDownloader):

    def __init__(self, board='b', local=False, get_data_on_init=True):
        self.board = board
        self.threads = []
        self.data = None

        if local:
            self.get_catalog = self._unpickle
        else:
            self.get_catalog = self._download

        if get_data_on_init:
            self.get_catalog()

    def _get_filename(self):
        return 'catalog_{}.pickle'.format(self.board)

    def _get_download_url(self):
        return CATALOG_URL.format(self.board)

    def search_threads(self, query=QUERY):
        if not self.data:
            return None

        query = re.compile(query, flags=re.IGNORECASE | re.UNICODE)
        for thread in self.data['threads']:
            if query.search(thread['comment']):
                thread = Thread(number=thread['num'], local=False)
                self.threads.append(thread)

    def start_downloads(self):
        for thread in self.threads:
            thread.find_webms()
            thread.start_download()

    def __repr__(self):
        return 'Catalog /{}/'.format(self.board)


class Thread(AbstractDownloader):

    def __init__(self, board='b', number=None, local=False):
        self.number = number
        self.last_post_number = 0
        self.board = board
        self.data = {}
        self.webms = []

        if local:
            self.get_thread = self._unpickle
        else:
            self.get_thread = self._download

        if number:
            self.get_thread()

    def _get_filename(self):
        return 'thread_{}_{}.pickle'.format(self.board, self.number)

    def _get_download_url(self):
        return THREAD_URL.format(self.board, self.number)

    def start_download(self):
        multiprocessing.Process(
            target=scraper.main, args=(self.webms,)).start()

        self.wait_and_download()

    def find_webms(self):
        posts = self.data['threads'][0]['posts']
        print('Got %s was %s' % (posts[-1]['num'], self.last_post_number))
        if posts[-1]['num'] <= self.last_post_number:
            print('waitng')
            self.wait_and_download()
            return

        print('Downloading')

        for post in posts:
            try:
                files = post['files']
            except KeyError:
                continue

            for f in files:
                if f['type'] == WEBM:
                    fullpath = BOARD_URL + self.board + '/' + f['path']
                    self.webms.append((fullpath, f['md5']))

        self.last_post_number = posts[-1]['num']

    def wait_and_download(self, seconds=1):
        time.sleep(seconds)
        try:
            print('Downloading')
            self.get_thread()
        except HTTPError:
            print('Got HTTPError, exiting')
            exit()
        else:
            self.find_webms()

    def __repr__(self):
        return 'Thread {}/{}'.format(self.board, self.number)


if __name__ == '__main__':
    catalog = Catalog(local=False)
    catalog.search_threads()
    catalog.start_downloads()
