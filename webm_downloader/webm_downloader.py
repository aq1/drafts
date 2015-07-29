# -*- coding: utf8 -*-

import urllib.request
import re
import json
import pprint
import pickle
import multiprocessing


from dot_dictionary import DotDictionary


URL = 'https://2ch.hk/{}/catalog.json'
QUERY = r'(webm | цуиь)'


class Catalog(object):

    def __init__(self, board='b', local=False, get_data_on_init=True):
        self.board = board
        self.data = None

        if local:
            self.get_catalog = self._unpickle
        else:
            self.get_catalog = self._download

        if get_data_on_init:
            self.get_catalog()

    def _get_filename(self):
        return 'catalog_{}.pickle'.format(self.board)

    def _unpickle(self):
        try:
            with open(self._get_filename(), 'rb') as f:
                self.data = DotDictionary(pickle.load(f))
        except (FileNotFoundError, pickle.UnpicklingError):
            return

    def _download(self):
        raw_data = urllib.request.urlopen(URL.format(self.board))
        self.json = raw_data.read().decode()
        self.data = DotDictionary(json.loads(self.json))

    def pickle(self):
        with open(self._get_filename(), 'wb') as f:
            pickle.dump(self.data, f)

    def search_threads(self, query=QUERY):
        if not self.data:
            return None

        query = re.compile(query, flags=re.IGNORECASE | re.UNICODE)
        for thread in self.data.threads:
            if query.search(thread.comment):
                print(thread.comment.decode('utf8'))
                # print(thread.keys())
                # print(thread.num)
