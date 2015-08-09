# -*- coding: utf8 -*-

try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

import os
import sys
import threading
from cStringIO import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from will_beams import models

urls = []

FOLDER = 'webm'


def setup_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "WillBeams.settings"
    sys.path.append("WillBeams/")


def save_file(name, data, mdb, semaphore):
    with open(os.path.join(FOLDER, name), 'wb') as f:
        f.write(data)

    print('Finished %s' % name)
    semaphore.release()


def get_url(url, md5, semaphore):
    raw_data = request.urlopen(url)
    save_to_django_model(name=url.split('/')[-1],
                         data=raw_data.read(),
                         semaphore=semaphore,
                         md5=md5)


def save_to_django_model(name, data, md5, semaphore=None):
    print('name', name)
    print('md5', md5)

    buf = StringIO(data)
    buf.seek(0, 2)
    webm = InMemoryUploadedFile(
        buf, 'video', name, None, buf.tell(), None)
    django_webm = models.Webm(md5=md5)
    django_webm.video.save(name, webm)
    semaphore.release()


def main(urls):
    setup_django()

    print('PID %s has started for %s webms' %
          (os.getpid(), len(urls)))

    semaphore = threading.BoundedSemaphore(value=2)
    with semaphore:
        try:
            for url, md5 in urls:
                print('Starting %s' % url)
                semaphore.acquire()
                t = threading.Thread(
                    target=get_url, args=(url, md5, semaphore))
                t.deamon = True
                t.start()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    main()
