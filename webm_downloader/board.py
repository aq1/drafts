# -*- coding: utf8 -*-

import urllib.request
import re
import json
import pprint
import pickle
import multiprocessing


from dot_dictionary import DotDictionary


CATALOG_URL = 'https://2ch.hk/{}/catalog.json'
THREAD_URL = 'https://2ch.hk/{}/res/{}.json'
QUERY = r'(webm | цуиь)'


class AbstractDownloader(object):

    def _download(self):
        raw_data = urllib.request.urlopen(self._get_download_url())
        json_data = raw_data.read().decode()
        self.data = DotDictionary(json.loads(json_data))
        self.pickle()

    def _unpickle(self):
        try:
            with open(self._get_filename(), 'rb') as f:
                self.data = DotDictionary(pickle.load(f))
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
        for thread in self.data.threads:
            if query.search(thread.comment):
                thread = Thread(number=thread.num, local=False)
                self.threads.append(thread)
                # print(thread)
                # print(thread.data)

    def __repr__(self):
        return 'Catalog /{}/'.format(self.board)


class Thread(AbstractDownloader):

    def __init__(self, board='b', number=None, local=False):
        self.board = board
        self.number = number
        self.data = None
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

    def __repr__(self):
        return 'Thread {}/{}'.format(self.board, self.number)


catalog = Catalog(local=False)
catalog.search_threads()


# link = 'http://2ch.pm/mov/src/612287/14382631576770.webm'
# u = urllib.request.urlopen(link)
# f = open('out.webm', 'wb')
# f.write(u.read())
# f.close()
